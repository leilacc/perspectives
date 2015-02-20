if (!hookElem) {
    document.body.setAttribute("id","currentpage")
    document.head.insertAdjacentHTML('afterend',"<div id='react-hook'></div>");
    var hookElem = document.body.querySelectorAll("#react-hook")
}

var Article = React.createClass({
    componentDidMount: function(){
        Velocity(this.getDOMNode(), {translateX: "0px"}, {duration:200, delay: 200+(50*this.props.num), easing:"ease-in-sine"})
    },
    render: function(){
        return (<li style={{backgroundColor: "rgba(255,255,255,0."+ (1+this.props.num)*2 +")"}}><h2>Title</h2></li>)
    }
})

var Main = React.createClass({
    getInitialState: function(){
       return {offsetY: document.body.scrollTop}
    },
    componentDidMount: function(){
        var self = this
        document.body.onscroll = function(){
            console.log(document.body.scrollTop)
            self.setState({offsetY: document.body.scrollTop})
        }
    },
    render: function(){
        var articles = [1, 2, 3, 4, 5, 6, 7, 8].map(function(i){
            return (<Article num={i}/>)
        })

        return (<div id="perspectives-side" style={{transform: "translate(30vw,"+this.state.offsetY+"px)"}}>
                    <ul>{articles}</ul>
                </div>)
    }
})

React.render(<Main />,
            document.getElementById('react-hook'));
