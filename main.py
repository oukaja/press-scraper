from flask import Flask, render_template, request, jsonify, current_app, send_from_directory
from bidi.algorithm import get_display
import arabic_reshaper
import pymysql.cursors
import pymongo

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articlesapi', methods=['POST', 'GET'])
def articles_api():
    db = pymysql.connect(host="localhost",  # your host
                         user="root",  # username
                         passwd="",  # password
                         db="presscrawler",  # name of the database
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM article ORDER BY publication;")
    result = cursor.fetchall()

    return jsonify({'message': result})


@app.route('/articlesapinosql', methods=['POST', 'GET'])
def articles_api_nosql():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["kolchipress"]
    collection = db["articles"]
    results = collection.find()
    items = []
    for result in results:
        items.append(result)
    return jsonify(items)


@app.route('/articlesapinosql/<journal>', methods=['POST', 'GET'])
def articles_api_nosql_by_journal(journal):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["kolchipress"]
    collection = db["articles"]
    results = collection.find({"journal": journal})
    items = []
    for result in results:
        items.append(result)
    return jsonify(items)


if __name__ == "__main__":
    app.run(debug=True)
