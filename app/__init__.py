import os
import datetime
import re
from flask import Flask, render_template, request, make_response, jsonify
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

# Only initialize db before first request, not during import(for tests) 
@app.before_first_request
def initialize_database():
    mydb.connect()
    mydb.create_tables([TimelinePost])

name = "Eric Zhang"

@app.route('/')
def index():
    about_section = "Hi! I'm Eric and I'm studying 💻 Software Engineering at the 🏫 University of Waterloo! I'm incredibly interested in 🤖 Machine Learning and I also love building out random 💡 ideas!"
    markers = [
        {'lat': 55, 'lon': -95, 'popup': 'Canada'},
        {'lat': 40, 'lon': -100, 'popup': 'U.S.A.'},
        {'lat': 36, 'lon': 104, 'popup': 'China'},
        {'lat': 20, 'lon': -79, 'popup': 'Cuba'},
    ]
    return render_template('index.html', name=name, title="About", about=about_section, markers=markers, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    hobby_list = ["Rock Climbing", "Piano", "Skipping", "Taekwondo", "Skateboard"]
    return render_template('hobbies.html', name=name, title="Hobbies", hobbies=hobby_list, url=os.getenv("URL"))

@app.route('/work_experiences')
def work_experiences():
    experiences = [
        {
        'job_title': "Production Engineering Fellow",
        'company': "Meta x MLH",
        'location': "Remote",
        'start_date': "June 2024",
        'end_date': "September 2024",
        },
        {
        'job_title': "Android Intern",
        'company': "RBC",
        'location': "Toronto, ON",
        'start_date': "May 2024",
        'end_date': "August 2024",
        },
        {
        'job_title': "Undergraduate Research Assistant",
        'company': "University of Waterloo",
        'location': "Waterloo, ON",
        'start_date': "Janruary 2024",
        'end_date': "April 2024",
        },
        {
        'job_title': "Software Developer Intern",
        'company': "RBC",
        'location': "Toronto, ON",
        'start_date': "July 2023",
        'end_date': "August 2023",
        },
        {
        'job_title': "Machine Learning Intern",
        'company': "IBM",
        'location': "Markham, ON",
        'start_date': "July 2022",
        'end_date': "August 2022",
        }
    ]
    return render_template('work_experiences.html', name=name, title="Work Experiences", work_experiences=experiences, url=os.getenv("URL"))

@app.route('/education')
def education():
    educations = [
        {
            'school': "University of Waterloo",
            'degree': "Bachelor's in Software Engineering",
            'start_date': "September 2023",
            'end_date': "April 2028",
            'description': "President's Scholarship | B.P. Dammizio Scholarship | BMO Scholarship | Dean's List (x1) | Term Distinction (x1)"
        }
    ]
    return render_template('education.html', name=name, title="Education", educations = educations, url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', name=name, title="Timeline")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return make_response(jsonify({'error': 'Name is required'}), 400)
    if not email:
        return make_response(jsonify({'error': 'Email is required'}), 400)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return make_response(jsonify({'error': 'Invalid email'}), 400)
    if not content:
        return make_response(jsonify({'error': 'Content is required'}), 400)

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<id>', methods=['DELETE'])
def delete_time_line_post(id):
    TimelinePost.delete().where(TimelinePost.id=={id}).execute()
    return "Post successfully deleted"

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_all_time_line_post():
    TimelinePost.delete().execute()
    return "All posts successfully deleted"
