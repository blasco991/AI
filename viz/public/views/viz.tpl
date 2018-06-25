<html>

<head>
    <title>viz.blasco991.com</title>
    <link rel="stylesheet" href="/css/style.css">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
            integrity="sha256-3edrmyuQ0w65f8gfBsqowzjJe2iM6n0nKciPUp8y+7E="
            crossorigin="anonymous">
    </script>
    <script>
        window.$ || document.write('<script src="javascripts/jquery-3.3.1.slim.min.js" type="text/javascript">\x3C/script>')
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
    <h1>Algo Visualizer by blasco991&reg;</h1>
    <select id="target" title="Target">
        % for key, files in folders.items():
        <optgroup label="{{fmap[key]}}">
            % for file in files:
            <option value="/artifacts/{{key + "/dot/" + file}}">{{file}}</option>
            % end
        </optgroup>
        % end
    </select>
</header>
<div id="graph"></div>
<footer>
    <button id="reset">Reset</button>
    <button id="back">Back</button>
    <button id="pp">Play/Pause</button>
    <button id="forward">Forward</button>
    <label>Step:&nbsp;
        <input id="step" type="range" title="Step" step="2"/>
    </label>
    <input id="step_value" type="number" title="Value" disabled="disabled"/>
    <label>Gear:&nbsp;
        <input id="gear" type="number" min="200" max="10000" title="gear" step="100"/>
    </label>
</footer>

<script src="/js/main.js" type="text/javascript"></script>
</body>

</html>
