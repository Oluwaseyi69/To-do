import re

from bson import ObjectId
from flask import Flask, render_template, url_for, request, redirect, flash, session
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
new_database_name = "todo_app"
db = client[new_database_name]
collection = db["todo"]
today = datetime.now
app.config["SECRET_KEY"] = 'dfba7e26ea088d28ce78eeef5718441bf7eca3e3'
app.config["MONGO_URI"] = "mongodb://localhost:27017"


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        new_user = {
            'username': username,
            'password': password
        }

        collection.db.users.insert_one(new_user)
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))

        if not is_valid_password(password):
            flash('Invalid password. Please choose a stronger password.', 'danger')
            return redirect(url_for('signup'))

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


def is_valid_password(password):
    length = 8
    uppercase = re.search(r'[A-Z]', password)
    lowercase = re.search(r'[a-z]', password)
    digit = re.search(r'\d', password)
    character = re.search(r'\W', password)

    if len(password) < length or not uppercase or not lowercase or not digit or not character:
        return False

    return True


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.db.users.find_one({'username': username})

        if user and password:
            flash('Login successful!', 'success')
            return render_template('index.html')

            # return redirect(url_for('index.html'))
        else:
            flash('Login unsuccessful. Check username and password.', 'danger')

    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task = {
            "content": task_content,
            "created_at": datetime.now(),
            "completed": False
        }
        collection.insert_one(task)
        tasks = collection.find()
        return render_template('signup.html', tasks=tasks)

    else:
        return render_template('signup.html')


@app.route('/complete_task/<int:task_id>', methods=['GET', 'POST'])
def complete_task(task):
    collection.update_one(task, {"$set": {"completed": True}})
    return redirect(url_for('index'))


@app.route('/create_task', methods=['POST', 'GET'])
def create_task():
    task_content = request.form['content']

    task = {
        "content": task_content,
        "created_at": datetime.now(),
        "completed": True
    }
    collection.insert_one(task)

    tasks = collection.find()
    return render_template('index.html', tasks=tasks)


@app.route('/delete_task/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task_id_object = ObjectId(task_id)
    collection.delete_one({'_id': task_id_object})

    return render_template('index.html')


@app.route('/update_task/<task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    global update_task_data
    task_id_object = ObjectId(task_id)
    if request.method == 'POST':
        update_task_data = {
            "content": request.form.get('content'),
            "created_at": datetime.now(),
            "completed": True
        }
    collection.update_one({'_id': task_id_object}, {'$set': update_task_data})

    return redirect(url_for('index'))

    # task = collection.find_one({'_id': task_id_object})
    # return render_template('update.html', task=task)


@app.route('/view_tasks', methods=['GET', 'POST'])
def view_tasks():
    tasks = collection.find()
    return render_template('view_tasks.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
