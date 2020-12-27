from model import model # Our model in model.py

# Calculate predictions
predictions = model.predict_proba({
    # "rain": "heavy", #Adding this in as evidence shouldn't change the appt attend/miss prob, since that is only directly based on the train being delayed or not (it will change track maintenance, &c. though)
    "train": "delayed" # Our evidence: train is delayed in this situation
})

# Print predictions for each node
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")
