from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape
import os

# Create an instance of Flask
app = Flask(__name__)

# Use pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    # Return template and data
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():
  
    mars_data = mongo.db.mars_data
    mars_data_set= mars_scrape.scrape()
    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_data_set, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)