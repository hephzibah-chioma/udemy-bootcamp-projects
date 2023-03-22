from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap5(app)
app.secret_key = "mysupersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)

# all_books = []

class Books(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(250), unique= True, nullable= False)
    author = db.Column(db.String(250), nullable= False)
    rating = db.Column(db.Float, nullable= False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods= ["POST", "GET"])
def add():
    if request.method == "POST":
        book_dict = request.form.to_dict()
        # all_books.append(book_dict)
        book_title = book_dict["title"]
        book_author = book_dict["author"]
        book_rating = book_dict["rating"]
        new_book_entry = Books(title=book_title, author=book_author, rating=book_rating)
        with app.app_context():
            db.session.add(new_book_entry)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        with app.app_context():
            book = Books.query.filter_by(id= id).first()
            book.rating = request.form["new_rating"]
            db.session.commit()
        return redirect(url_for('home'))
    book = Books.query.filter_by(id= id).first()
    return render_template('edit.html', book = book)

@app.route('/<id>')
def delete(id):
    with app.app_context():
        book = Books.query.filter_by(id= id).first()
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

