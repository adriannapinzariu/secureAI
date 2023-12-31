import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras.models import Model
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import urllib
import openai
from transformers import pipeline

openai.api_key = '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'

def analyze_sentiment(review):
    # Initialize the sentiment analysis pipeline
    sentiment_analyzer = pipeline('sentiment-analysis')

    # Analyze the sentiment of the review
    result = sentiment_analyzer(review)[0]
    
    # result is a dictionary with 'label' and 'score' keys. 'label' could be 'POSITIVE' or 'NEGATIVE', and 'score' is a float
    return result

def analyze_reviews(reviews):
    # reviews should be a list of strings, where each string is a review text
    negative_reviews = []

    for review in reviews:
        sentiment = analyze_sentiment(review)

        if sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.5:  # You can adjust the threshold as needed
            negative_reviews.append(review)

    return negative_reviews

def create_autoencoder(input_shape):
    # Encoder
    inputs = Input(input_shape)
    conv1 = Conv2D(16, 3, activation='relu', padding='same')(inputs)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(32, 3, activation='relu', padding='same')(pool1)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(64, 3, activation='relu', padding='same')(pool2)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    # Decoder
    conv4 = Conv2D(64, 3, activation='relu', padding='same')(pool3)
    up1 = UpSampling2D((2, 2))(conv4)
    conv5 = Conv2D(32, 3, activation='relu', padding='same')(up1)
    up2 = UpSampling2D((2, 2))(conv5)
    conv6 = Conv2D(16, 3, activation='relu', padding='same')(up2)
    up3 = UpSampling2D((2, 2))(conv6)
    outputs = Conv2D(1, 3, activation='sigmoid', padding='same')(up3)

    model = Model(inputs, outputs)
    return model

def train_autoencoder(image_dataset):
    # Preprocess the image dataset
    image_dataset = image_dataset.astype('float32') / 255.0

    # Create and compile the autoencoder model
    input_shape = image_dataset.shape[1:]
    autoencoder = create_autoencoder(input_shape)
    autoencoder.compile(optimizer='adam', loss='mse')

    # Train the autoencoder
    autoencoder.fit(image_dataset, image_dataset, epochs=10, batch_size=32, verbose=1)

    return autoencoder

def detect_outliers(autoencoder, image_dataset, threshold):
    # Use the trained autoencoder to reconstruct images
    reconstructed_images = autoencoder.predict(image_dataset)

    # Compute the mean squared error (MSE) between original and reconstructed images
    mse = np.mean(np.square(image_dataset - reconstructed_images), axis=(1, 2, 3))

    # Identify outliers based on the MSE
    outliers = np.where(mse > threshold)[0]

    return outliers

def process_image(autoencoder, img):
     # Preprocess the image
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)

    # Use the trained autoencoder to reconstruct the image
    reconstructed_img = autoencoder.predict(img)

    # Compute the mean squared error (MSE) between the original and reconstructed image
    mse = np.mean(np.square(img - reconstructed_img))

    return mse

def analyze_outliers_with_openai(outliers, image_metadata):
    # Convert your outlier data to text descriptions or labels
    outlier_data = []
    for idx in outliers:
        outlier_data.append(image_metadata[idx])  # assuming image_metadata is a list of descriptions or labels

    # Initialize OpenAI API
    openai.api_key = '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'

    # Setup chat messages
    chat_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Identify patterns in the following image descriptions: " + ", ".join(outlier_data)}
    ]

    # Request OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or any other compatible model
        messages=chat_messages
    )

    # Get the model's response
    assistant_response = response['choices'][0]['message']['content']
    
    return assistant_response

def main():
    print("Image Outlier Detection")
    url = 'https://www.hotels.com'
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

        # Extract alt attributes as image metadata
        img_alts = [img.get('alt', '') for img in img_tags]

        print(f"Found {len(img_urls)} image URLs")

        # Load the image dataset from scraped URLs
        image_dataset = []
        for i, img_url in enumerate(img_urls):
            try:
                print(f"Downloading image {i}")
                # Download the image
                img_data = requests.get(img_url).content

                # Save the image
                img_filename = f'image_{i}.jpg'
                with open(img_filename, 'wb') as handler:
                    handler.write(img_data)

                print(f"Saved {img_filename}")

                # Load the image with tensorflow
                img = tf.keras.preprocessing.image.load_img(img_filename, target_size=(256, 256))
                img = tf.keras.preprocessing.image.img_to_array(img)
                image_dataset.append(img)
            except Exception as e:
                print(f"Unable to download or process image_{i}. Error: {e}")

        # Convert the list to numpy array
        image_dataset = np.array(image_dataset)

        # Preprocess the image dataset
        image_dataset = image_dataset.astype('float32') / 255.0

        # Train the autoencoder
        autoencoder = train_autoencoder(image_dataset)

        # Process all images and calculate MSE for each
        mse_values = []
        for i, img in enumerate(image_dataset):
            mse = process_image(autoencoder, img)
            mse_values.append(mse)
            print(f"MSE for image {i}: {mse}")

        # Analyze MSE values to detect outliers
        # This is a simple example, you can use more sophisticated methods
        threshold = 0.04
        # Detect outliers
        outliers = detect_outliers(autoencoder, image_dataset, threshold)
        print(f"Number of outlier images detected: {len(outliers)}")

        # Extract reviews
        review_tags = soup.find_all('div', {'class': 'review'})  # Replace with appropriate tag and class name
        reviews = [review.get_text() for review in review_tags]

        print(f"Found {len(reviews)} reviews")

        # Analyze reviews
        negative_reviews = analyze_reviews(reviews)
        print(f"Found {len(negative_reviews)} negative reviews")
        
        for review in negative_reviews:
            print(review)

        # Analyze outliers with OpenAI GPT-3
        assistant_response = analyze_outliers_with_openai(outliers, img_alts)
        print(f"Assistant's insights on outliers: {assistant_response}")

        # Make a directory to save the outlier images
        os.makedirs('outliers', exist_ok=True)

        # Save the outlier images
        for i in outliers:
            outlier_img = image_dataset[i]
            outlier_img_filename = f'outliers/outlier_{i}.jpg'
            tf.keras.preprocessing.image.save_img(outlier_img_filename, outlier_img)
            print(f"Saved outlier image to {outlier_img_filename}")
    else:
        print(f"Failed to send GET request to {url}. Status code: {response.status_code}")

    
if __name__ == '__main__':
    main()

    


