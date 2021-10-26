from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/dish.db'
db = SQLAlchemy(app)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menuname = db.Column(db.String(200))
    done = db.Column(db.Boolean)


@app.route('/')
def home():
    dish = Menu.query.all()
    return render_template('index.html', dish=dish)


@app.route('/create-dish', methods=['POST'])
def create():
    new_dish = Menu(menuname=request.form['menuname'], done=False)
    db.session.add(new_dish)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/done/<id>')
def done(id):
    dish = Menu.query.filter_by(id=int(id)).first()
    dish.done = not(dish.done)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    Menu.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
