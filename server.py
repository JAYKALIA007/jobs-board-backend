from urllib import response
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/JobApplication_db"   
app.config['MONGO_DBNAME'] = 'JobApplication_db'
mongo = PyMongo(app)
mycol = "job_applications"

@app.route('/')
def hello_world():
    response.headers.add("Access-Control-Allow-Origin", "*")
    return jsonify('Flask is running for jobs board')
 
@app.route('/get_categories', methods=['GET'])
def get_categories():
    categories = []
    r=requests.get('https://remotive.com/api/remote-jobs')
    response=r.json()
    jobs = response['jobs']
    for job in jobs:
        if(job['category'] not in categories):
            categories.append(job['category'])
    return jsonify(categories)

@app.route('/get_jobs_by_category', methods=['GET'])
def get_jobs_by_category():
    categoryObj = request.args
    categorySlug = ''
    if(categoryObj['category'] == 'Software Development'):
        categorySlug = 'software-dev'
    elif(categoryObj['category'] == 'Design') :
        categorySlug = 'design'
    elif(categoryObj['category'] == 'Human Resources'):
        categorySlug = 'hr'
    elif(categoryObj['category'] == 'DevOps / Sysadmin'):
        categorySlug = 'devops'
    elif(categoryObj['category'] == 'Product'):
        categorySlug = 'product'
    elif(categoryObj['category'] == 'Finance / Legal'):
        categorySlug = 'finance-legal'
    elif(categoryObj['category'] == 'Business'):
        categorySlug = 'business'
    elif(categoryObj['category'] == 'Sales'):
        categorySlug = 'sales'
    elif(categoryObj['category'] == 'Writing'):
        categorySlug = 'writing'
    elif(categoryObj['category'] == 'Customer Service'):
        categorySlug = 'customer_support'
    elif(categoryObj['category'] == 'Marketing'):
        categorySlug = 'marketing'
    elif(categoryObj['category'] == 'Data'):
        categorySlug = 'data'
    elif(categoryObj['category'] == 'QA'):
        categorySlug = 'qa'
    else:
        categorySlug = 'all-others'
    
    myUrl = "https://remotive.com/api/remote-jobs?category=" + categorySlug 

    r=requests.get(myUrl)
    response=r.json()

    return response

@app.route('/apply', methods=['POST'])
def apply():
    userInfo = request.json
    # print(userInfo)
    mongo.db[mycol].insert_one(userInfo)
    return jsonify('Applied successfully')


if __name__ == '__main__':
	app.run()
