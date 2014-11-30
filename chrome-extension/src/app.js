if (!hookElem) {
    var hookElem = document.createElement("div");
    hookElem.setAttribute("id", "react-hook");
    document.body.appendChild(hookElem);
}

var calculateOffset = function(elem) {
    var rect = elem.getBoundingClientRect()
    return rect.left + document.body.scrollLeft
}

var datata = [{title:"Americans in Israel Try to Adjust to Life in a Conflict Zone", source: "Vocative", url:"http://www.vocativ.com/world/israel-world/americans-israel-try-adjust-life-conflict-zone/"},
            {title:"Israel's Iron Dome is Amazing, and That's a Problem", source:"Businessweek", url:"http://www.businessweek.com/articles/2014-07-11/israels-iron-dome-is-amazing-and-thats-a-problem"},
            {title:"Gaza Rocket Hits Ashdod Gas Station, One Seriously Injured", source:"Jerusalem Post", url:"http://www.jpost.com/National-News/Rocket-hits-Ashdod-gas-station-362369"},
            {source:"USA Today", title:"Israel Vows to Continue Airstrikes Despite Growing Pressure", url:"http://www.usatoday.com/story/news/world/2014/07/11/israel-gaza-hamas-palestinians/12511497/"},
              {title:"Turkey Says Israel's Gaza Offensive Threatens Rapprochement", source:"Jerusalem Post", url:"http://www.jpost.com/Operation-Protective-Edge/Turkey-says-Israels-Gaza-offensive-threatens-rapprochement-362420"},
              {title:"Turkey Says Israel's Gaza Offensive Threatens Rapprochement", source:"Jerusalem Post", url:"http://www.jpost.com/Operation-Protective-Edge/Turkey-says-Israels-Gaza-offensive-threatens-rapprochement-362420"},
              {title:"Turkey Says Israel's Gaza Offensive Threatens Rapprochement", source:"Jerusalem Post", url:"http://www.jpost.com/Operation-Protective-Edge/Turkey-says-Israels-Gaza-offensive-threatens-rapprochement-362420"},
            {title:"Turkey Says Israel's Gaza Offensive Threatens Rapprochement", source:"Jerusalem Post", url:"http://www.jpost.com/Operation-Protective-Edge/Turkey-says-Israels-Gaza-offensive-threatens-rapprochement-362420"}
             ];

var Article = React.createClass({
  goto: function () {
      console.log(this.props.url);
  },
  componentDidMount: function () {
      Velocity(this.getDOMNode(), {translateX: "0px"}, {duration:200, delay: 150*this.props.num, easing:"ease-out"})
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
  origFontColor: undefined,
  getInitialState: function() {
      return {loading: true,
              data: []};
  },
  hideExt: function() {
      chrome.browserAction.disable()
  },
  componentDidMount: function(){
      Velocity(document.body.querySelector("#Shape"), {rotateZ: "360deg"}, {loop: true, duration: 2000, easing: "easeInOutQuint"})
      var self = this;
      setTimeout(function(){
        self.setState({loading: false,
                       data: datata});},3000);
  },
  componentWillMount: function() {
    var pageTitle = document.body.querySelector('h1')
    pageTitle = document.body.querySelector('h1')
    this.titleOffset = calculateOffset(pageTitle)
    Velocity(pageTitle ,"scroll", { duration: 1500, easing: "spring", offset: -30})
  },
  render: function(){
      var offsetLeft = this.titleOffset
      if(this.state.data.length > 0){
          var articles = this.state.data.map(function (d, i) {
          return (
                  <Article num={i} offset={offsetLeft} title={d.title} source={d.source} url={d.url}/>
          );
        });}
      else{
        var articles = <svg className="react-icon-loader" width="128px" height="128px" viewBox="0 0 128 128" version="1.1"><g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g id="icon"><path d="M64,-7.81597009e-14 C28.6520889,-7.81597009e-14 0,28.6520889 0,64 C0,99.3479111 28.6520889,128 64,128 C99.3479111,128 128,99.3479111 128,64 C128,28.6520889 99.3479111,-7.81597009e-14 64,-7.81597009e-14 M64,124.120178 C30.848,124.120178 3.87982222,97.152 3.87982222,64 C3.87982222,30.848 30.848,3.8784 64,3.8784 C97.152,3.8784 124.120178,30.848 124.120178,63.9985778 C124.120178,97.152 97.152,124.120178 64,124.120178" id="Shape-3" fill="#ffffff" ></path><path d="M103.409363,28.7370701 L100.666946,25.9946532 L95.1811063,31.4804926 L97.9235231,34.2229095 L103.409363,28.7370701 L103.409363,28.7370701 Z" fill="#ffffff" ></path><path d="M34.4093626,97.7370701 L31.6669457,94.9946532 L26.1811063,100.480493 L28.9235231,103.22291 L34.4093626,97.7370701 L34.4093626,97.7370701 Z" fill="#ffffff"></path><rect id="Rectangle-path" fill="#ffffff"  x="62.5777778" y="109.511111" width="3.8784" height="7.75822222"></rect><rect id="Rectangle-path" fill="#ffffff"  x="62.5777778" y="11.3777778" width="3.8784" height="7.75822222"></rect><rect id="Rectangle-path" fill="#ffffff"  x="108.088889" y="62.5777778" width="7.75822222" height="3.8784"></rect><rect id="Rectangle-path" fill="#ffffff"  x="11.3777778" y="62.5777778" width="7.75822222" height="3.8784"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(98.713165, 98.927420) rotate(225.016206) translate(-98.713165, -98.927420) " x="94.8362243" y="96.9882383" width="7.7538815" height="3.87836296"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(29.295234, 30.108781) rotate(44.975691) translate(-29.295234, -30.108781) " x="25.4161602" y="28.1695998" width="7.75814852" height="3.87836316"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(81.580657, 109.573273) rotate(248.011322) translate(-81.580657, -109.573273) " x="77.7032097" y="107.633483" width="7.75489383" height="3.87958011"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(46.421360, 19.880393) rotate(67.995385) translate(-46.421360, -19.880393) " x="42.5434774" y="17.9403854" width="7.75576527" height="3.88001607"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(108.842178, 46.304120) rotate(158.006009) translate(-108.842178, -46.304120) " x="104.963164" y="44.3635462" width="7.75802861" height="3.88114759"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(19.689182, 82.790958) rotate(-21.999303) translate(-19.689182, -82.790958) " x="15.8093111" y="80.8510222" width="7.75974144" height="3.87987072"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(108.072608, 83.282612) rotate(203.003741) translate(-108.072608, -83.282612) " x="104.194121" y="81.3433686" width="7.7569741" height="3.87848705"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(19.250526, 46.032859) rotate(22.980405) translate(-19.250526, -46.032859) " x="15.3715768" y="44.0937401" width="7.75789839" height="3.87823811"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(83.058140, 19.557293) rotate(22.967618) translate(-83.058140, -19.557293) " x="81.1182824" y="15.6797112" width="3.87971461" height="7.75516268"></rect><rect id="Rectangle-path" fill="#ffffff"  transform="translate(45.539518, 108.946679) rotate(202.993192) translate(-45.539518, -108.946679) " x="43.6004264" y="105.069917" width="3.87818399" height="7.75352369"></rect><path id="icon-cursor" d="M56.8689778,56.6072889 L24.0256,104.201956 C23.872,104.425244 24.1393778,104.694044 24.3612444,104.539022 L71.9573333,71.6942222 L104.802133,24.0967111 C104.954311,23.8734222 104.688356,23.6088889 104.465067,23.7610667 L56.8689778,56.6072889 L56.8689778,56.6072889 Z M38.4839111,90.0807111 L59.2497778,59.7162667 L68.7672889,69.2352 L38.4839111,90.0807111 L38.4839111,90.0807111 Z" id="Shape" fill="#ffffff" ></path></g></g></svg>
      }
      return (
        <div>
          <div className="react-black" onClick={this.hideExt}></div>
          {articles}
        </div>)
  }})

React.render(
        <Main />,
        document.getElementById('react-hook')
      );
