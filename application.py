
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)

# Connect to the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Create the Book database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    # Convert book information into a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "book_name": self.book_name,
            "author": self.author,
            "publisher": self.publisher
        }

# Create the database tables
with app.app_context():
    db.create_all()

# GET - Retrieve all books
@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()

    book_list = []

    for book in books:
        book_list.append(book.to_dict())

    return jsonify(book_list)

# GET - Retrieve one book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)

    return jsonify(book.to_dict())

# POST - Add a new book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    if not data or not all(key in data for key in ["book_name", "author", "publisher"]):
        return jsonify({"message": "Missing book information"}), 400

    new_book = Book(
        book_name=data["book_name"],
        author=data["author"],
        publisher=data["publisher"]
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dict()), 201

# PUT - Update an existing book
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)

    data = request.get_json()

    book.book_name = data["book_name"]
    book.author = data["author"]
    book.publisher = data["publisher"]

    db.session.commit()

    return jsonify(book.to_dict())

# DELETE - Remove a book
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"})
if __name__ == "__main__":
    app.run(debug=True)