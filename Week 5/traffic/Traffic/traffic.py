import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import keras
from keras import layers
import PIL 

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Test out load data
    # images, labels = load_data("gtsrb-small")
    # print(images[0])
    # print("_____________________")
    # print(labels[0])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    # start a loop for each category
    for i in range(NUM_CATEGORIES):
        #start a loop for all files
        cat_dir = os.path.join(data_dir, str(i))
        for img_dir in os.listdir(cat_dir):
            #read & resize an image
            image = cv2.imread(os.path.join(cat_dir, img_dir))
            # print("Before resizing:")
            # print(image.shape)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)   # BGR -> RGB
            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT), interpolation= cv2.INTER_LINEAR)
            # print("After resizing:")
            # print(image.shape)

            #add the corresponding elements to the list
            images.append(image)
            labels.append(i)
    
    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    # model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    
    model.add(tf.keras.layers.Flatten())
    
    model.add(tf.keras.layers.Dense(256, activation="relu"))
    model.add(tf.keras.layers.Dropout(0.5))

    # model.add(tf.keras.layers.Dense(256, activation="relu"))
    # model.add(tf.keras.layers.Dropout(0.5))
    
    model.add(tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )    

    model.summary()

    return model

if __name__ == "__main__":
    main()
