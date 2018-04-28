from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

list_of_names = []

@app.route('/')
def home():
	return render_template('home.html', names=list_of_names)

@app.route('/add-name', methods=['POST'])
def add_name():
	list_of_names.append(request.form['name'])
	return redirect('/')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)