perspectives
============

### Al Jazeera Canvas #MediaInContext Hack

#### Problem

Many people only read one or two articles about any given news story.
But different articles can portray the same event in slightly or very 
different ways. The reader's point of view can be shaped by the connotations of the words the author chooses, and the inclusion/exclusion of certain facts.
For example, one news platform might reference "freedom fighter" while another references "terrorist".
In extreme cases, 2 articles on the same topic can have completely contradictory headlines:
see [ICC rejects pro-Turkey war crimes allegations against IDF in Gaza flotilla raid](http://jpost.com/Israel-News/ICC-rejects-pro-Turkey-war-crimes-allegations-against-IDF-in-Gaza-flotilla-raid-380955) & [IHH: ICC finds Israel guilty of ‘war crimes’ in Mavi Marmara raid](http://www.todayszaman.com/diplomacy_ihh-icc-finds-israel-guilty-of-war-crimes-in-mavi-marmara-raid_363650.html).

#### Solution

With Perspectives, our goal is to promote the awareness of multiple perspectives on newsworthy content. As readers pick their way through the over-saturated world of media, they need help assembling the whole picture. Some differences are reflected in language. . The words that news platforms choose when they report are reflective of their view points and biases. A news headlines might be in passive voice, while another will be in active voice, implicating the participants in an event. Every linguistic decision journalists make when covering events reflect their viewpoints and biases.

To shed light on this topic and attempt to alleviate the bias in news articles, we have introduced a chrome plugin that allows users to discover alternative versions of the current story they are reading. Our tool also allows a user to discover if an article is slanted toward a particular viewpoint.Through the plugin, a user can see alternative articles which have different words, phrases, and information than the one you were reading before. Furthermore, the loaded terms, facts, & viewpoints have been extracted to make it easily accessible. 

The beauty of this application is that it allows the possibility to see what an initial article may have missed. Users can immerse themselves in other perspectives, and, in the process, become better armed to identify bias.In this application, we extract key words and noun phrases from an article a user is reading. We use those key words to query several web APIs and scrape other news sources that may provide alternative views. We do semantic differential analysis using natural language processing tools like NLTK and Wordnet to measure these differences and we deliver you the best results to expand your views. The next steps for our project involved integrating more APIs, supplementing news articles with social media news. 

In the U.S. the Pew Research Center found that believability ratings for news outlets is at its lowest in at least 30 years. Our project raises the credibility of ALL news sources, by offering a more transparent viewer interaction with them. We hope that a tool like this can legitimize and humanize people who have different backgrounds and viewpoints than ourselves.
