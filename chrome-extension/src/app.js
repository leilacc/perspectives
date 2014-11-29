if (!hookElem) {
    var hookElem = document.createElement("div");
    hookElem.setAttribute("id", "react-hook");
    document.body.appendChild(hookElem);
}

var calculateOffsetTop = function(elem) {
    var rect = elem.getBoundingClientRect()
    return [rect.top + document.body.scrollTop, rect.left + document.body.scrollLeft]
}


var datata = [{title:"Americans in Israel Try to Adjust to Life in a Conflict Zone", source: "Vocative", url:"http://www.vocativ.com/world/israel-world/americans-israel-try-adjust-life-conflict-zone/"},
            {title:"Israel's Iron Dome is Amazing, and That's a Problem", source:"Businessweek", url:"http://www.businessweek.com/articles/2014-07-11/israels-iron-dome-is-amazing-and-thats-a-problem"},
            {title:"Gaza Rocket Hits Ashdod Gas Station, One Seriously Injured", source:"Jerusalem Post", url:"http://www.jpost.com/National-News/Rocket-hits-Ashdod-gas-station-362369"},
            {source:"USA Today", title:"Israel Vows to Continue Airstrikes Despite Growing Pressure", url:"http://www.usatoday.com/story/news/world/2014/07/11/israel-gaza-hamas-palestinians/12511497/"},
            {title:"Turkey Says Israel's Gaza Offensive Threatens Rapprochement", source:"Jerusalem Post", url:"http://www.jpost.com/Operation-Protective-Edge/Turkey-says-Israels-Gaza-offensive-threatens-rapprochement-362420"}
             ];

var Article = React.createClass({
  goto: function () {
      console.log(this.props.url);
  },
  render: function() {
    return (
            <section style={{paddingLeft: this.props.offset}} onClick={this.goto}>
                <h1 className="source react">{this.props.source}</h1>
                <h1 className="react">{this.props.title}</h1>
            </section>
    );
  }
});

var Main = React.createClass({
  nthBlock: 0,
  titleOffset: undefined,
  componentWillMount: function() {
    var pageTitle = document.body.querySelector('h1')
    pageTitle.scrollIntoViewIfNeeded(true)
    this.titleOffset = calculateOffsetTop(pageTitle)
    this.nthBlock = Math.ceil(this.titleOffset[0] / (window.innerHeight / 6))
  },
  render: function(){
      var offsetLeft = this.titleOffset[1]
      var articles = datata.map(function (d) {
        return (
                <Article offset={offsetLeft} title={d.title} source={d.source} url={d.url}/>
        );
      });
      articles.splice([this.nthBlock - 1], 0, <div className="black"></div>)
      return (
        <div>
          {articles}
        </div>)
  }})

React.render(
        <Main />,
        document.getElementById('react-hook')
      );
