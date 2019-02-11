from flask import Flask, render_template, request, Response
import json
import os
import mysql.connector
from mysql.connector import errorcode
from base64 import b64encode
from sys import exit

if 'AWS_USER' not in os.environ or 'AWS_PASS' not in os.environ or 'AWS_HOST' not in os.environ or 'AWS_DB' not in os.environ:
	print('Missing required env vars AWS_USER, AWS_PASS, AWS_HOST, AWS_DB')
	exit()

app = Flask(__name__)

add_user = 'INSERT INTO user (username) VALUES (%s)'
select_users_where = 'SELECT * FROM user WHERE username = %s'
select_users = 'SELECT * FROM user'

def create_mysql_connection():
	try:
		cnx = mysql.connector.connect(user=os.environ.get('AWS_USER'), password=os.environ.get('AWS_PASS'),
								host=os.environ.get('AWS_HOST'), database=os.environ.get('AWS_DB'))
		return cnx
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cnx.close()

def write_data(sql_command, data):
	cnx = create_mysql_connection()
	cursor = cnx.cursor()
	cursor.execute(sql_command, data)
	id = cursor.lastrowid
	cnx.commit()
	cursor.close()
	cnx.close()
	return id

def read_data(sql_command, data):
	print('start read_data')
	cnx = create_mysql_connection()
	print('mysql_connection created')
	cursor = cnx.cursor(dictionary=True)
	result = []
	cursor.execute(sql_command, data)
	for row in cursor:
		result.append(row)
	cursor.close()
	cnx.close()
	return result

def create_success_response(data, status=200):
	return Response(json.dumps(data), status=status, mimetype='application/json')

def create_server_error_response(error_message, status=500):
	return Response(json.dumps({ 'error': error_message, 'note': 'contact James if you see this because you never should' }), status=status, mimetype='application/json')

def create_client_error_response(error_message, status=400):
	return Response(json.dumps({ 'error': error_message }), status=status, mimetype='application/json')

def handle_user_post(data):
	try:
		data_json = json.loads(data)
	except:
		return create_client_error_response('Payload was not valid JSON. You must pass valid JSON.')

	if 'username' not in data_json:
		return create_client_error_response('Payload did not contain required field "username". You must pass "username" field.')
	username = data_json['username']

	try:
		if len(read_data(select_users_where, (username,))) > 0:
			return create_client_error_response('A user with that "username" already exists', status=409)
	except:
		return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)
	try:
		new_id = write_data(add_user, (username,))
	except:
		return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)
	
	return create_success_response({ 'id': new_id, 'username': username }, status=201)

def handle_user_get_filter(username):
	try:
		results = read_data(select_users_where, (username,))
		if len(results) == 0:
			return create_client_error_response('No user with "username" %s was found.' % (username,), status=404)
		return create_success_response(results[0])
	except:
		return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)

def handle_user_get():
	# try:
	print('handle_user_get')
	results = read_data(select_users, ())
	print('data read')
	return create_success_response(results)
	# except:
	# 	return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)

@app.route('/user', methods=['GET', 'POST'])
def handle_user():
	if request.method == 'POST':
		return handle_user_post(request.get_data())
	if 'username' in request.args:
		return handle_user_get_filter(request.args['username'])
	return handle_user_get()

@app.route('/auth', methods=['POST'])
def handle_auth():
	try:
		data_json = json.loads(request.get_data())
	except:
		return create_client_error_response('Payload was not valid JSON. You must pass valid JSON.')

	if 'username' not in data_json:
		return create_client_error_response('Payload did not contain required field "username". You must pass "username" field.')
	username = data_json['username']

	try:
		if len(read_data(select_users_where, (username,))) == 0:
			return create_client_error_response('A user with that "username" does not exist', status=400)
	except:
		return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)
	
	token_value = b64encode(username)
	response = create_success_response({ 'token': token_value })
	response.set_cookie('sillyauth', token_value)
	return response

@app.route('/')
def home():
	return render_template('home.html')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True, debug=True)