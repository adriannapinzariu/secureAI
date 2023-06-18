import streamlit as st
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras.models import Model
import numpy as np
import os

def main():
    st.title("Hello, World!")
    st.write("Welcome to my Streamlit app.")
    st.write("This is a basic example.")

if __name__ == '__main__':
    main()

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


def detect_outliers(image_dataset, threshold):
    # Preprocess the image dataset
    image_dataset = image_dataset.astype('float32') / 255.0

    # Create and compile the autoencoder model
    input_shape = image_dataset.shape[1:]
    autoencoder = create_autoencoder(input_shape)
    autoencoder.compile(optimizer='adam', loss='mse')

    # Train the autoencoder
    autoencoder.fit(image_dataset, image_dataset, epochs=10, batch_size=32, verbose=1)

    # Use the trained autoencoder to reconstruct images
    reconstructed_images = autoencoder.predict(image_dataset)

    # Compute the mean squared error (MSE) between original and reconstructed images
    mse = np.mean(np.square(image_dataset - reconstructed_images), axis=(1, 2, 3))

    # Identify outliers based on the MSE
    outliers = np.where(mse > threshold)[0]

    return outliers


def main():
    st.title("Image Outlier Detection")

    # Set the path to the image dataset directory
    dataset_dir = '/content/drive/MyDrive/test_imgs'

    # Set the threshold value for outlier detection
    threshold = 0.04

    # Load the image dataset
    image_dataset = []
    for filename in os.listdir(dataset_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img_path = os.path.join(dataset_dir, filename)
            img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
            img = tf.keras.preprocessing.image.img_to_array(img)
            image_dataset.append(img)
    image_dataset = np