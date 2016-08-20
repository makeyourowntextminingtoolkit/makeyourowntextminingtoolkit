# module with visualisation functions

# import visualisation modules
import wordcloud
import matplotlib.pyplot as plt

def plot_wordcloud(word_count, most_common=None):
    # wordcloud object
    wc = wordcloud.WordCloud(max_words=100, width=1600, height=800, background_color="white", margin=10,
                             prefer_horizontal=1.0)
    wc.generate_from_frequencies(word_count.most_common(most_common))

    # plot wordcloud
    plt.figure(dpi=300, figsize=(16, 8))
    plt.imshow(wc)
    plt.axis("off")
    pass
