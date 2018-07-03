$(function () {

    let step = 0, gear = 100, timerId = null;
    const $gear = $("#gear"), $step = $("#step"), $target = $("#target"), $step_value = $("#step_value");
    const selection = d3.select("#graph");
    const graphviz = selection.graphviz() //{scaleExtent: [1, 10]}
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
    const urlParams = new URLSearchParams(location.search);

    const resetZoom = () => graphviz.resetZoom(graphviz.transition());

    const ftc = target => fetch(target)
        .then(response => response.text())
        .then(text => {
                step = 0;
                //console.info(text);
                dotLines = text.trim().split('\n');
                dotFooter = dotLines.slice(-1);
                dotHeader = dotLines.slice(0, 3);
                n_steps = dotLines.length - dotHeader.length - dotFooter.length;
                $step.val(step);
                $step_value.val(step);
                $step.attr("min", step);
                $step.attr("max", n_steps);
                //console.log(text);
                console.log(n_steps);
                graphviz.dot(text).render();
            }
        ).catch(error => console.error(error));

    $target.val(urlParams.has('target') ? urlParams.get('target') : $("#target option:first").val())
        .change(event => window.location.href = "/?target=" + encodeURI(event.target.value)).focus();
    /*event =>
    timerId = clearTimeout(timerId);
    ftc(encodeURI(event.target.value));
    history.pushState({target: event.target.value}, document.title, "?target=" + event.target.value);*/

    window.onpopstate = event => window.location.href = "/?target=" + encodeURI(event.target.value);
    /*function (event) {
    timerId = clearTimeout(timerId);
    ftc(encodeURI(event.state.target));
    $target.val(new URLSearchParams(location.search).get('target'));
    };*/

    ftc($target.val());

    const renderStep = () => {
        //console.info("render");
        if (step >= n_steps + dotFooter.length) {
            timerId = clearTimeout(timerId);
        } else {
            $step.val(step);
            $step_value.val(step);
            let dotBody = String(dotLines.slice(dotHeader.length, step + dotHeader.length).join('\n'));
            step++;
            let dot = dotHeader.join(' ') + dotBody + dotFooter.join(' ');

            if (dot.includes('subgraph cluster') && ((dot.match(/{/g) || []).length > (dot.match(/}/g) || []).length))
                dot = dot.concat('}');

            if (!dot.includes('GOALSTATE'))
                dot = dot.replace(new RegExp('color=red', 'g'), '');

            //console.log(dot);
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
        if (step >= 2) {
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