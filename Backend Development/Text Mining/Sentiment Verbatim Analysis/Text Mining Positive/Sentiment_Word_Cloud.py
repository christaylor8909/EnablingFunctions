import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from textblob import TextBlob
import nltk

nltk.download('punkt')
nltk.download('stopwords')

file_path = r"C:\Users\t0355lp\.vscode\Python\InterviewSummaryData.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

df.columns = df.columns.map(lambda x: str(x).strip().replace('\u00A0', '').replace('\n', '').lower())

print("✅ Available columns:")
print(df.columns.tolist())

verbatim_column = "q20 - final verbatim"

text_data = df[verbatim_column].dropna().astype(str)

combined_text = " ".join(text_data).lower()
combined_text = re.sub(r'[^\w\s]', '', combined_text)

tokens = word_tokenize(combined_text)

stop_words = set(stopwords.words('english'))
custom_stopwords = set([
    'car', 'service', 'vehicle', 'staff', 'time', 'jeep', 'customer', 'done', 'work', 'back', 'get', 'would', 'also', 'one', 'could',
    'still', 'issue', 'problem', 'call', 'told', 'waiting', 'parts', 'warranty', 'cost', 'price', 'fix', 'repair', 'replacement',
    'said', 'asked', 'came', 'good', 'happy', 'great', 'excellent', 'satisfied',
    'thanks', 'thank', 'year', 'years', 'two', 'old', 'grand', 'cherokee', 'media', 'social', 'job', 'team', 'last', 'first'
])
all_stopwords = stop_words.union(custom_stopwords)

filtered_tokens = [word for word in tokens if word not in all_stopwords]

bigram_list = list(ngrams(filtered_tokens, 2))
bigram_phrases = [' '.join(bigram) for bigram in bigram_list]

positive_action_phrases = []
for phrase in bigram_phrases:
    polarity = TextBlob(phrase).sentiment.polarity
    if polarity > 0:
        # Only keep phrases that look like service actions
        if any(action in phrase for action in ["explained", "helpful", "friendly", "quick", "efficient", "courteous", "easy", "called", "available", "booked", "resolved", "fixed", "assisted", "organised", "professional", "informed", "checked", "collected", "ready", "diagnosed", "prepared"]):
            positive_action_phrases.append(phrase)

phrase_freq = {}
for phrase in positive_action_phrases:
    phrase_freq[phrase] = phrase_freq.get(phrase, 0) + 1

wc = WordCloud(width=1000, height=600, background_color='white', colormap='Greens').generate_from_frequencies(phrase_freq)

plt.figure(figsize=(15, 7))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("Positive Service Action Phrases (Business Insight Focused)")
plt.show()
