perspectives
============

## Al Jazeera Canvas #MediaInContext Hack

### Problem

Many people in the world today consult a single source on any given news item. Sometimes theadlines for the **same event** from two different news platforms may look like it is about two completely different events. Through the tool we have built, our goal is to promote the awareness of multiple perspectives on newsworthy content. 

As consumers navigate an over-saturated world of media, they need a tool that can give a better sense of the whole picture. News articles present their biases in various ways. Some differences are reflected in language. For example, one news platform might reference "freedom fighter" while another references "terrorist". The words that news platforms choose when they report are reflective of their view points and biases. A news headlines might be in passive voice, while another will be in active voice, implicating the participants in an event. Every linguistic decision journalists make when covering events reflect their viewpoints and biases.

To shed light on this topic and attempt to alleviate the bias in news articles, we have introduced a chrome plugin that allows users to discover alternative versions of the current story they are reading. Our tool also allows a user to discover if an article is slanted toward a particular viewpoint.Through the plugin, a user can see alternative articles which have different words, phrases, and information than the one you were reading before. Furthermore, the loaded terms, facts, & viewpoints have been extracted to make it easily accessible. 

The beauty of this application is that it allows the possibility to see what an initial article may have missed. Users can immerse themselves in other perspectives, and, in the process, become better armed to identify bias.In this application, we extract key words and noun phrases from an article a user is reading. We use those key words to query several web APIs and scrape other news sources that may provide alternative views. We do semantic differential analysis using natural language processing tools like NLTK and Wordnet to measure these differences and we deliver you the best results to expand your views. The next steps for our project involved integrating more APIs, supplementing news articles with social media news. 

In the U.S. the Pew Research Center found that believability ratings for news outlets is at its lowest in at least 30 years. Our project raises the credibility of ALL news sources, by offering a more transparent viewer interaction with them. We hope that a tool like this can legitimize and humanize people who have different backgrounds and viewpoints than ourselves.
