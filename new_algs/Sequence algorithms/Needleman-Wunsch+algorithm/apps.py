from flask import Flask
from flask import abort
from flask import request
from flask import Response
from flask import jsonify
from flask import json
from flask import render_template
import numpy as np
import io
import os

app = Flask(__name__, template_folder='templates')

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/static/<path:path>')
def get_resource(path):  # pragma: no cover
    mimetypes = {
        ".css": "text/css",
        ".html": "text/html",
        ".js": "application/javascript",
    }
    complete_path = os.path.join(root_dir(), path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)
 
@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/alignment_service', methods=['GET'])
def alignment_service():
    import global_alignment as ga
    s1 = request.args['s1']
    s2 = request.args['s2']
    match = request.args['match']
    missmatch = request.args['missmatch']
    gap = request.args['gap']
    ga.DoAlignment(s1, s2, int(match), int(missmatch), int(gap), 'NW')
    #print('req s1 : ' + s1 + ' s2 : ' + s2 + ' match/missmatch/gap : ' + match+'/'+missmatch+'/'+gap)
    #ga.ShowNode(False, True, False, False) #score
    #ga.ShowNode(False, False, True, False) #direction
    #ga.ShowAlignedSequence()
    resp = Response(response=json.dumps(ga.ConvertToJSON()), status=200, mimetype="application/json")
    return resp
 

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)