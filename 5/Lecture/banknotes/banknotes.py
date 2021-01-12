import csv
import tensorflow as tf

from sklearn.model_selection import train_test_split

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a neural network (Tensorflow)
model = tf.keras.models.Sequential()
    #--Sequential Neural Network: one layer after another...

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))
    #--Dense Layer: each node is connected to each node in the previous layer
    #--Hidden layer w/ 8 artificial neurons
    #--Input shape: input has 4 values, so 4
    #--Activation function: Relu

# Add output layer with 1 unit, with sigmoid activation
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))
    #--1 unit in the output (Counterfeit v. authenticate)
    #--Sigmoid: S-shaped curve (gives probability of counterfeit/authentic)

# Train neural network
    #--Define the model
model.compile(
    optimizer="adam", #--optimization algorithms
    loss="binary_crossentropy",
    metrics=["accuracy"] #--evaluation metric (we care about accuracy)
)
#--TRAIN the neural network
    #--go thru each dataset 20 epochs (times)...
model.fit(X_training, y_training, epochs=20)

# Evaluate how well model performs
model.evaluate(X_testing, y_testing, verbose=2)
    #--Test the model on the test_data... how accurate?



#
