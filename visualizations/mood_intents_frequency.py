import json
import matplotlib.pyplot as plt
import pandas as pd


with open("../data/raw/intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mood_intents = ['depressed', 'suicidal', 'angry', 'happy', 'sad', 'anxious', 'lonely', 'stressed', 'good', 'neutral']  # Add/remove based on your intents.json

mood_counts = {}
for item in data["intents"]:
    tag = item["tag"]
    if tag in mood_intents:
        mood_counts[tag] = len([p for p in item["patterns"] if p.strip()])

mood_series = pd.Series(mood_counts).sort_values(ascending=False)

plt.figure(figsize=(11, 7))
colors = plt.cm.Set2(range(len(mood_series)))

bars = plt.bar(mood_series.index, mood_series.values, color=colors, edgecolor='black', linewidth=1.5)

plt.title("Frequency of Mood-Related User Intents", fontsize=18, fontweight='bold', pad=30)
plt.xlabel("Mood Intent", fontsize=14, labelpad=15)
plt.ylabel("Number of Messages", fontsize=14, labelpad=15)
plt.xticks(rotation=45, ha='right', fontsize=12)

plt.yticks(range(0, mood_series.max() + 2, max(1, mood_series.max() // 10)))

for bar in bars:
    height = int(bar.get_height())
    plt.text(bar.get_x() + bar.get_width()/2., height + mood_series.max()*0.01,
             f'{height}', ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.show()