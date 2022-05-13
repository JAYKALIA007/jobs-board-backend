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

@app.route('/category_filter' , methods=['GET'])
def category_filter():
    category = request.args['filterTerm']
    offsetValue = request.args['offsetValue']
    categorySlug = ''
    if(category == 'Software Development'):
        categorySlug = 'software-dev'
    elif(category == 'Design') :
        categorySlug = 'design'
    elif(category == 'Human Resources'):
        categorySlug = 'hr'
    elif(category == 'DevOps / Sysadmin'):
        categorySlug = 'devops'
    elif(category == 'Product'):
        categorySlug = 'product'
    elif(category == 'Finance / Legal'):
        categorySlug = 'finance-legal'
    elif(category == 'Business'):
        categorySlug = 'business'
    elif(category == 'Sales'):
        categorySlug = 'sales'
    elif(category == 'Writing'):
        categorySlug = 'writing'
    elif(category == 'Customer Service'):
        categorySlug = 'customer_support'
    elif(category == 'Marketing'):
        categorySlug = 'marketing'
    elif(category == 'Data'):
        categorySlug = 'data'
    elif(category == 'QA'):
        categorySlug = 'qa'
    else:
        categorySlug = 'all-others'
    
    myUrl = "https://remotive.com/api/remote-jobs?category=" + categorySlug + "&limit=10&offset=" + offsetValue

    r=requests.get(myUrl)
    response=r.json()

    return response

@app.route('/search', methods=['GET'])
def search():
    searchTerm = request.args['searchTerm']
    myUrl = 'https://remotive.com/api/remote-jobs?search='+searchTerm
    r = requests.get(myUrl)
    response = r.json()
    searchTermJobCount = response['job-count']
    if searchTermJobCount == 0:
        return jsonify("No jobs found. Please change search term.")
    else :
        return response  

@app.route('/apply', methods=['POST'])
def apply():
    arg_body = request.json
    userInfo = request.json['userDetails']
    userInfoBody = {}
    userInfoBody['userInfo'] = userInfo['userInfo']
    userInfoBody['educationInfo'] = userInfo['educationInfo']
    userInfoBody['jobExperienceInfo'] = userInfo['jobExperienceInfo']
    userInfoBody['uuid'] = arg_body['uuid']
    mongo.db[mycol].insert_one(arg_body)
    result = mongo.db["users"].find_one({"uuid": arg_body['uuid']})
    if result : 
        mongo.db["users"].replace_one({"uuid":arg_body['uuid']},userInfoBody)
    else : 
        mongo.db["users"].insert_one(userInfoBody)
    return jsonify('Applied successfully')

@app.route('/get_applied_jobs' , methods=['GET'])
def get_applied_jobs():
    userUUID = request.args['userUUID']
    jobIdArray = []
    results = mongo.db[mycol].find({'uuid' : userUUID})
    for r in results:
        if r['jobId'] not in jobIdArray:
            jobIdArray.append(r['jobId'])

    return jsonify(jobIdArray)

@app.route('/get_current_user_info' , methods=['GET'])
def get_current_user_info():
    userUUID = request.args['userUUID']
    result = mongo.db["users"].find_one({'uuid' : userUUID})
    if result : 
        userInfoBody = {}
        userInfoBody['userInfo'] = result['userInfo']
        userInfoBody['educationInfo'] = result['educationInfo']
        userInfoBody['jobExperienceInfo'] = result['jobExperienceInfo']
    else :
        userInfoBody = 'No user information found'
    return jsonify(userInfoBody)

if __name__ == '__main__':
	app.run()
