import os
import sklearn

from joblib import load

import pandas as pd


def make_prediction(test):
    mnb_model = load("./static/model/model.joblib")
    vect = load("./static/model/vectorizer.joblib")
    column_names = test[0]
    data = test[1:]

    data = pd.DataFrame(data, columns=column_names)

    data.dropna(axis='rows', inplace=True)
    X = vect.transform(data.text)
    output = mnb_model.predict(X)

    data['Predictions'] = output
    data['Predictions'] = data['Predictions'].replace(0, "Not Disaster!")
    data['Predictions'] = data['Predictions'].replace(1, "Disaster!")

    html_table = data.to_html(index=False, classes="table table-striped")
    return html_table, data
