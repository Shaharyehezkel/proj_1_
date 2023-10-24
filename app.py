from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Configuring the SQLite database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"


# SQLAlchemy database object
db = SQLAlchemy(app)


# Object Classes

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    def __init__(self, title, author, year_published):
        self.title = title
        self.author = author
        self.year_published = year_published
       
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    loan_date = db.Column(db.Integer, nullable=False)
    loan_length = db.Column(db.Integer, nullable=False)
    def __init__(self, book_id, user_id, loan_date, loan_length):
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.loan_length = loan_length


# Create the database tables
with app.app_context():
    db.create_all()


# Route to get all books
@app.route('/books', methods=["GET"])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year_published": book.year_published
        }
        book_list.append(book_data)
    return jsonify({"books": book_list})

@app.route('/books/list')
def list_books():
    return render_template('books.html')


# Route to add a new book
@app.route('/books/add', methods=["POST"])
def add_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year_published = data.get("year_published")
    if title and author and year_published:
        new_book = Book(title=title, author=author, year_published=year_published)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully"})
    else:
        return jsonify({"error": "Title, author and publishing year are required fields"}), 400


# Route to update a book by ID
@app.route('/books/update/<int:book_id>', methods=["PUT"])
def update_book(book_id):
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year_published = data.get("year_published")
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if title:
        book.title = title
    if author:
        book.author = author
    if year_published:
        book.year_published = year_published
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})


# Route to delete a book by ID
@app.route('/books/delete/<int:book_id>', methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})


# Route to get all users
@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "city": user.city,
            "age": user.age
        }
        user_list.append(user_data)
    return jsonify({"users": user_list})

@app.route('/users/list')
def list_user():
    return render_template('users.html')


# Route to add a new user
@app.route('/users/add', methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    city = data.get("city")
    age = data.get("age")
    if name and age:
        new_user = User(name=name, city=city, age=age)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"})
    else:
        return jsonify({"error": "Full name, city and age are required fields"}), 400


# Route to update a user by ID
@app.route('/users/update/<int:user_id>', methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    city = data.get("city")
    age = data.get("age")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if name:
        user.name = name
    if city:
        user.city = city
    if age:
        user.age = age
    db.session.commit()
    return jsonify({"message": "User updated successfully"})


# Route to delete a user by ID
@app.route('/users/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


# Route to get all loans
@app.route('/loans', methods=["GET"])
def get_loans():
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        loan_data = {
            "id": loan.id,
            "book_id": loan.book_id,
            "user_id": loan.user_id,
            "loan_date": loan.loan_date,
            "loan_length": loan.loan_length
        }
        loan_list.append(loan_data)
    return jsonify({"loans": loan_list})

@app.route('/loans/list')
def list_loans():
    return render_template('loans.html')


# Route to add a new loan
@app.route('/loans/add', methods=["POST"])
def add_loan():
    data = request.json
    book_id = data.get("book_id")
    user_id = data.get("user_id")
    loan_date = data.get("loan_date")
    loan_length = data.get("loan_length")
    if book_id and user_id and loan_date and loan_length:
        new_loan = Loan(book_id=book_id, user_id=user_id, loan_date=loan_date, loan_length=loan_length)
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({"message": "Loan added successfully"})
    else:
        return jsonify({"error": "Book ID, user ID, loan date and loan length are required."}), 400


# Route to update a loan by ID
@app.route('/loans/update/<int:loan_id>', methods=["PUT"])
def update_loan(loan_id):
    data = request.json
    book_id = data.get("book_id")
    user_id = data.get("user_id")
    loan_date = data.get("loan_date")
    loan_length = data.get("loan_length")
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    if book_id:
        loan.book_id = book_id
    if user_id:
        loan.user_id = user_id
    if loan_date:
        loan.loan_date = loan_date
    if loan_length:
        loan.loan_length = loan_length
    db.session.commit()
    return jsonify({"message": "Loan updated successfully"})


# Route to delete a loan by ID
@app.route('/loans/delete/<int:loan_id>', methods=["DELETE"])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": "Loan deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)