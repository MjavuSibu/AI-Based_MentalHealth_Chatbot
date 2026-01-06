from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_models(texts, labels):
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 3))
    X = vectorizer.fit_transform(texts)

    nb = MultinomialNB()
    rf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)

    nb.fit(X, labels)
    rf.fit(X, labels)

    nb_acc = accuracy_score(labels, nb.predict(X))
    rf_acc = accuracy_score(labels, rf.predict(X))

    print(f"Naive Bayes accuracy  : {nb_acc:.3f}")
    print(f"Random Forest accuracy: {rf_acc:.3f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    joblib.dump(nb, "models/nb_model.pkl")
    joblib.dump(rf, "models/rf_model.pkl")

    return vectorizer, nb, rf