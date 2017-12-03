import csv
import pwd
import jwt
import crypt
import getpass
import MySQLdb as m
from flask import Flask, url_for
from flask import json, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

@app.route('/add', methods=['POST'])
def api_add():
	posted = request.get_data()
	request_json=request.json
	username=request_json['username']
	password=request_json['password']
	email=request_json['email']
	if addToDB(username,password,email)==False:
		return jwt.encode({'username': username }, 'secret', algorithm='HS256')
	else:
		return json.dumps({"status":200, "success":"false"})
@app.route('/checkuser', methods=['POST'])
def api_checkuser():
	posted = request.get_data()
	request_json=request.json
	username=request_json['username']
	password=request_json['password']
	if checkUser(username,password)==True:
		return jwt.encode({'username': username }, 'secret', algorithm='HS256')
	else:
		return json.dumps({"status":200, "success":"false"})
@app.route('/getcities', methods=['GET'])
def api_getCities():
	results = cities()
	return json.dumps({"status":200, "success":"true", "results":results})
@app.route('/places/<city>', methods=['GET'])
def places(city):
	places=getPlaces(city)
	return json.dumps({"status":200, "success":"true", "city":city, "places":places})
def addToDB(username,password,email):
	hashed = crypt.crypt(password, 'aa')
	exists=False
	db = m.connect(user='root',passwd='hello',db= 'test2',host='127.0.0.1',port=3306)
	connect=db.cursor()
	query=("SELECT * FROM `Users`"
		"WHERE `username`=%s")
	usernames=(username,)
	connect.execute(query,usernames)
	if len(connect.fetchall()) != 0:
		exists=True
		print "user already exists"
	else:
		add_user=("INSERT INTO Users"
		"(email, username, password)"
		"VALUES (%s,%s,%s)")
		print add_user
		user_data=(email,username,hashed)
		connect.execute(add_user,user_data)
		db.commit()
		db.close()
	return exists
	print "complete"
#INSERT INTO `Users` (`ID`, `email`, `username`, `password`)
def checkUser(username,password):
	structure=('ID','email','username','password')
	hashed = crypt.crypt(password, 'aa')
	db = m.connect(user='root',passwd='hello',db= 'test2',host='127.0.0.1',port=3306)
	connection=db.cursor()
	query=("SELECT * FROM `Users`"
		"WHERE `username`=%s")
	usernames=(username,)
	connection.execute(query,usernames)
	for row in connection.fetchall():
		index=0
		mydict={}
		for entry in row:
			mydict.update({structure[index]:entry})
			index+=1
	if mydict['password']==hashed:
		return True
	else:
		return False
	connection.close()
	db.close()

def cities():
	results=[]
	db = m.connect(user='root',passwd='hello',db= 'test2',host='127.0.0.1',port=3306)
	connect=db.cursor()
	query=("SELECT `city` FROM `top_places`")
	connect.execute(query)
	for row in connect.fetchall():
		results.append(row[0])
	return results
def getPlaces(city): #cannot have a slash in the city name else server error
	query=("SELECT `places` FROM `top_places`"
		"WHERE `city`=%s")
	db = m.connect(user='root',passwd='hello',db= 'test2',host='127.0.0.1',port=3306)
	connect=db.cursor()
	cities=(city,)
	connect.execute(query,cities)
	res=connect.fetchall()
	if len(res)==0:
		return None
	else:
		placesStr=res[0][0]
		print placesStr
		places=json.loads(placesStr) #get in proper json form
		return places
if __name__ == '__main__':
    app.run()