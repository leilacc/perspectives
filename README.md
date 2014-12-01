Perspectives
============

### Al Jazeera Canvas #MediaInContext Hack

#### Problem

Many people only read one or two articles about any given news story.
But different articles can portray the same event in slightly or very 
different ways. The reader's point of view can be shaped by the connotations of the words the author chooses, and the inclusion/exclusion of certain facts, influenced by the author's inherent conscious or subconscious biases.
For example, one news platform might reference "freedom fighter" while another references "terrorist".
In extreme cases, 2 articles on the same topic can have completely contradictory headlines:
see [ICC rejects pro-Turkey war crimes allegations against IDF in Gaza flotilla raid](http://jpost.com/Israel-News/ICC-rejects-pro-Turkey-war-crimes-allegations-against-IDF-in-Gaza-flotilla-raid-380955) and [IHH: ICC finds Israel guilty of ‘war crimes’ in Mavi Marmara raid](http://www.todayszaman.com/diplomacy_ihh-icc-finds-israel-guilty-of-war-crimes-in-mavi-marmara-raid_363650.html).

#### Solution

With Perspectives, our goal is to promote the awareness of multiple perspectives
on newsworthy content.
We want to equip everyday media consumers - people like you and me and my mom - with as many versions of the 'truth' as possible,
enabling them to come to their own conclusions about what's happening in the world.

Perspectives is a Chrome extension that allows news readers to seamlessly discover alternative accounts of any article they read online
(although currently limited to 4 news organizations, we plan to expand to include as many organizations as possible).
Through the extension, the reader is shown facts taken from other articles.
These facts are specifically chosen to have different words, phrases, and
information than the article that was originally being read.

Pulling related articles from several other news organizations allows
Perspecitves to show all the information that
any single article may have missed. Readers can immerse themselves in many different
points of view, and, in the process, become better armed to identify media bias in all forms.

#### Technical details

When a reader opens a news article webpage, Perspectives determines the article's
main topics by extracting key words from the headline.
These key words are used to find similar articles posted by other news organizations
by querying their web APIs, if available, or by scraping other news sites.
We do a semantic differential analysis between the original article and these
alternate articles using natural language processing tools like NLTK and Wordnet.
We identify and display the largest semantic differences in the alternate articles.

Planned next steps include integrating more APIs, and supplementing official news articles
with high quality social media news/opinions (ie Twitter).

#### Fin

In the U.S. the Pew Research Center found that believability ratings for news outlets is at its lowest in at least 30 years. Our project raises the credibility of ALL news sources, by offering a more transparent viewer interaction with them. We hope that a tool like this can legitimize and humanize people who have different backgrounds and viewpoints than ourselves.
