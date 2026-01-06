import json
import matplotlib.pyplot as plt
import pandas as pd

with open("../data/raw/intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mood_intents = ['depressed', 'suicidal', 'angry', 'happy', 'sad', 'anxious', 'lonely', 'stressed', 'good', 'neutral']

mood_counts = {}
for item in data["intents"]:
    tag = item["tag"].lower()
    if tag in mood_intents:
        mood_counts[tag] = len([p for p in item["patterns"] if p.strip()])

mood_series = pd.Series(mood_counts).sort_values(ascending=True)  # Sort for horizontal bars (lowest at top)

plt.figure(figsize=(10, 8))

bars = plt.barh(mood_series.index, mood_series.values, color='#ff4081', height=0.7, edgecolor='none')

from matplotlib.patches import Rectangle

for bar in bars:
    width = bar.get_width()
    height = bar.get_height()
    y = bar.get_y()


    left_cap = Rectangle((0, y), width=0, height=height, facecolor='#ff4081', edgecolor='none', clip_on=False)
    right_cap = Rectangle((width, y), width=0, height=height, facecolor='#ff4081', edgecolor='none', clip_on=False)

    plt.gca().add_patch(left_cap)
    plt.gca().add_patch(right_cap)

plt.title("Frequency of Mood-Related User Messages", fontsize=18, fontweight='bold', pad=30)
plt.xlabel("Number of Messages", fontsize=14, labelpad=15)
plt.ylabel("Mood Intent", fontsize=14, labelpad=15)

plt.xticks(range(0, mood_series.max() + 2, max(1, mood_series.max() // 10)))

for i, value in enumerate(mood_series.values):
    plt.text(value + mood_series.max() * 0.01, mood_series.index[i], f'{value}',
             va='center', fontweight='bold', fontsize=12, color='black')

# Clean layout
plt.tight_layout()
plt.show()