import joblib
import numpy as np

vectorizer = joblib.load("models/vectorizer.pkl")
nb_model = joblib.load("models/nb_model.pkl")
rf_model = joblib.load("models/rf_model.pkl")

def predict_intent(text, use_model="rf"):
    vec = vectorizer.transform([text.lower().strip()])
    if use_model == "nb":
        pred = nb_model.predict(vec)[0]
        conf = np.max(nb_model.predict_proba(vec))
    else:
        pred = rf_model.predict(vec)[0]
        conf = np.max(rf_model.predict_proba(vec))
    return pred, conf