import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load previously saved result
file_path = "Negative_Verbatim_Final_NoMisc.xlsx"
result_df = pd.read_excel(file_path, sheet_name="All Negative Phrases")

# Prepare data: phrases and their counts
phrase_counts = result_df.groupby("Phrase")["Count"].sum().to_dict()

# Generate Word Cloud
wordcloud = WordCloud(width=1400, height=800, background_color='white',
                      colormap='Reds', prefer_horizontal=1.0).generate_from_frequencies(phrase_counts)

# Plot Word Cloud
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Negative Verbatim Word Cloud (Filtered Phrases Only)", fontsize=20)
plt.show()
