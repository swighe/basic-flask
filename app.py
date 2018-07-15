from flask import Flask, render_template, request, url_for, redirect
import ast
import os
import re

app = Flask(__name__)

people_data = [
	{
		'id': 1,
		'first_name': 'James',
		'last_name': 'Lin',
		'phone': '302-668-3584'
	},
	{
		'id': 2,
		'first_name': 'Tanni',
		'last_name': 'Kufferath-Lin',
		'phone': '805-345-1086'
	},
	{
		'id': 3,
		'first_name': 'James',
		'last_name': 'Not-Lin',
		'phone': '123-456-7890'
	}
]

def is_int(maybe_int):
	try:
		int(maybe_int)
	except Exception:
		return False
	return True

def get_people(search_param):
	search_param_is_int = is_int(search_param)
	matching_people = []
	lower_search_param = search_param.lower()
	for person in people_data:
		if search_param_is_int:
			if re.search(search_param + '$', person['phone']) is not None:
				matching_people.append(person)
				continue
		else:
			if person['first_name'].lower() == lower_search_param:
				matching_people.append(person)
				continue
			if person['last_name'] == lower_search_param:
				matching_people.append(person)
				continue
	# get all people
	# if search_param is numeric, then match on phone last 4
	# else match on either first name or last name (make lower)
	return matching_people

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		people_results = get_people(request.form['check_in_input'])
		# check for success, if failure, then show no results page
		return redirect(url_for('check_in', people=people_results))
	return render_template('home.html')

def print_name_tags(ids):
	for id in ids:
		print 'PRINT NAMETAG FOR PERSON WITH ID: ' + id

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