This folder can contain dictionaries.

It is not intended that they will all be located on github as some will have license or usage restrictions which means
you will need to download them yourself. In this case, links will be provided.

Most unix-like systems have a simple dictionary in /use/share/dict/words

You can also download customised dictionaries from aspell http://app.aspell.net/create


words.txt
=========
The one included here is from aspell.net and configured according to the README file (which is required to be included
with the text). It has the following steps of processing applied:

 * remove 's from the end of any word
 * lowercase all text
 * remove duplicates

 This list is useful because
it also contains real proper names such as Stephens, and major place names like Sheffield.