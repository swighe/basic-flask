from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

def a_function_we_call():
	return render_template('another.html')

@app.route('/another')
def not_home():
	return a_function_we_call()

@app.route('/is_it_over_9000/<int:number>')
def over_9000_check(number):
	if number > 9000:
		return render_template('9000.html')
	else:
		return 'no'

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)