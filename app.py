from flask import Flask, render_template, request, url_for, redirect
import ast
import json
import os
import requests

app = Flask(__name__)
base_breeze_api_endpoint = 'https://yourmnc.breezechms.com/api'
breeze_api_key = os.environ.get("BREEZE_API_KEY")
# currently using "Emergency Contact Phone Number 1"
phone_number_field_id = '1055797162'
# currently using "Label"
name_field_id = '11106318'

def is_int(maybe_int):
	try:
		int(maybe_int)
	except Exception:
		return False
	return True

def search_people(search_param):
	search_param_is_int = is_int(search_param)
	matching_people = []
	people_data = []
	if search_param_is_int:
		people_data = requests.get(
			base_breeze_api_endpoint + '/people',
			headers={'api-key': breeze_api_key},
			params={'filter_json': json.dumps({phone_number_field_id + '_contains': search_param})}
		).json()
	else:
		people_data = requests.get(
			base_breeze_api_endpoint + '/people',
			headers={'api-key': breeze_api_key},
			params={'filter_json': json.dumps({name_field_id + '_contains': search_param})}
		).json()
	for person in people_data:
		matching_people.append({
			'id': person['id'],
			'first_name': person['first_name'],
			'last_name': person['last_name']
		})
	return matching_people

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		people_results = search_people(request.form['check_in_input'])
		# check for success, if failure, then show no results page
		return redirect(url_for('check_in', people=people_results))
	return render_template('home.html')

def print_name_tags(ids):
	for id in ids:
		print ('SELECTED PERSON WITH NAME: ' + id)

@app.route('/check-in?people=<people>', methods=['GET', 'POST'])
def check_in(people):
	if request.method == 'POST':
		check_in_results = request.form
		print_name_tags(check_in_results)
		# check for success, if failure, then show get help page
		# or maybe show success page to indicate success, and then button to go back home
		return redirect(url_for('home'))
	return render_template('check-in.html', people=ast.literal_eval(people))

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.debug = True
	app.run(host="0.0.0.0", port=port, threaded=True)