# Usage: $

# $ pip3 install scikit-learn
import calendar
import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

#--Global Variables
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    #--Split data into input/output sets (training/test data each):
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    #--Train model and make predictions
    model = train_model(X_train, y_train)

    #--Use scikit to make predictions
    predictions = model.predict(X_test)



    #--
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

# <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <> <>



def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    #--Open data from file:
    with open(filename) as file:
        #--Load csv data into a reader:
        reader = csv.reader(file)


        #--Skip header row:
        headers = next(reader)
        #--A list of all the col headings to match to data cols:
        headings = {} # {col-index:heading,}
        for heading, i in enumerate(headers[:17]):
            headings[heading] = i
#        print(">>>", headings)
        #--Dictionary of month_abbrs and indices as values:
        monthcast = {month: index for index, month in enumerate(calendar.month_abbr) if month}

        #--Two master-lists containing evidence/labels for data
        evidence, labels = [], []
        c=0
        for row in reader:
            #--Add an evidence sublist per row of data:
            evidencerow = evidencer(row[:17], headings, monthcast)
            evidence.append(evidencerow)
                #
            #--Add a label sublist per row of data:
            labelrow = labeler(row[-1])
            labels.append(labelrow)

        #--Add evidence/labels master-lists to a tuple:
        data = (evidence, labels) # tuple()
        #
        #
        #
        return data


def evidencer(data, headings, monthcast):
    """
    Takes data row and a dictionary of index:headings to clean up data. Returns a (sub)list of all-numeric data, per data row.
    """
    #--Headings and how to cast the value (int, float, or special):
    intcast = ["Administrative", "Informational", "ProductRelated", "OperatingSystems", "Browser", "Region", "TrafficType"]
    floatcast = ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]
    #--Specials = Visitor_Type, Weekend, Month
    clean = []
    for i, d in enumerate(data):
        name = headings[i]
        #
        if name in intcast:
            clean.append(int(d))
        #
        elif name in floatcast:
            clean.append(float(d))
        #--Change month abbrs to nums (but 0-indexed)
        elif name == "Month":
            if d == "June": # not properly abbrv. as JUN
                clean.append(4)
            else:
                clean.append(monthcast[d] - 1)
        #
        elif name == "Weekend" or name == "VisitorType":
            if d == "TRUE" or "Returning_Visitor":
                clean.append(1)
            elif d == "FALSE" or "New_Visitor":
                clean.append(0)
            else:
                raise Exception("Weekend/VisitorType data incorrectly entered.")
        #
        else:
            raise Exception("Data row's cols are incorrectly formatted.")
    #
    #
    #--Returns a list of all numeric data to sublist in 'evidence' list
    return clean














def labeler(datum):
    """
    Turns 18th data row (Revenue = TRUE/FALSE) into 1/TRUE (bought) and 0/FALSE (did not buy).
    """
    if datum == "TRUE":
        return 1 #--Revenue > $0, made a purchase
    elif datum == "FALSE":
        return 0 # No purchase made...
    else:
        raise Exception("Revenue datum incorrect form, must be 'TRUE' or 'FALSE'.")
# # # # # # # # # #















def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a fitted k-nearest neighbor model (k=1) trained on the data.
    • K-Nearest Neighbors Classification: the data pt. in question is predicted using the k-nearest neighbors (eg if the 3 nearest dots to the unknown are blue, it is predicted to be blue as well).
    """
    #--Nearest neighbors, 'k':
    k = 1

    #--SET-UP K-Neighbors Classification model (imported):
    model = KNeighborsClassifier(n_neighbors=k)

    #--FIT training data [evidence] [list] to model
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels, return a tuple (sensitivity, specificty). Assume each label is either a 1 (positive) or 0 (negative).

    - `sensitivity` should be a floating-point value from 0 to 1 representing the "true positive rate": the proportion of actual positive labels that were accurately identified.

    - `specificity` should be a floating-point value from 0 to 1 representing the "true negative rate": the proportion of actual negative labels that were accurately identified.
    """
    #--Evaluation measures:
    sensitivity, sens_total = 0.0, 0 # TRUE POS RATE, POS RATE TOTAL
    specificity, spec_total = 0.0, 0 # TRUE NEG RATE, NEG RATE TOTAL

    #--Ziploop actuals/predictions:
    for actual, predict in zip(labels, predictions):
        if actual == 1: #--Check if Actual is +/- Rate
            sens_total += 1 #--Sum + 1
            if actual == predict: #--If actual == predicted,
                sensitivity +=1 #--add to the proportion rate too
        elif actual == 0:
            spec_total += 1
            if actual == predict:
                specificity += 1
        else:
            raise Exception("Improper Revenue/label value")


    #--Get sens/spec values based on proportion to all data:
    #--Proportion sens/spec:
    sensitivity /= sens_total
    specificity /= spec_total # e.g. 9/10 = 0.9, or 90%

    #--Tuple the outputs:
    eval = (sensitivity, specificity)
    return eval



if __name__ == "__main__":
    main()
