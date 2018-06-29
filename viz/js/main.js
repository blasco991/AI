$(function () {

    let step = 0, gear = 100, timerId = null;
    const $gear = $("#gear"), $step = $("#step"), $target = $("#target"), $step_value = $("#step_value");
    const selection = d3.select("#graph"), graphviz = selection.graphviz() //{scaleExtent: [1, 10]}
        .transition(function () {
            return d3.transition("main")
            //.ease(d3.easeLinear)
            //.duration(1000);
        });
    //.logEvents(true);
    //.on("initEnd", render);
    //.tweenPaths(false);

    $gear.val(gear);

    let dotLines, dotHeader, dotFooter, n_steps;
    const urlParams = new URLSearchParams(window.location.search);

    const resetZoom = () => graphviz.resetZoom(graphviz.transition());

    const ftc = target => fetch(target)
        .then(response => response.text())
        .then(text => {
                //console.info(text);
                dotLines = text.split('\n');
                dotHeader = dotLines.slice(0, 3);
                dotFooter = dotLines.slice(-2);
                n_steps = dotLines.length - dotHeader.length - dotFooter.length;
                step = dotHeader.length;
                $step.attr("min", String(dotHeader.length));
                $step.attr("max", n_steps + dotFooter.length);
                $step.val(step);
                $step_value.val(step);
                //console.log(text);
                console.log(n_steps);
                graphviz.dot(text).render();
            }
        ).catch(error => console.error(error));

    $target.val(urlParams.has('target') ? urlParams.get('target') : $("#target option:first").val());
    $target.change(event => window.location.href = "/?target=" + encodeURI(event.target.value));
    /*$target.change(event => {
        timerId = clearTimeout(timerId);
        ftc(encodeURI(event.target.value));
    });*/

    ftc($target.val());

    const renderStep = () => {
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
                dotBody = dotBody
                    .replace(new RegExp('black color=red', 'g'), 'black')
                    .replace(new RegExp('grey color=red', 'g'), 'grey');

            step++;
            let dot = dotHeader.join(' ') + dotBody + dotFooter.join(' ');
            //console.log("dot:\t", dot);
            graphviz.dot(dot).render()
                .on("end", function () {
                    resetZoom();
                    if (timerId != null)
                        timerId = setTimeout(renderStep, gear);
                });
        }
    };


    $("#reset").click(() => resetZoom());

    $("#back").click(function () {
        timerId = clearTimeout(timerId);
        if (step > 1 + dotHeader.length) {
            step -= 2;
            renderStep();
        }
    });

    $("#forward").click(function () {
        timerId = clearTimeout(timerId);
        renderStep();
    });

    $("#pp").click(function () {
        if (timerId != null) {
            timerId = clearTimeout(timerId);
        } else
            timerId = setTimeout(renderStep, gear);
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
        renderStep();
    });

    $gear.change(function (event) {
        gear = Number(event.target.value);
        if (timerId != null) {
            clearTimeout(timerId);
            timerId = setTimeout(renderStep, gear);
        }
    });

});