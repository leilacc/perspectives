var currentbody = document.body

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (!hookElem) {
            document.body.setAttribute("id","currentpage")
            document.body.setAttribute("style","transition: transform 0.2s ease-in-out;transform:translateX(-150px)")
            document.head.insertAdjacentHTML('afterend',"<div id='perspectives'></div>")
            var hookElem = document.querySelectorAll("#perspectives")[0]
        }

        React.render(<Main data={request}/>, hookElem);
});

//<div className="visible-on-hover">
//    <h2>Horrific Images Capture The Sheer Brutality Of War In Ukraine</h2>
//    <p className="details">Buzzfeed <span className="pull-right">3 days ago</span></p>
//</div>

var Article = React.createClass({
    componentDidMount: function(){
        Velocity(this.getDOMNode(), {translateX: "0px"}, {duration:200, delay: 200+(50*(this.props.num)), easing:"ease-in-sine"})
    },
    render: function(){
        var re = /\*{2}(\w+)\*{2}/g;
        var body = this.props.art.sentences[0].replace(re, "<b>$1</b>")

        return (<li>
            <div className="hidden-on-hover" dangerouslySetInnerHTML={{__html: "<p>" + body + "</p>"}}>
            </div>
        </li>)
    }
})

var arts = [
            "“On Tuesday, however, <b>rebels</b> seized most of the town and took several Ukrainian soldiers captive.”",
            "“The rebels had just <b>seized the town</b>, cutting Debaltseve off from the last road leading to Ukrainian territory.”",
            "“When Russian-backed rebels went on the <b>offensive</b> in east Ukraine a month ago, the focal point of the <b>clashes</b> quickly switched to Debaltseve, a strategically key rail junction linking their two unsanctioned states.”",
            "“For weeks, Ukraine’s <b>government denied</b> rebel claims to have the town surrounded, even as artillery fire prompted most civilians to flee, killed hundreds, and destroyed the town beyond recognition.”",
            "“The soldiers were mostly local volunteers, though their <b>commanding officers were Russian</b> — as were the men who delivered them tanks and artillery.”"
];

var Main = React.createClass({
    getInitialState: function(){
        return {firstTimeShowToggle: true,
                articles: arts}
    },
    componentDidMount: function(){
        //setTimeout(function(s){s.setState({articles: arts})}, 2000, this);
    },
    onHover: function(){
        currentbody.setAttribute("style","transition: transform 0.2s ease-in-out;transform:translateX(-150px)")
    },
    onHoverOut: function(){
        if(this.state.firstTimeShowToggle) {
            this.setState({firstTimeShowToggle: false})
        }
        currentbody.setAttribute("style","transition: transform 0.2s ease-in-out;transform:translateX(-25px)")
    },
    render: function(){
        var articles = this.props.data.map(function(f,i){
            return (<Article num={i} art={f}/>)
        })

        var showToggle = this.state.firstTimeShowToggle ? "show" : "";

        return (<div>
                    <ul id="perspectives-side" onMouseOver={this.onHover} onMouseOut={this.onHoverOut} className={showToggle}>
                        {articles}
                    </ul>
                </div>)
    }
})

