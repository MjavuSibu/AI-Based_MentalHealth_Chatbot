import customtkinter as ctk
from tkinter import END
import numpy as np
import os
import sys
from datetime import datetime
from PIL import Image, ImageSequence

from src.predictor import predict_intent
from src.data_handler import load_intents

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class MentalSparkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MentalSpark")
        self.geometry("500x900")
        self.minsize(400, 700)
        self.maxsize(600, 700)

        _, _, self.responses = load_intents()

        self.animation_id = None

        self.show_onboarding()

    def show_onboarding(self):
        for widget in self.winfo_children():
            widget.destroy()

        onboarding_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        onboarding_frame.pack(fill="both", expand=True)

        try:
            gif_path = "assets/logo.gif"
            gif = Image.open(gif_path)
            frames = []

            for frame in ImageSequence.Iterator(gif):
                photo = ctk.CTkImage(
                    light_image=frame.convert("RGBA"),
                    dark_image=frame.convert("RGBA"),
                    size=(300, 300)
                )
                frames.append(photo)

            logo_label = ctk.CTkLabel(onboarding_frame, text="")
            logo_label.pack(pady=(120, 40))

            def animate(idx=0):
                if idx < len(frames):
                    logo_label.configure(image=frames[idx])
                    delay = gif.info.get('duration', 100)
                    self.animation_id = self.after(delay, animate, (idx + 1) % len(frames))

            animate(0)

        except Exception:
            fallback = ctk.CTkLabel(onboarding_frame, text="MentalSpark",
                                    font=ctk.CTkFont(size=48, weight="bold"),
                                    text_color="#ff4081")
            fallback.pack(pady=(120, 40))

        tagline_label = ctk.CTkLabel(
            onboarding_frame,
            text="A spark for every mind",
            font=ctk.CTkFont(size=28, slant="italic"),
            text_color="#333333"
        )
        tagline_label.pack(pady=(10, 100))

        start_btn = ctk.CTkButton(
            onboarding_frame,
            text="Get Started",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white",
            fg_color="#ff4081",
            hover_color="#e91e63",
            height=60,
            width=300,
            corner_radius=30,
            command=self.start_chat
        )
        start_btn.pack(pady=20)

    def start_chat(self):
        if self.animation_id is not None:
            self.after_cancel(self.animation_id)
            self.animation_id = None

        for widget in self.winfo_children():
            widget.destroy()

        self.show_main_chat()

    def show_main_chat(self):
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#ffebee")
        main_frame.pack(fill="both", expand=True)

        header = ctk.CTkFrame(main_frame, height=80, corner_radius=0, fg_color="#000000")
        header.pack(fill="x")
        header.pack_propagate(False)

        back_btn = ctk.CTkButton(
            header,
            text="←",
            width=60,
            fg_color="#000000",
            text_color="white",
            hover_color="#ff4081",
            font=ctk.CTkFont(size=18),
            command=self.destroy
        )
        back_btn.pack(side="left", padx=20, pady=15)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", expand=True)

        title = ctk.CTkLabel(
            title_frame,
            text="MentalSpark",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ff4081"
        )
        title.pack()

        settings_btn = ctk.CTkButton(
            header,
            text="⚙️",
            width=60,
            fg_color="#000000",
            text_color="white",
            hover_color="#ff4081",
            font=ctk.CTkFont(size=18),
            command=self.open_settings
        )
        settings_btn.pack(side="right", padx=20, pady=15)

        chat_frame = ctk.CTkFrame(main_frame, corner_radius=0, fg_color="#ffebee")
        chat_frame.pack(fill="both", expand=True)

        self.canvas = ctk.CTkCanvas(chat_frame, highlightthickness=0, bg="#ffebee")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(chat_frame, command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.messages_frame = ctk.CTkFrame(self.canvas, fg_color="#ffebee")
        self.canvas.create_window((0, 0), window=self.messages_frame, anchor="n", width=600)

        self.messages_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.typing_label = ctk.CTkLabel(
            self.messages_frame,
            text="MentalSpark is typing...",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color="#666666",
            fg_color="#f8bbd0",
            corner_radius=18,
            padx=20,
            pady=12
        )

        input_bar = ctk.CTkFrame(main_frame, height=90, corner_radius=0, fg_color="white")
        input_bar.pack(fill="x")
        input_bar.pack_propagate(False)

        self.entry = ctk.CTkEntry(
            input_bar,
            placeholder_text="Type a message...",
            font=ctk.CTkFont(size=16),
            height=55,
            corner_radius=30,
            border_width=3
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=18)
        self.entry.bind("<Return>", self.send_message)
        self.entry.focus()

        send_btn = ctk.CTkButton(
            input_bar,
            text="Send",
            width=80,
            height=55,
            corner_radius=30,
            fg_color="#ff4081",
            hover_color="#e91e63",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.send_message
        )
        send_btn.pack(side="right", padx=(0, 20), pady=18)

        self.daily_check_in()

        self.daily_affirmation()

        self.add_bot_message(
            "Hey! I'm MentalSpark, your personal companion. How are you feeling today? Remember, our chat is anonymous and secure.")

    def daily_check_in(self):
        check_file = "last_check.txt"
        today = datetime.now().strftime("%Y-%m-%d")
        if not os.path.exists(check_file):
            with open(check_file, "w") as f:
                f.write(today)

    def daily_affirmation(self):
        affirmation_file = "last_affirmation.txt"
        today = datetime.now().strftime("%Y-%m-%d")
        affirmations = [
            "You are capable of amazing things.",
            "Your strength is greater than any struggle.",
            "Today is full of possibilities — you’ve got this.",
            "You are worthy of love and kindness — especially from yourself.",
            "Every day you are growing stronger and wiser.",
            "You bring light to the world just by being you.",
            "Progress, not perfection — you're doing better than you think.",
            "Your feelings are valid, and you are never alone.",
            "You have survived 100% of your hardest days — keep going.",
            "Be proud of how far you've come.",
            "You are enough, exactly as you are.",
            "Small steps are still progress.",
            "You deserve peace and happiness.",
            "Your voice matters — speak kindly to yourself.",
            "Today, you choose courage over comfort.",
            "You are resilient, brave, and strong.",
            "Good things are coming — trust the journey.",
            "You are doing your best, and that is enough.",
            "Breathe — you've got this moment.",
            "You are worthy of good things."
        ]
        show_affirmation = False
        if not os.path.exists(affirmation_file):
            show_affirmation = True
            with open(affirmation_file, "w") as f:
                f.write(today)
        else:
            with open(affirmation_file, "r") as f:
                last_date = f.read().strip()
            if last_date != today:
                show_affirmation = True
                with open(affirmation_file, "w") as f:
                    f.write(today)
        if show_affirmation:
            affirmation = np.random.choice(affirmations)
            self.add_bot_message(f" Daily Affirmation \n{affirmation}")

    def save_mood(self, mood):
        mood_file = "mood_history.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(mood_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - Feeling: {mood}\n")

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.resizable(False, False)
        settings_window.transient(self)
        settings_window.grab_set()
        title = ctk.CTkLabel(settings_window, text="Settings", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        theme_frame = ctk.CTkFrame(settings_window)
        theme_frame.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(theme_frame, text="Appearance", font=ctk.CTkFont(size=16)).pack(anchor="w", padx=20, pady=10)
        theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode" if ctk.get_appearance_mode() == "Light" else "Light Mode",
            command=lambda: self.fake_toggle(theme_switch)
        )
        theme_switch.pack(anchor="w", padx=40)
        if ctk.get_appearance_mode() == "Dark":
            theme_switch.select()
        ctk.CTkButton(
            settings_window,
            text="Clear Chat History",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.clear_chat
        ).pack(pady=20, ipadx=20, ipady=10)
        ctk.CTkButton(
            settings_window,
            text="View Mood History",
            command=self.view_mood_history
        ).pack(pady=10, ipadx=20, ipady=10)
        ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy
        ).pack(pady=30)

    def fake_toggle(self, switch):
        if switch.cget("text") == "Dark Mode":
            switch.configure(text="Light Mode")
        else:
            switch.configure(text="Dark Mode")
        self.add_bot_message("Theme changes take effect when you restart the app!")

    def clear_chat(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        self.add_bot_message("Chat cleared. Ready for a fresh start whenever you are.")

    def view_mood_history(self):
        mood_file = "mood_history.txt"
        if os.path.exists(mood_file):
            os.startfile(mood_file)
        else:
            self.add_bot_message("No mood history yet — start chatting and I'll keep track!")

    def add_user_message(self, text):
        user_container = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        user_container.pack(anchor="e", padx=20, pady=3)
        name_label = ctk.CTkLabel(
            user_container,
            text="You",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        name_label.pack(anchor="e")
        bubble = ctk.CTkLabel(
            user_container,
            text=text,
            wraplength=360,
            fg_color="#ff4081",
            text_color="white",
            corner_radius=22,
            padx=18,
            pady=12,
            font=ctk.CTkFont(size=15),
            justify="right"
        )
        bubble.pack(anchor="e")
        self.scroll_to_bottom()

    def add_bot_message(self, text):
        bot_container = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        bot_container.pack(anchor="w", padx=20, pady=3)
        name_label = ctk.CTkLabel(
            bot_container,
            text="MentalSpark",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        name_label.pack(anchor="w")
        bubble = ctk.CTkLabel(
            bot_container,
            text=text,
            wraplength=360,
            fg_color="#f0f0f0",
            text_color="black",
            corner_radius=22,
            padx=18,
            pady=12,
            font=ctk.CTkFont(size=15),
            justify="left"
        )
        bubble.pack(anchor="w")
        self.scroll_to_bottom()

    def show_typing(self):
        try:
            if not self.typing_label.winfo_viewable():
                self.typing_label.pack(anchor="w", padx=20, pady=3)
                self.scroll_to_bottom()
        except:
            pass

    def hide_typing(self):
        try:
            self.typing_label.pack_forget()
        except:
            pass

    def scroll_to_bottom(self):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.add_user_message(msg)
        self.entry.delete(0, END)
        self.show_typing()
        crisis_keywords = ["suicide", "kill myself", "end my life", "hurt myself", "don't want to live", "want to die"]
        if any(keyword in msg.lower() for keyword in crisis_keywords):
            crisis_reply = (
                "I'm really worried about you right now. Your life matters.\n\n"
                "Please reach out for immediate help:\n"
                "• SADAG 24hr Helpline: 0800 567 567\n"
                "• Suicide Crisis Line: 0800 567 567\n\n"
                "You are not alone — someone is waiting to help you right now."
            )
            self.after(800, lambda: [self.hide_typing(), self.add_bot_message(crisis_reply)])
            return
        mood_keywords = {
            "happy": ["happy", "good", "great", "awesome", "feeling good", "im good"],
            "okay": ["okay", "fine", "alright"],
            "sad": ["sad", "down", "depressed", "low"],
            "anxious": ["anxious", "worried", "stressed", "nervous"],
            "angry": ["angry", "mad", "frustrated"]
        }
        detected_mood = None
        for mood, keywords in mood_keywords.items():
            if any(word in msg.lower() for word in keywords):
                detected_mood = mood
                break
        if detected_mood:
            self.save_mood(detected_mood.capitalize())
        intent, confidence = predict_intent(msg, use_model="rf")
        reply_list = self.responses.get(intent, [
            "I'm glad to hear that! What's making you feel good today?",
            "Thanks for sharing! How can I support you right now?",
            "I hear you. What's on your mind?",
            "That sounds like a lot. Want to talk more about it?",
            "I'm here for you. How can I help?"
        ])
        reply = np.random.choice(reply_list)
        self.after(1500, lambda: [self.hide_typing(), self.add_bot_message(reply)])

if __name__ == "__main__":
    app = MentalSparkApp()
    app.mainloop()