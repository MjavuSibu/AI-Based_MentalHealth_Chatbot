from src.trainer import train_models
from src.data_handler import load_intents

if __name__ == "__main__":
    print("Training models...")
    texts, labels, _ = load_intents()
    train_models(texts, labels)
    print("Models trained and saved!")

    from src.ui.chatbot import MentalSparkApp
    app = MentalSparkApp()
    app.mainloop()