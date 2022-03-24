from flask import Flask
from flask import request, render_template
from hr_predictor_api import make_prediction, feature_names


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"]) # predit page
def predict():
    x_input, predictions = make_prediction(request.args)
    return render_template('HRpredict.html',
                            feature_names = feature_names,
                            x_input=x_input,
                            prediction = predictions
                            )


if __name__ == '__main__':
    app.run(debug=True)
