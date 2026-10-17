from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///contacts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Contact {self.name}>'

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        if not name or not phone:
            flash('Name and Phone are required!', 'danger')
            return render_template('create.html', name=name, phone=phone, email=email, address=address)
        else:
            new_contact = Contact(name=name, phone=phone, email=email, address=address)
            db.session.add(new_contact)
            db.session.commit()
            flash('Contact added successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>')
def view(id):
    contact = Contact.query.get_or_404(id)
    return render_template('view.html', contact=contact)

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    contact = Contact.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        if not name or not phone:
            flash('Name and Phone are required!', 'danger')
            return render_template('edit.html', contact=contact, name=name, phone=phone, email=email, address=address)
        else:
            contact.name = name
            contact.phone = phone
            contact.email = email
            contact.address = address
            db.session.commit()
            flash('Contact updated successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('edit.html', contact=contact)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
