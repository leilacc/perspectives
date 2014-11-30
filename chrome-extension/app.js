var hookElem = document.createElement("div");
hookElem.setAttribute("id", "react-hook");
document.body.appendChild(hookElem);

React.render(
        <h1>Hello, world!</h1>,
        document.getElementById('react-hook')
      );
