from flask import Flask, render_template, url_for,request,redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
#below line  defines the datbase (three/:means relative path, four /:means absolute path, data will be stored in test.db file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialising database here
db = SQLAlchemy(app)


#creating a model
class Todo(db.Model):
    #id of each task
    id = db.Column(db.Integer, primary_key = True)
    #content of each task, nullable=False means task cannot be empty
    content = db.Column(db.String(200),nullable = False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    #function to return a string evertime we create a new element
    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your Task"


    else:
            #returns all the data created in the order they were created
            tasks= Todo.query.order_by(Todo.date_created).all()
            return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was a problem deleting that task"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method=="POST":
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem with the update"

    else:
        return render_template('update.html',task=task)



if __name__ == "__main__":
    app.run(debug=True)
