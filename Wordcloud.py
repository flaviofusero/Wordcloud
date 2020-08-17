# Creates a masked wordcloud from an exported WhatsApp chat
from wordcloud import WordCloud, STOPWORDS
# For stopwords in another language:
# from stop_words import get_stop_words
import numpy as np
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# Defines plotting function for the wordcloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off");

# Defines stopwords adding custom stopwords to the default list
# I added "Media omessi" since this is going to appear every time a media was removed from the WhatsApp exported chat
# Since it's just noise, we don't want to include it in the wordcloud
my_stopwords = STOPWORDS.union({"media", "omessi"})

# Import image to np.array
mask = np.array(Image.open('C:\\Users\\flavi\\Desktop\\Scripts\\Wordcloud\\whatsapp.png'))+255

# Creates the wordcloud
wordcloud = WordCloud(width = 3000,
                      height = 2000,
                      stopwords = my_stopwords,
                      background_color="white",
                      max_words=220,
                      mask=mask)

# Imports the file
df = pd.read_csv("C:\\Users\\flavi\\Desktop\\Scripts\\Wordcloud\\Chat WhatsApp con Deutsches Filminstitut.txt",
                 encoding ="utf-8",
                 sep="\n")

## Data preparation
df.columns = ["line"]
# Since every line is now in the format "datetime - author : message", we need to split every line in three columns
df[["datetime", "tmp"]] = df.line.str.split("-", n=1, expand=True)
df[["author", "message"]] = df.tmp.str.split(":", n=1, expand=True)
df = df[["datetime", "author", "message"]]

# Creates the bag of words
messages = df["message"]

# Creates the bag of words for texts sent by a specific person
f_messages = df.loc[df["author"].str.strip() == "flavio"]["message"]
words = ""
for m in messages:
    words += str(m)

# Plots the wordcloud
wordcloud = wordcloud.generate_from_text(words)
plot_cloud(wordcloud)