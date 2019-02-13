from flask import Flask, render_template, request, Response
import json
import os
import mysql.connector
from mysql.connector import errorcode
from base64 import b64encode, b64decode
from sys import exit

if 'AWS_USER' not in os.environ or 'AWS_PASS' not in os.environ or 'AWS_HOST' not in os.environ or 'AWS_DB' not in os.environ:
    print('Missing required env vars AWS_USER, AWS_PASS, AWS_HOST, AWS_DB')
    exit()

app = Flask(__name__)

add_user = 'INSERT INTO user (username) VALUES (%s)'
select_users_where = 'SELECT * FROM user WHERE username = %s'
select_users = 'SELECT * FROM user'
add_todo_item = 'INSERT INTO todo_item (content, user_id, deleted, completed) VALUES (%s, %s, 0, 0)'
select_todo_items_where_user_id = 'SELECT * FROM todo_item WHERE user_id = %s AND deleted = 0'
select_todo_items_where_user_id_and_id = 'SELECT * FROM todo_item WHERE user_id = %s AND id = %s AND deleted = 0'
delete_todo_items_where_id = 'UPDATE todo_item SET deleted = 1 WHERE id = %s'
update_todo_items_where_id = 'UPDATE todo_item SET content = %s, completed = %s WHERE id = %s'

AUTH_COOKIE_NAME = 'sillyauth'


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
    cnx = create_mysql_connection()
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
    return Response(json.dumps({'error': error_message, 'note': 'contact James if you see this because you never should'}), status=status, mimetype='application/json')


def create_client_error_response(error_message, status=400):
    return Response(json.dumps({'error': error_message}), status=status, mimetype='application/json')


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

    return create_success_response({'id': new_id, 'username': username}, status=201)


def handle_user_get_filter(username):
    try:
        results = read_data(select_users_where, (username,))
        if len(results) == 0:
            return create_client_error_response('No user with "username" %s was found.' % (username,), status=404)
        return create_success_response(results)
    except:
        return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)


def handle_user_get():
    try:
        results = read_data(select_users, ())
        return create_success_response(results)
    except:
        return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)


@app.route('/user', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'POST':
        return handle_user_post(request.get_data())
    if 'username' in request.args:
        return handle_user_get_filter(request.args['username'])
    return handle_user_get()


def handle_todo_item_post(data, user_id):
    try:
        data_json = json.loads(data)
    except:
        return create_client_error_response('Payload was not valid JSON. You must pass valid JSON.')

    if 'content' not in data_json:
        return create_client_error_response('Payload did not contain required field "content". You must pass "content" field.')
    content = data_json['content']

    try:
        new_id = write_data(add_todo_item, (content, user_id))
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)

    return create_success_response({'id': new_id, 'content': content, 'deleted': False, 'completed': False, 'user_id': user_id}, status=201)


def transform_db_to_api(object):
    to_return = object
    to_return['deleted'] = bool(object['deleted'])
    to_return['completed'] = bool(object['completed'])
    return to_return


def handle_todo_item_get(user_id):
    try:
        results = read_data(select_todo_items_where_user_id, (user_id,))
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)
    return create_success_response(list(map(transform_db_to_api, results)))


@app.route('/todo-item', methods=['GET', 'POST'])
def handle_todo_item():
    if AUTH_COOKIE_NAME not in request.cookies:
        return create_client_error_response('The todo-item service requires authentication. See the auth service.', status=401)
    username = b64decode(request.cookies[AUTH_COOKIE_NAME].encode(
        'utf-8')).decode('utf-8')

    try:
        users = read_data(select_users_where, (username,))
        if len(users) == 0:
            return create_client_error_response('Authorized user not found.', status=401)
        user_id = users[0]['id']
    except:
        return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)
    if request.method == 'POST':
        return handle_todo_item_post(request.get_data(), user_id)
    return handle_todo_item_get(user_id)


def handle_todo_item_with_id_delete(todo_item_id, user_id):
    try:
        results = read_data(
            select_todo_items_where_user_id_and_id, (user_id, todo_item_id))
        if len(results) == 0:
            return create_client_error_response('Could not delete todo-item %s as user %s.' % (todo_item_id, user_id))
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)
    try:
        write_data(delete_todo_items_where_id, (results[0]['id'],))
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)
    return create_success_response('', status=204)


def handle_todo_item_with_id_put(data, todo_item_id, user_id):
    try:
        data_json = json.loads(data)
    except:
        return create_client_error_response('Payload was not valid JSON. You must pass valid JSON.')

    if 'content' not in data_json and 'completed' not in data_json:
        return create_client_error_response('Payload did not contain one of fields "content" and "completed".')

    try:
        results = read_data(
            select_todo_items_where_user_id_and_id, (user_id, todo_item_id))
        if len(results) == 0:
            return create_client_error_response('Could not put update todo-item %s as user %s.' % (todo_item_id, user_id))
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)

    if 'content' in data_json:
        content = data_json['content']
    else:
        content = results[0]['content']
    if 'completed' in data_json:
        completed = data_json['completed']
    else:
        completed = bool(results[0]['completed'])

    try:
        write_data(update_todo_items_where_id,
                   (content, int(completed), todo_item_id))
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)

    return create_success_response({'id': todo_item_id, 'content': content, 'deleted': False, 'completed': completed, 'user_id': user_id})


def handle_todo_item_with_id_get(todo_item_id, user_id):
    try:
        results = read_data(
            select_todo_items_where_user_id_and_id, (user_id, todo_item_id))
        if len(results) == 0:
            return create_client_error_response('Could not find todo-item %s as user %s.' % (todo_item_id, user_id), status=404)
    except:
        return create_server_error_response('Something went wrong trying to write to the mysql database', status=503)
    return create_success_response(transform_db_to_api(results[0]))

@app.route('/todo-item/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_todo_item_with_id(id):
    if AUTH_COOKIE_NAME not in request.cookies:
        return create_client_error_response('The todo-item service requires authentication. See the auth service.', status=401)
    username = b64decode(request.cookies[AUTH_COOKIE_NAME].encode(
        'utf-8')).decode('utf-8')

    try:
        users = read_data(select_users_where, (username,))
        if len(users) == 0:
            return create_client_error_response('Authorized user not found.', status=401)
        user_id = users[0]['id']
    except:
        return create_server_error_response('Something went wrong trying to read from the mysql database', status=503)

    if request.method == 'DELETE':
        return handle_todo_item_with_id_delete(id, user_id)
    elif request.method == 'PUT':
        return handle_todo_item_with_id_put(request.get_data(), id, user_id)
    return handle_todo_item_with_id_get(id, user_id)


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

    token_value = b64encode(username.encode('utf-8')).decode('utf-8')
    response = create_success_response({'token': token_value})
    response.set_cookie(AUTH_COOKIE_NAME, token_value)
    return response


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
