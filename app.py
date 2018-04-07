from flask import Flask, render_template
import os
import requests

app = Flask(__name__)

api_url = 'http://borough-data.herokuapp.com'

@app.route('/')
def home():
	api_data = requests.get(api_url + '/borough').json()['data']
	return render_template('home.html', boroughs=api_data)

@app.route('/view/borough/<int:id>')
def render_borough_view(id):
	api_data = requests.get(api_url + '/borough/' + str(id)).json()['data']
	return render_template(
		'borough_view.html',
		name=api_data['name'],
		county_name_value=api_data['county_name'],
		area_value=api_data['area_sq_mi'],
		population_value=api_data['population']
	)

@app.route('/combined')
def render_combined_view():
	i = 1
	combined_data = []
	while i <= 5:
		api_data = requests.get(api_url + '/borough/' + str(i)).json()['data']
		i = i + 1
		combined_data.append(api_data)
	return render_template(
		'combined.html',
		boroughs=combined_data
	)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)