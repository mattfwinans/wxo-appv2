from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = '123'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Applications model
class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contract_start = db.Column(db.Date, nullable=False)
    cloud_provider = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Routes
@app.route('/')
def home():
    apps_ = Applications.query.all()
    return render_template('applications.html', apps_=apps_)

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        name = request.form['name']
        contract_start_str = request.form['contract_start']
        cloud_provider = request.form['cloud_provider']
        cost = request.form['cost']
        description = request.form['description']  # Get description from form

        try:
            contract_start = datetime.strptime(contract_start_str, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD.", 400


        new_app = Applications(name=name, contract_start=contract_start, cloud_provider=cloud_provider, cost=cost, description=description)
        db.session.add(new_app)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_application.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    app_ = Applications.query.get(id)
    if request.method == 'POST':
        app_.name = request.form['name']
        contract_start_str = request.form['contract_start']
        app_.cloud_provider = request.form['cloud_provider']
        app_.cost = request.form['cost']
        app_.description = request.form['description']  # Update description

        try:
            app_.contract_start = datetime.strptime(contract_start_str, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD.", 400

        db.session.commit()
        return redirect(url_for('view_application', id=app_.id))

    return render_template('edit_application.html', app_=app_)


@app.route('/view/<int:id>')
def view_application(id):
    app_ = Applications.query.get_or_404(id)
    return render_template('view_application.html', app_=app_)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_application(id):
    app_ = Applications.query.get_or_404(id)
    db.session.delete(app_)
    db.session.commit()
    flash('Application Deleted Successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/api/descriptions', methods=['GET'])
def get_all_descriptions():
    applications = Applications.query.all()
    descriptions = [{"id": app_.id, "name": app_.name, "cost": app_.cost, "description": app_.description} for app_ in applications]
    return {"descriptions": descriptions}, 200

# Running the app on a custom port
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) 

