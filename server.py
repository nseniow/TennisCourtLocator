from flask import Flask, request
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
    return "BLah"

if __name__ == '__main__':
    app.run()
