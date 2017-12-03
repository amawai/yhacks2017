#import MySQLdb as m
from flask import Flask, url_for, render_template
from flask import json, request
import matplotlib.pyplot as plt
import networkx as nx
import pprint
#from flask_cors import CORS, cross_origin
app = Flask(__name__)
#CORS(app)
from graphtest import computeNodes, pplDict, bannedPpl


@app.route('/')
def main():
	G = computeNodes()
	badGuys = [ppl.getName() for ppl in pplDict.values() if ppl.getName() not in bannedPpl]
	G = computeNodes()
	plt.plot(121)
	f = plt.figure(figsize=(5,4))
	a = f.add_subplot(111)
	plt.axis('off')
	nx.draw(G, node_color=[ppl.getFactor() for ppl in pplDict.values()], font_weight='bold')
	plt.savefig('./templates/graph.png')
	return render_template('index.html', badGuys=badGuys)

@app.route('/images/<whatever>')
def images(whatever):
	return render_template('images.html')

@app.route('/fig')
def fig():
	G = computeNodes()
	plt.plot(121)
	f = plt.figure(figsize=(5,4))
	a = f.add_subplot(111)
	plt.axis('off')
	nx.draw(G, node_color=[ppl.getFactor() for ppl in pplDict.values()], font_weight='bold')

	f.savefig(img)
	plt.savefig('graph.png')
	return render_template('index.html')
	#nx.draw_shell(G, with_labels=True, font_weight='bold')
	#plt.show()

if __name__ == '__main__':
    app.run()
