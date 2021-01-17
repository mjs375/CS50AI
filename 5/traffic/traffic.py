"""
TRAFFIC
CS50: AI w/ Python
"""

import cv2
import numpy as np
import os
import re
import sys
import tensorflow as tf


# $ pip install -r requirements.txt

from sklearn.model_selection import train_test_split

#--
EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
# NUM_CATEGORIES = 3 # gtsrb-small (sample dataset)
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

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

    Assume `data_dir` has one directory named after each category, number 0 through NUM_CATEGORIES - 1. Inside each category directory will be some number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all of the images in the data directory, where each image is formatted as a numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should be a list of integer labels, representing the categories for each of the corresponding `images`.
    """
    images, labels = [], []

    #--GTSRB folder has 43 subfolders (0-42). os.walk() returns: current_folder_name, subfolders list, files_in_current_folder.
    for path, subfolders, files in os.walk(data_dir):

        #--Get category num from path name:
        #category = re.match('.*?([0-9]+)$', path)
        #label = category.group(1)

        #--Access files within (0-42) folder:
        for file in files:
            if not file.startswith("."): #--Skip ".DS_Store" file:

                #--Read each image as a numpy.ndarray
                img = cv2.imread(os.path.join(path,file))
                #print(img.shape)
                #--Resize img to uniform IMG_WIDTH & IMD_HEIGHT (30x30):
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

                #--Add IMAGE & LABEL to return lists:
                images.append(img)
                labels.append(int(os.path.basename(path)))


    #--Return a tuple processed images/labels:
    return (images, labels)




def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """


    #--Create a TensorFlow Neural Network. Sequential: one layer after another...
    model = tf.keras.models.Sequential([

        #--Convolutional layer: applies a filter to the img to help the NN process it.
        tf.keras.layers.Conv2D(
            #--learn 32 filters, use 3x3 kernel, h•w, RGB=3 channels:
            32, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        #--Max-pooling layer (use 2x2 pool, extract max values to reduce img size):
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        #--2nd Convolutional layer: ...?
        tf.keras.layers.Conv2D(
            32, (3,3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        #--Flatten units:
        tf.keras.layers.Flatten(),

        #--Add (1) hidden layer with dropout (prevent overfitting) (128 units in hidden layer, randomly dropout 0.5 of nodes to generalize fit):
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.33),

        #--Add output layer with output units for all categories (e.g. 43, &c.):
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")

    ])

    #--
    model.compile(
        #--
        optimizer="adam",
        #...
        loss="categorical_crossentropy",
        #...
        metrics=["accuracy"]
    )

    return model








if __name__ == "__main__":
    os.system('reset')
    main()

# Video DEMO
# http://youtu.be/Ry4K1rNVcDE?hd=1
