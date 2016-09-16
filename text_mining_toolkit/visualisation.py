# module with visualisation functions

# import os for local resources like html templates
import os

# import visualisation modules
import wordcloud
import matplotlib.pyplot as plt

# import modules for d3 graphs
import IPython.core.display
import networkx
import networkx.readwrite.json_graph

# word cloud
def plot_wordcloud(word_count, most_common=None):
    # wordcloud object
    wc = wordcloud.WordCloud(max_words=100, width=1600, height=800, background_color="white", margin=10,
                             prefer_horizontal=1.0)

    # words and plot sizes (word count, relevance, etc)
    words_and_numbers = list(word_count.items())

    wc.generate_from_frequencies(words_and_numbers[:most_common])

    # plot wordcloud
    plt.figure(dpi=300, figsize=(16, 8))
    plt.imshow(wc)
    plt.axis("off")
    pass


# force-directed graph
def plot_force_directed_graph(graph):
    # read html template
    html_template_file = os.path.join(os.path.dirname(__file__), 'html_templates/d3_force_directed_graph_template.html')

    with open(html_template_file, mode='r') as f:
        html = f.read()
        pass

    # display html in notebook cell
    IPython.core.display.display(IPython.core.display.HTML(html))

    pass