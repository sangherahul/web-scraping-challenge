from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/scraper")

@app.route("/")

def home():

    default = mongo.db.scrapped_info.find_one()

    return render_template('index.html', data = default)


@app.route('/scrape')

def scrape():

    data = scrape_mars.scraper()
    mongo.db.scrapped_info.update({}, data, upsert = True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)