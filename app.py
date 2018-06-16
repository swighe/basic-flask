from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/fulfill')
def home():
	return '{"fulfillmentText":"this response came from fulfillment"}'
	# return render_template('home.html')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True)