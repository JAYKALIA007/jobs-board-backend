from urllib import response
from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    response.headers.add("Access-Control-Allow-Origin", "*")
    return jsonify('Flask is running for jobs board')
 
@app.route('/get_categories')
def get_categories():
    categories = []
    r=requests.get('https://remotive.com/api/remote-jobs')
    response=r.json()
    jobs = response['jobs']
    for job in jobs:
        if(job['category'] not in categories):
            # tempCategory = {}
            # tempCategory['category'] = job['category']
            # tempCategory['selected'] = False
            # categories.append(tempCategory)
            categories.append(job['category'])
    return jsonify(categories)


if __name__ == '__main__':
	app.run()
