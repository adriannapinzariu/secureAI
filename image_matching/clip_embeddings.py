import torch
import pinecone
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from datasets import load_dataset, Image, Dataset
import datasets
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer
from typing import Tuple
from sklearn.metrics.pairwise import cosine_similarity  
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pinecone.init(
   api_key = "",
   environment="asia-southeast1-gcp-free"  # find next to API key in console
)


def plot_images_by_side(top_images):
    index_values = list(top_images.index.values)
    list_images = [top_images.iloc[idx].image for idx in index_values]
    similarity_score = [top_images.iloc[idx].cos_sim for idx in index_values]
    n_row = n_col = 2
    _, axs = plt.subplots(n_row, n_col, figsize=(12, 12))
    axs = axs.flatten()
    for img, ax, sim_score in zip(list_images, axs, similarity_score):
        ax.imshow(img)
        sim_score = 100*float("{:.2f}".format(sim_score))
        caption = "1"
        ax.title.set_text(f"Caption: {caption}\nSimilarity: {sim_score}%")
    plt.show()

def get_dataset(files_path='/usr/src/app/data/train/files.txt'):
    with open(files_path, 'r') as f:
        # Read lines into a list
        lines = f.read().splitlines()
    #  Convert the list into a dictionary
    dict_files = {'image_url': lines, 'image': lines}
    dict_files = pd.DataFrame.from_dict(dict_files)
    image_data = Dataset.from_pandas(dict_files).cast_column("image", Image())
    return image_data
    

class CLIPModelPinecone:
    def __init__(self, model_ID="openai/clip-vit-base-patch32") -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.processor, self.tokenizer = self.get_model_info(model_ID, self.device)
        
        # Create an index for searching
        my_index_name = "clip-image-search"
        vector_dim = 512
        if my_index_name not in pinecone.list_indexes():
            # Create the vectors dimension
            pinecone.create_index(name = my_index_name,
                                dimension=vector_dim,
                                metric="cosine", shards=1,
                                pod_type='s1.x1')
        # Connect to the index
        self.my_index = pinecone.Index(index_name = my_index_name)


    def get_model_info(self,model_ID: str, device: str) -> Tuple:
        #  Save the model to device
        model = CLIPModel.from_pretrained(model_ID).to(device)
        # Get the processor
        processor = CLIPProcessor.from_pretrained(model_ID)
        # Get the tokenizer
        tokenizer = CLIPTokenizer.from_pretrained(model_ID)
        # Return model, processor & tokenizer
        return model, processor, tokenizer
    
    def get_single_text_embedding(self,text): 
        inputs = self.tokenizer(text, return_tensors = "pt")
        inputs['input_ids'] = inputs['input_ids'].to(self.device)
        inputs['attention_mask'] = inputs['attention_mask'].to(self.device)
        
        text_embeddings = self.model.get_text_features(**inputs)
        # convert the embeddings to numpy array
        embedding_as_np = text_embeddings.cpu().detach().numpy()
        return embedding_as_np
    
    def get_all_text_embeddings(self, df, text_col):
        df["text_embeddings"] = df[str(text_col)].apply(self.get_single_text_embedding)
        return df

    def get_single_image_embedding(self,my_image):
        image = self.processor(
                text = None,
                images = my_image,
                return_tensors="pt"
                )["pixel_values"].to(self.device)
        embedding = self.model.get_image_features(image)
        # convert the embeddings to numpy array
        embedding_as_np = embedding.cpu().detach().numpy()
        return embedding_as_np
    
    def get_all_images_embedding(self, df, img_column):
        embeddings = []
        for b in df:
            embeddings.append(self.get_single_image_embedding(b["image"]))
        print(len(embeddings))

        dset_embed = datasets.Dataset.from_dict({"img_embeddings": embeddings})
        dset_concat = datasets.concatenate_datasets([df, dset_embed], axis=1)
        print(len(dset_concat))
        return dset_concat
    
    def get_top_N_images(self, query, data, top_K=5, search_criterion="text"):
        # Text to image Search
        if(search_criterion.lower() == "text"):
            query_vect = self.get_single_text_embedding(query)
        # Image to image Search
        else:
            query_vect = self.get_single_image_embedding(query)
        print("query_vect: ", type(query_vect))
        print("query_vect: ", query_vect.shape)
        # Relevant columns
        revevant_cols = ["image", "cos_sim"]
        # Run similarity Search
        cos_sim = np.array([cosine_similarity(query_vect,x)[0,0] for x in np.array(data["img_embeddings"])[:,:,:]])
        print(cos_sim.shape)

        cos_sim = datasets.Dataset.from_dict({"cos_sim": cos_sim})
        data = datasets.concatenate_datasets([data, cos_sim], axis=1)
        
        # data["cos_sim"] = pd.DataFrame(np.array(data["img_embeddings"])[:,0,:]).apply(lambda x: cosine_similarity(query_vect, x))# line 17
        # data["cos_sim"] = data["cos_sim"].apply(lambda x: x[0][0])
        """
        Retrieve top_K (4 is default value) articles similar to the query
        """
        most_similar_articles = data.sort('cos_sim',  reverse=True)[1:top_K+1] # line 24
        most_similar_articles = pd.DataFrame.from_dict(most_similar_articles)
        return most_similar_articles.reset_index()
    
    def process_df_to_pinecone(self, df):
        df_urls = pd.DataFrame(df["image_url"])
        df_urls = list(df_urls.index)
        df_urls = [str(x) for x in df_urls]
        vector_id = datasets.Dataset.from_dict({"vector_id": df_urls})
        image_data_df = datasets.concatenate_datasets([df, vector_id], axis=1)

        #metadata
        final_metadata = []
        for index in range(len(image_data_df)):
            final_metadata.append({"ID": index, "image": image_data_df[index]["image_url"]})

        image_IDs = image_data_df['vector_id']
        image_embeddings = [arr for arr in image_data_df['img_embeddings']]
        data_to_upsert = list(zip(image_IDs, image_embeddings, final_metadata))
        # Upload the final data
        self.my_index.upsert(vectors = data_to_upsert)

    def search_pinecone(self, query, top_K=4):
        return self.my_index.query(query, top_k=top_K, include_metadata=True)
    
    def plot_result(self, results):
        # number of columns and rows for the plot
        ncols = 2
        nrows = len(results) // ncols + (len(results) % ncols > 0)

        # create a new figure
        fig, axes = plt.subplots(nrows, ncols, figsize=(10, 10))

        # iterate over the results
        for ax, result in zip(axes.flat, results):
            # read the image
            img = mpimg.imread(result['metadata']['image'])
            
            # display the image
            ax.imshow(img)
            
            # set the title
            ax.set_title('Score: {:.3f}'.format(result['score']))
            
            # remove axis
            ax.axis('off')

        # if there are less images than slots, remove the extra subplots
        if len(results) < nrows*ncols:
            for idx in range(len(results), nrows*ncols):
                fig.delaxes(axes.flatten()[idx])

        plt.tight_layout()
        plt.show()

    