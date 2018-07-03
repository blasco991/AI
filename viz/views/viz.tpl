<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>viz.blasco991.com</title>
    <link rel="stylesheet" href="/css/style.css">
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"
            integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
            crossorigin="anonymous">
    </script>
    <script>
        window.$ || document.write('<script src="javascripts/jquery-3.3.1.min.js" type="text/javascript">\x3C/script>')
    </script>
    <script src="https://d3js.org/d3.v4.min.js" type="text/javascript"></script>
    <script>
        window.d3 || document.write('<script src="/js/d3.v4.js" type="text/javascript">\x3C/script>')
    </script>
    <script src="https://unpkg.com/viz.js@1.8.0/viz.js" type="javascript/worker"></script>
    <script>
        window.Viz || document.write('<script src="/js/viz.js" type="javascript/worker">\x3C/script>')
    </script>
    <script src="https://unpkg.com/d3-graphviz@1.4.0/build/d3-graphviz.js" type="text/javascript"></script>
    <script>
        window.graphviz || document.write('<script src="/js/d3-graphviz.js"type="text/javascript">\x3C/script>')
    </script>

</head>
<body>
<header>
    <span>Algo Visualizer by blasco991&reg;</span>
    <select id="target" title="Target">
        % for key, files in folders.items():
        <optgroup label="{{fmap[key]}}">
            % for file in files:
            <option value="artifacts/{{key + "/dot/" + file}}">{{file}}</option>
            % end
        </optgroup>
        % end
    </select>
</header>
<div id="spinner" class="spinner"></div>
<div id="graph" style="display: none"></div>
<footer>
    <button id="reset">Center</button>
    <button id="back">Back</button>
    <button id="pp">Play/Pause</button>
    <button id="forward">Forward</button>
    <label>Step:&nbsp;
        <input id="step" type="range" title="Step" style="width:50%"/>
    </label>
    <input id="step_value" type="number" title="Value" disabled="disabled"/>
    <label>Gear:&nbsp;
        <input id="gear" type="number" min="200" max="10000" title="gear" step="100"/>
    </label>
</footer>
<script src="/js/main.js" type="text/javascript"></script>
</body>

</html>
