# python3 banknotes0.py

import csv
import random

from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

#--Which model to use:
# model = Perceptron()
    # => 98.1% accuracy
# model = svm.SVC() #SupportVector Classifier
    # => 100% accurate
# model = KNeighborsClassifier(n_neighbors=1)
    # => 100% accurate
model = GaussianNB()
    # => 82.85-85% accurate

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
        #--4 pieces of evidence per bill
            "evidence": [float(cell) for cell in row[:4]],
        #--Human investigator who decided if counterfeit(1) or not(0)
            "label": "Authentic" if row[4] == "0" else "Counterfeit"
        })

#--Separate data into training and testing groups
holdout = int(0.40 * len(data)) # 40% 'held-out' for testing
random.shuffle(data)
testing = data[:holdout] #
training = data[holdout:] #

# Train model on training set
    #-- x-values are inputs (evidence)
X_training = [row["evidence"] for row in training]
    #-- authentic or counterfeit label
y_training = [row["label"] for row in training]
#--Fit training data [evidence] [list] to model
model.fit(X_training, y_training)



# Make predictions on the testing set
X_testing = [row["evidence"] for row in testing]
    #--ACTUAL values of bill
y_testing = [row["label"] for row in testing]
    #--PREDICTED values of bill (based on model)
predictions = model.predict(X_testing)

# Compute how well we performed
correct = 0
incorrect = 0
total = 0
#--zip lets you run thru 2 lists, side-by-side, at same time:
for actual, predicted in zip(y_testing, predictions):
    total += 1
    #--Does model's predictions match actual labels?
    if actual == predicted: #
        correct += 1
    else:
        incorrect += 1

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")
