from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Setting up database path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))

# Create database file
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    new_entry = Feedback(score=data['score'], comment=data['comment'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"status": "success", "message": "Received!"})

@app.route('/admin')
def admin():
    all_data = Feedback.query.all()
    return render_template('admin.html', feedbacks=all_data)

if __name__ == '__main__':
    print("CX Smart Feedback Server active at http://127.0.0.1:5000")
    app.run(debug=True)