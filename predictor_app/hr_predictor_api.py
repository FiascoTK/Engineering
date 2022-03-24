import pickle as pkl
import numpy as np

with open("./models/batting.pkl", "rb") as f:
    lr_model = pkl.load(f)
feature_names = lr_model.feature_names

def make_prediction(feature_dict):
    x_input = []
    for name in lr_model.feature_names:
        x_input_ = int(feature_dict.get(name, 0))
        x_input.append(x_input_)

    hr_pred = round(lr_model.predict([x_input])[0], 2)

    return (x_input, hr_pred)
