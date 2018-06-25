$(function () {

    let step = 0, gear = 100, timerId = null;
    const $gear = $("#gear"), $step = $("#step"), $target = $("#target"), $step_value = $("#step_value");
    const selection = d3.select("#graph"), graphviz = selection.graphviz({scaleExtent: [1, 10]})
        .transition(function () {
            return d3.transition("main")
            //.ease(d3.easeLinear)
            //.duration(1000);
        });
    //.logEvents(true);
    //.on("initEnd", render);
    //.tweenPaths(false);

    $gear.val(gear);
    $step.val(step);
    $step_value.val(step);

    let dotLines, dotHeader, dotFooter, n_steps;
    const urlParams = new URLSearchParams(window.location.search);

    const ftc = target => fetch(target)
        .then(response => response.text())
        .then(text => {
                //console.info(text);
                dotLines = text.split('\n');
                dotHeader = dotLines.slice(0, 3);
                //dotBody = dotLines.slice(dotHeader.length, step + dotHeader.length);
                dotFooter = dotLines.slice(-2);
                n_steps = dotLines.length - dotHeader.length - dotFooter.length;
                step = dotHeader.length;
                $step.attr("min", String(dotHeader.length));
                $step.attr("max", n_steps);
                //console.log(text);
                console.log(n_steps);
                graphviz.dot(text).render()
            }
        ).catch(error => console.error(error));

    $target.val(urlParams.has('target') ? urlParams.get('target') : $("#target option:first").val());
    $target.change(event => window.location.href = "/?target=" + encodeURI(event.target.value));

    ftc($target.val());

    const render = () => {
        //console.info("render");
        if (step > n_steps + dotFooter.length) {
            timerId = clearTimeout(timerId);
        } else {
            $step.val(step);
            $step_value.val(step - 3);
            let dotBody = String(dotLines.slice(dotHeader.length, step).join('\n'));
            if (!dotBody.endsWith('}') && dotBody.includes('subgraph cluster'))
                dotBody = dotBody.concat('}');

            if (!dotBody.includes('GOALSTATE'))
                dotBody = dotBody.replace(new RegExp('red', 'g'), 'grey');

            step++;
            let dot = dotHeader.join(' ') + dotBody + dotFooter.join(' ');
            //console.log("dot:\t", dot);
            graphviz.dot(dot).render()
                .on("end", function () {
                    if (timerId != null)
                        timerId = setTimeout(render, gear);
                });
        }
    };

    $("#reset").click(() => graphviz.resetZoom(graphviz.transition()));

    $("#back").click(function () {
        timerId = clearTimeout(timerId);
        if (step > 1 + dotHeader.length) {
            step -= 2;
            render();
        }
    });

    $("#forward").click(function () {
        timerId = clearTimeout(timerId);
        render();
    });

    $("#pp").click(function () {
        if (timerId != null) {
            timerId = clearTimeout(timerId);
        } else
            timerId = setTimeout(render, gear);
    });

    $step.get().oninput = function (event) {
        timerId = clearTimeout(timerId);
        step = Number(event.target.value);
        $step_value.val(step - dotHeader.length);
    };

    $step.change(function (event) {
        timerId = clearTimeout(timerId);
        step = Number(event.target.value);
        $step_value.val(step - dotHeader.length);
        render();
    });

    $gear.change(function (event) {
        gear = Number(event.target.value);
        if (timerId != null) {
            clearTimeout(timerId);
            timerId = setTimeout(render, gear);
        }
    });

});