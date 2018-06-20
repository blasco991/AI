let gear = 0;
document.getElementById("gear").value = gear;

const graphviz = d3.select("#graph").graphviz()
    .transition(function () {
        return d3.transition("main")
        //.ease(d3.easeLinear)
        //.duration(1000);
    });
//.logEvents(true);
//.on("initEnd", render);

let step = 0;
document.getElementById("step_value").value = step;
document.getElementById("step").value = step;

let dotLines, dotHeader, dotBody, dotFooter, n_steps;
const urlParams = new URLSearchParams(window.location.search);
const target = urlParams.get('target');
console.log(target);

fetch(target)
    .then(response => response.text())
    .then(text => {
            //console.info(text);
            dotLines = text.split('\n');
            dotHeader = dotLines.slice(0, 3);
            dotBody = dotLines.slice(dotHeader.length, step + dotHeader.length);
            dotFooter = dotLines.slice(-2);
            n_steps = dotLines.length - dotHeader.length - dotFooter.length;
            step = dotHeader.length;
            document.getElementById("step").setAttribute("min", String(dotHeader.length));
            document.getElementById("step").setAttribute("max", n_steps);
            //console.log(text);
            console.log(n_steps);
            graphviz.dot(text).render()
        }
    ).catch(error => console.error(error));

let timerId = null;

function render() {
    //console.info("render");
    if (step > n_steps ) {
        clearTimeout(timerId);
        timerId = null;
    } else {
        document.getElementById("step").value = step;
        document.getElementById("step_value").value = step - 3;
        dotBody = String(dotLines.slice(dotHeader.length, step).join(' '));
        if (!dotBody.endsWith('}') && dotBody.includes('subgraph cluster'))
            dotBody = dotBody.concat('}');

        if (step !== n_steps)
            dotBody = dotBody.replace(new RegExp('red', 'g'), 'black');

        step++;
        let dot = dotHeader.join(' ') + dotBody + dotFooter.join('');
        //console.log("dot:\t", dot);
        graphviz.dot(dot).render()
            .on("end", function () {
                if (timerId != null)
                    timerId = setTimeout(render, gear);
            });
    }
}

document.getElementById("back").onclick = function () {
    clearTimeout(timerId);
    step -= 2;
    render();
};

document.getElementById("forward").onclick = function () {
    clearTimeout(timerId);
    render();
};

document.getElementById("pp").onclick = function () {
    if (timerId != null) {
        clearTimeout(timerId);
        timerId = null;
    } else
        timerId = setTimeout(render, gear);
};

document.getElementById("step").oninput = function (event) {
    clearTimeout(timerId);
    step = Number(event.target.value);
    document.getElementById("step_value").value = step - dotHeader.length;
};

document.getElementById("step").onchange = function (event) {
    clearTimeout(timerId);
    step = Number(event.target.value);
    document.getElementById("step_value").value = step - dotHeader.length;
    render();
};

document.getElementById("gear").onchange = function (event) {
    gear = Number(event.target.value);
    if (timerId != null) {
        clearTimeout(timerId);
        timerId = setTimeout(render, gear);
    }
};
