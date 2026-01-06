import json
import matplotlib.pyplot as plt


with open("../data/raw/intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

positive_moods = ['happy', 'good', 'joy', 'excited', 'grateful', 'content', 'relieved']
negative_moods = ['sad', 'depressed', 'anxious', 'stressed', 'angry', 'lonely', 'suicidal', 'self_harm', 'worthless',
                  'hopeless']

positive_count = 0
negative_count = 0
other_count = 0

for item in data["intents"]:
    tag = item["tag"].lower()
    num_patterns = len([p for p in item["patterns"] if p.strip()])

    if tag in positive_moods:
        positive_count += num_patterns
    elif tag in negative_moods:
        negative_count += num_patterns
    else:
        other_count += num_patterns

labels = ['Positive Moods', 'Negative Moods', 'Neutral/Other']
sizes = [positive_count, negative_count, other_count]
colors = ['#a8e6cf', '#ff9999', '#dddddd']  # Soft green, soft red, neutral grey
explode = (0.08, 0.08, 0)  # Slightly more separation for clarity

plt.figure(figsize=(10, 9))

wedges, texts, autotexts = plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    shadow=True,
    textprops={'fontsize': 14},
    pctdistance=0.85  # Moves percentage labels a bit inward to avoid crowding
)

for autotext in autotexts:
    autotext.set_fontsize(15)
    autotext.set_fontweight('bold')
    autotext.set_color('black')


plt.title(" Positive vs Negative Mood Messages in the Dataset",
          fontsize=18, fontweight='bold', pad=40)


plt.legend(
    [f'Positive Moods ({positive_count} messages)',
     f'Negative Moods ({negative_count} messages)',
     f'Neutral/Other ({other_count} messages)'],
    title="Mood Categories",
    loc="right",
    bbox_to_anchor=(1.0, 1.0),
    fontsize=10,
    title_fontsize=13,
    frameon=True,
    fancybox=True,
    shadow=False
)

plt.show()