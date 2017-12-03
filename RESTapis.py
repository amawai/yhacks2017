#import MySQLdb as m
from flask import Flask, url_for, render_template
from flask import json, request
#from flask_cors import CORS, cross_origin
app = Flask(__name__)
#CORS(app)
from graphtest import computeNodes
@app.route('/')
def main():
	badGuys = computeNodes()
	print(badGuys)
	return render_template('index.html', badGuys=badGuys)

if __name__ == '__main__':
    app.run()
