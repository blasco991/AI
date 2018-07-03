from bottle import route, run, view, static_file
import os

f_map = {"gs": "Graph Search", "ts": "Tree Search", "tsp": "Tree Search Optimized",
         "tsd": "Tree Search Avoid Branch Repetition", "tspd": "Tree Search Opitmized Avoid Branch Repetition"}


@route('/css/<filepath>')
def css(filepath):
    return static_file(filepath, root='./css/')


@route('/js/<filepath>')
def js(filepath):
    return static_file(filepath, root='./js/')


@route('/artifacts/<filepath:path>')
def file_dot(filepath):
    return static_file(filepath, root='./artifacts/')


@route('/')
@view('viz')
def app():
    folders = {}
    for folder in os.listdir('./artifacts/'):
        folders[folder] = sorted(os.listdir('./artifacts/{}/dot/'.format(folder)))

    return dict(folders=folders, fmap=f_map)


try:
    run(host='localhost', port=8080)  # , quiet=True)
except OSError as e:
    pass
