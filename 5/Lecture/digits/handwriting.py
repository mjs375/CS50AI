import sys
import tensorflow as tf

# Use MNIST handwriting dataset
    #--TS has built-in datasets: e.g. samples of handwritten digits
mnist = tf.keras.datasets.mnist

# Prepare data for training (re-shaping...)
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0 # divide color by 255 to get 0-1 range
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)
x_train = x_train.reshape(
    x_train.shape[0], x_train.shape[1], x_train.shape[2], 1
)
x_test = x_test.reshape(
    x_test.shape[0], x_test.shape[1], x_test.shape[2], 1
)




# Create a convolutional neural network (CNN)
model = tf.keras.models.Sequential([
    #--A list of all the layers wanted:

    # Convolutional layer. Learn 32 filters using a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(28, 28, 1)
    ), #28x28 pixel grid (each image), 1 channel value (B/W only, no color: RGB might be 3...)

    # Max-pooling layer, using 2x2 pool size
        #--look at 2x2 regions and extract max values (reducing SIZE):
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout
    tf.keras.layers.Dense(128, activation="relu"), #128 units in hidden layer
    tf.keras.layers.Dropout(0.5), #prevent overfitting (randomly dropout half of the nodes...)

    # Add an output layer with output units for all 10 digits
    tf.keras.layers.Dense(10, activation="softmax")
        #--softmax act. function: turns output into a probability distribution...
])

# Train neural network
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model.fit(x_train, y_train, epochs=10)

# Evaluate neural network performance
model.evaluate(x_test,  y_test, verbose=2)

# Save model to file
if len(sys.argv) == 2:
    filename = sys.argv[1]
    model.save(filename) # SAVE THE MODEL (don't retrain... takes too long!)
    print(f"Model saved to {filename}.")
