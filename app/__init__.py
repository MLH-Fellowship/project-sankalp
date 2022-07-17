import os, sys
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])
    
@app.route('/main')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/')
def About_Yourself():
    return render_template('About_Yourself.html')

@app.route('/Map')
def Map():
    return render_template('Map.html')

@app.route('/Hobbies')
def Hobbies():
    return render_template('Hobbies.html')

@app.route('/Education')
def Education():
    return render_template('Education.html')

@app.route('/Experience')
def Experience():
    return render_template('Previous_Work_Experience.html')

@app.route('/Timeline')
def timeline():
    posts = TimelinePost.select()
    storage = []
    for post in posts:
        storage.append(model_to_dict(post))
    
    return render_template('timeline.html', title='Timeline')
#      return render_template('timeline.html', posts=posts)

app.add_url_rule("/aboutUs", endpoint="/")
app.add_url_rule("/aboutMap", endpoint="/Map")
app.add_url_rule("/aboutHobbies", endpoint="/Hobbies")
app.add_url_rule("/aboutEducation", endpoint="/Education")
app.add_url_rule("/aboutExperience", endpoint="/Experience")

# Post new timeline
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

# # Retrieve all timeline and return a list of points
# @app.route('/api/display_timeline_post', methods=['GET'])
# def display_timeline_post():
#     posts = TimelinePost.select()
#     storage = []
#     for post in posts:
#         storage.append(model_to_dict(post))
#      return storage

 
# # Retrieve all timeline posts ordered by created_at descending
# @app.route('/api/timeline_post', methods=['GET'])
# def get_time_line_post():
#     return {
#         'timeline_posts': [
#             model_to_dict(p)
#             for p in
# TimelinePost.select().order_by(TimelinePost.created_at.desc())
#         ]
#     }

