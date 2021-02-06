from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import re
import nltk as nlp
import ast

app = Flask(__name__)

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/foo', methods=['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def foo():
    msg = request.args.get('text')
    print(msg)
    return jsonify(['43.89422,-79.459207', '43.900228,-79.431756', '43.902095,-79.458712', '43.904878,-79.427869'])

if __name__ == '__main__':
    app.run()
