from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import re
import nltk as nlp
import ast
import time
from find_tennis_court import *
from MapLoader import *

app = Flask(__name__)

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/foo', methods=['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def foo():
    WKT_argument = request.args.get('text')
    print(WKT_argument)

    if WKT_argument != "":
        WKT_to_Images(WKT_argument)
    list = find_tennis_court()
    return jsonify(list)

if __name__ == '__main__':
    app.run()
