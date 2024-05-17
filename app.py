from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app) 

# Data Class (or we can say raw of data)
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed  = db.Column(db.Integer, default=0)
    created =   db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route('/', methods=["POST", "GET"])
def index():
    # add a task
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    # show all tasks   
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

# delete an task
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR: {e}")
        return f"ERROR: {e}"

# update an task
@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id:int):
    task = MyTask.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    else:
        return render_template("update.html", task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)