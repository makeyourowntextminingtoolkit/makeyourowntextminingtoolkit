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
def plot_force_directed_graph(words_by_co_occurance):
    # convert words_by_co_occurance to graph
    graph = networkx.from_pandas_dataframe(words_by_co_occurance, 'word1', 'word2', 'weight')

    # d3 library url
    d3_url = "https://d3js.org/d3.v4.min.js"

    # read html template
    html_template_file = os.path.join(os.path.dirname(__file__), 'html_templates/d3_force_directed_graph.html')
    with open(html_template_file, mode='r') as f:
        html = f.read()
        pass

    # read javascript template
    js_template_file = os.path.join(os.path.dirname(__file__), 'html_templates/d3_force_directed_graph.js')
    with open(js_template_file, mode='r') as f:
        js = f.read()
        pass

    #print(str(networkx.readwrite.json_graph.node_link_data(graph)))

    # substitute links and data
    html = html.replace('%%links%%', str(networkx.readwrite.json_graph.node_link_data(graph)))
    html = html.replace('%%nodes%%', str(networkx.readwrite.json_graph.node_link_data(graph)))
    #print(html)

    # display html in notebook cell
    IPython.core.display.display_html(IPython.core.display.HTML(html))
    # display (run) javascript in notebook cell
    IPython.core.display.display_javascript(IPython.core.display.Javascript(data=js, lib=d3_url))
    pass