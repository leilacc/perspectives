Perspectives
============

### Al Jazeera Canvas #MediaInContext Hack

#### Problem

Many people only read one or two articles about any given news story.
But different articles can portray the same event in slightly or even very 
different ways. The reader's point of view can be influenced by the author's
inherent conscious or subconscious biases, including the connotations of
chosen words and the inclusion/exclusion of certain facts.
For example, one article might reference a "freedom fighter", connoting a
sort of goodness, while another references "terrorist".
In extreme cases, two articles on the same topic can have completely contradictory headlines:
see [ICC rejects pro-Turkey war crimes allegations against IDF in Gaza flotilla raid](http://jpost.com/Israel-News/ICC-rejects-pro-Turkey-war-crimes-allegations-against-IDF-in-Gaza-flotilla-raid-380955) and [IHH: ICC finds Israel guilty of ‘war crimes’ in Mavi Marmara raid](http://www.todayszaman.com/diplomacy_ihh-icc-finds-israel-guilty-of-war-crimes-in-mavi-marmara-raid_363650.html).

#### Solution

With Perspectives, our goal is to promote the awareness of multiple perspectives
on newsworthy events.
We want to equip everyday media consumers - people like you, and me, and your mom - with as many versions of the 'truth' as possible,
enabling them to come to their own conclusions about what's really happening in the world.

Perspectives is a Chrome extension that allows news readers to seamlessly discover alternate accounts of any article they read online
(although currently limited to 4 news organizations, we plan to expand to include as many organizations as possible).
Through the extension, the reader is shown facts taken from other articles.
These facts are specifically chosen to contain words, phrases, and
information that are different from the article that was originally being read.

Pulling related articles from several other news organizations allows
Perspecitves to show information that
any single article may have missed. Readers can immerse themselves in many different
points of view, becoming better informed about current events while
simultaneously becoming better equipped to identify media bias in all shapes and sizes.

#### Technical details

When a reader opens a news article webpage, Perspectives determines the article's
main topics by extracting key words from the headline.
These key words are used to find similar articles posted by other news organizations
by querying their web APIs, if available, or by scraping other news sites.
We do a semantic differential analysis between the original article and these
alternate articles using natural language processing tools like NLTK and WordNet.
We identify and display the largest semantic differences that were found in the alternate articles.

Planned next steps include integrating more news APIs, and supplementing these official news articles
with high quality social media news/opinions (ie Twitter).

#### Fin

In the U.S. the Pew Research Center found that believability ratings for news outlets is at its lowest in at least 30 years. Our project raises the credibility of _all_ news sources, by offering more transparent interactions with them. We hope that a tool like this can legitimize and humanize people who have different backgrounds and viewpoints than ourselves.

Created by: Jelle Akkerman, Zahra Parnia Ashktorab, Jackie Hurwitz, and Leila Chan Currie
