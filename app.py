from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMIY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20),nullable = False)
    content = db.Column(db.String(200),nullable = False)
    date_created = db.Column(db.DateTime,default = datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id


db.create_all()


@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        message_content = request.form['content']
        print(message_content)
        new_message = Todo(sender="User", content= message_content)
        try:
            db.session.add(new_message)
            db.session.commit()

        except:
            return 'There was an error'

        bot_message = Todo(sender="BOT", content= "hello")
        try:
            db.session.add(bot_message)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an error'

    else:
        messages = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",messages = messages)


if __name__ == "__main__":
    app.run(debug=True)
