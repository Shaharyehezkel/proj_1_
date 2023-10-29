from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask import render_template
from datetime import datetime, timedelta
from sqlalchemy import func, or_
from flask_migrate import Migrate
from sqlalchemy import and_



app = Flask(__name__)




# Configuring the SQLite database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"




# SQLAlchemy database object
db = SQLAlchemy(app)
migrate = Migrate(app, db)





# Object Classes


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    def __init__(self, title, author, year_published, stock):
        self.title = title
        self.author = author
        self.year_published = year_published
        self.stock = stock
    loans = relationship('Loan', backref='book', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age
    loans = relationship('Loan', backref='user', lazy=True)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loan_date = db.Column(db.Integer, nullable=False)
    loan_length = db.Column(db.Integer, nullable=False)
    return_date = db.Column(db.Date, nullable=True)


    def __init__(self, book_id, user_id, loan_date, loan_length,return_date):
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.loan_length = loan_length
        self.return_date = return_date


#routes for html

@app.route('/books/list', methods=["GET"])
def page_books():
    return render_template("books.html")

@app.route('/loans/list', methods=["GET"])
def page_loans():
    return render_template("loans.html")

@app.route('/users/list', methods=["GET"])
def page_users():
    return render_template("users.html")


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
            "year_published": book.year_published,
            "stock": book.stock
        }
        book_list.append(book_data)
    return jsonify({"books": book_list})




# Route to add a new book
@app.route('/books/add', methods=["POST"])
def add_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year_published = data.get("year_published")
    stock = data.get("stock")
    if title and author and year_published and stock:
        new_book = Book(title=title, author=author, year_published=year_published, stock=stock)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "Book added successfully"})
    else:
        return jsonify({"error": "Title, author, publishing year and stock are required fields"}), 400




# Route to update a book by ID
@app.route('/books/<int:book_id>/update', methods=["PUT"])
def update_book(book_id):
    data = request.json
    title = data.get("title")
    author = data.get("author")
    year_published = data.get("year_published")
    stock = data.get("stock")
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if title:
        book.title = title
    if author:
        book.author = author
    if year_published:
        book.year_published = year_published
    if stock:
        book.stock = stock
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})


# Route to delete a book by ID
@app.route('/books/<int:book_id>/delete', methods=["DELETE"])
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




# Route to add a new user
@app.route('/users/add', methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    city = data.get("city")
    age = data.get("age")
    if name and city and age:
        new_user = User(name=name, city=city, age=age)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"})
    else:
        return jsonify({"error": "Full name, city and age are required fields"}), 400




# Route to update a user by ID
@app.route('/users/<int:user_id>/update', methods=["PUT"])
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
@app.route('/users/<int:user_id>/delete', methods=["PUT"])
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
            "loan_length": loan.loan_length,
            "return_date":loan.return_date
        }
        loan_list.append(loan_data)
    return jsonify({"loans": loan_list})




# Route to add a new loan
# @app.route('/loans/add', methods=["POST"])
# def add_loan():
#     book = Book.query.get(book_id)
#     data = request.json
#     book_id = data.get("book_id")
#     user_id = data.get("user_id")
#     loan_date = data.get("loan_date")
#     loan_length = data.get("loan_length")
#     return_date = data.get("return_date")
#     if not book:
#             return jsonify({"error": "Book not found"}), 404
   
#     if book_id and user_id and loan_date and loan_length and return_date:
#         # Check if the book exists
#         book = Book.query.get(book_id)
#         if not book:
#             return jsonify({"error": "Book not found"}), 404
       
#         user = User.query.get(user_id)
#         if not user:
#             return jsonify({"error": "User not found"}), 404
       
#         # Check if there are enough books in stock
#         if book.stock <= 0:
#             return jsonify({"error": "No more copies of this book in stock"}), 400
       
#         # Check if the requested loan length is valid
#     try:
#         loan_length_int = int(loan_length)
#         if 1 <= loan_length_int <= 365:
#             new_loan = Loan(book_id=book_id, user_id=user_id, loan_date=loan_date, loan_length=loan_length,return_date=return_date)
#             db.session.add(new_loan)
#             db.session.commit()

#             # Update the stock of the book
#             book.stock -= 1
#             db.session.commit()
#             return jsonify({"message": "Loan added successfully"})
#         else:
#             return jsonify({"error": "Loan length should be between 1 and 365 days."}),400
#         #else:
#         #return jsonify({"error": "Book ID, user ID, loan date, and loan length are required."}), 400
#     except ValueError:
#         return jsonify({"error": "Invalid loan length provided."})
@app.route('/loans/add', methods=["POST"])
def add_loan():
    data = request.json
    
    try:
        book_id = int(data.get("book_id"))
        user_id = int(data.get("user_id"))
    except ValueError:
        return jsonify({"error": "Invalid book_id or user_id provided."}), 400

    loan_date = data.get("loan_date")
    loan_length = data.get("loan_length")
    return_date = data.get("return_date")

    # Check if the book and user exist
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if there are enough books in stock
    if book.stock <= 0:
        return jsonify({"error": "No more copies of this book in stock"}), 400

    try:
        loan_length_int = int(loan_length)
        if 1 <= loan_length_int <= 365:
            new_loan = Loan(book_id=book_id, user_id=user_id, loan_date=loan_date, loan_length=loan_length, return_date=return_date)
            db.session.add(new_loan)
            db.session.commit()

            # Update the stock of the book
            book.stock -= 1
            db.session.commit()

            return jsonify({"message": "Loan added successfully"})
        else:
            return jsonify({"error": "Loan length should be between 1 and 365 days."}), 400

    except ValueError:
        return jsonify({"error": "Invalid loan length provided."})




# Route to update a loan by ID
@app.route('/loans/<int:loan_id>/update', methods=["PUT"])
def update_loan(loan_id):
    data = request.json
    book_id = data.get("book_id")
    user_id = data.get("user_id")
    loan_date = data.get("loan_date")
    loan_length = data.get("loan_length")
    returned = data.get("returned")  # New field to specify return status


    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404


    # Check the previous return status before updating
    previous_returned = loan.returned
   
    if book_id:
        loan.book_id = book_id
    if user_id:
        loan.user_id = user_id
    if loan_date:
        loan.loan_date = loan_date
    if loan_length:
        loan.loan_length = loan_length
    if returned is not None:
        loan.returned = returned  # Update the return status


    db.session.commit()


    # Check if the return status has changed from False to True
    if not previous_returned and loan.returned:
        # The book has been returned, increase the stock of the relevant book by 1
        book = Book.query.get(loan.book_id)
        if book:
            book.stock += 1
            db.session.commit()


    return jsonify({"message": "Loan updated successfully"})




# Route to delete a loan by ID
@app.route('/loans/<int:loan_id>/delete', methods=["PUT"])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    loan.book_id = "DELETED LOAN"
    loan.user_id = "null"
    loan.loan_date = "null"
    loan.loan_length = "null"
    loan.returned = "null"
    db.session.commit()
    return jsonify({"message": "Loan deleted successfully"})

@app.route('/loans/<int:loan_id>/return', methods=["PUT"])
def return_book(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    # Assuming you have a boolean column in Loan model named `returned` which is False by default
    loan.returned = True
    # Update book stock
    book = Book.query.get(loan.book_id)
    book.stock += 1
    db.session.commit()
    return jsonify({"message": "Book returned successfully"})



#@app.route('/loans/late', methods=["GET"])
#def get_late_loans():
 #   current_date = datetime.utcnow()
  #  late_loans = Loan.query.filter(and_(
   #  Loan.loan_date + timedelta(days=Loan.loan_length) < current_date).all()

    #loans_list = [{
     #   "id": loan.id,
      #  "book_id": loan.book_id,
       # "user_id": loan.user_id,
        #"loan_date": loan.loan_date,
        #"loan_length": loan.loan_length,
        #"return_date": str(loan.return_date) if loan.return_date else None

    #} for loan in late_loans]

    #return jsonify({"late_loans": loans_list})

@app.route('/loans/late', methods=["GET"])
def get_late_loans():
    current_date = datetime.utcnow()

    # Fetch all the loans
    all_loans = Loan.query.all()

    # Filter out only the late loans using list comprehension
    late_loans = [
        loan for loan in all_loans
        if datetime.strptime(loan.loan_date, "%Y-%m-%d") + timedelta(days=loan.loan_length) < current_date
        and (loan.return_date is None or loan.return_date > current_date)
    ]

    loans_list = [{
        "id": loan.id,
        "book_id": loan.book_id,
        "user_id": loan.user_id,
        "loan_date": loan.loan_date,
        "loan_length": loan.loan_length,
        "return_date": str(loan.return_date) if loan.return_date else None
    } for loan in late_loans]

    return jsonify({"late_loans": loans_list})





if __name__ == '__main__':
    app.run(debug=True)


