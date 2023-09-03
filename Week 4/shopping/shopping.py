import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    # print(evidence)
    # print("\n")
    # print(labels)
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


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
    #create a month dict
    month_dict = {
        "Jan" : 1,
        "Feb" : 2,
        "Mar" : 3,
        "Apr" : 4,
        "May" : 5,
        "June" : 6,
        "Jul" : 7,
        "Aug" : 8,
        "Sep" : 9,
        "Oct" : 10,
        "Nov" : 11,
        "Dec" : 12
    }

    vt_dict = {
        "Returning_Visitor" : 1,
        "New_Visitor" : 0,
        "Other" : 0
    }

    weekend_dict = {
        "FALSE" : 0,
        "TRUE" : 1
    }

    revenue_dict = {
        "FALSE" : 0,
        "TRUE" : 1
    }

    # open the file and assign the data to a dictionary
    with open(filename) as f:
        data = csv.DictReader(f)

        # Initiate evidence & label lists
        evidence = []
        labels = []

        #Iterate every row in the data dict, massage each collumn accordingly & add to lists
        for row in data:
            e_item = [
                int(row["Administrative"]), \
                float(row["Administrative_Duration"]),\
                int(row["Informational"]),\
                float(row["Informational_Duration"]),\
                int(row["ProductRelated"]),\
                float(row["ProductRelated_Duration"]),\
                float(row["BounceRates"]),\
                float(row["ExitRates"]),\
                float(row["PageValues"]),\
                float(row["SpecialDay"]),\
                month_dict[row["Month"]],\
                int(row["OperatingSystems"]),\
                int(row["Browser"]),\
                int(row["Region"]),\
                int(row["TrafficType"]),\
                vt_dict[row["VisitorType"]],\
                weekend_dict[row["Weekend"]],\
            ]
            labels.append(revenue_dict[row["Revenue"]])
            evidence.append(e_item)
        
        return (evidence, labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=12)
    return model.fit(evidence, labels)

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in range(len(labels)):
        if labels[i] == predictions[i] and labels[i] == 1:
            tp += 1
        if labels[i] == predictions[i] and labels[i] == 0:
            tn += 1
        if labels[i] != predictions[i] and predictions[i] == 1:
            fp += 1
        if labels[i] != predictions[i] and predictions[i] == 0:
            fn += 1
    
    return (tp/(tp+fn), tn/(tn+fp))

if __name__ == "__main__":
    main()
