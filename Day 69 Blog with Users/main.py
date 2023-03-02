from flask import Flask, render_template, redirect, url_for, flash, request, session, abort
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LogInForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
from dotenv import load_dotenv, dotenv_values
import os
import gunicorn

load_dotenv("C:/Users/HP/Documents/GitHub/100-days-of-coding/Day 69 Blog with Users/environment.env")
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
ckeditor = CKEditor(app)
Bootstrap5(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##CONFIGURE TABLES

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    author = relationship("User", back_populates="comments")
    parent_post = relationship("BlogPost", back_populates="comments")
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, user= current_user, logged_in= current_user.is_authenticated)


@app.route('/register', methods= ["GET", "POST"])
def register():
    form= RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with app.app_context():
                new_user = User(
                    email= request.form["email"],
                    password = generate_password_hash(password= request.form["password"], method= "pbkdf2:sha256", salt_length= 8),
                    name = request.form["name"]
                )
            all_users = db.session.query(User).all()
            all_emails = [user.email for user in all_users]
            if request.form["email"] in all_emails:
                flash("You've already signed up with that email. Please log in instead.")
                return redirect(url_for('login'))
            else:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('get_all_posts'))
    return render_template("register.html", form= form, logged_in= current_user.is_authenticated)


@app.route('/login', methods= ["GET", "POST"])
def login():
    form = LogInForm()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        with app.app_context():
            user_to_check = User.query.filter_by(email= email).first()
            if user_to_check is None:
                flash("That email is not registered. Please try again.")
            else:
                check_password = check_password_hash(pwhash=user_to_check.password, password= password)
                session["username"] = user_to_check.name
                if check_password:
                    login_user(user= user_to_check)
                    return redirect(url_for('get_all_posts'))
                else:
                    flash("Password incorrect. Please try again.")
    return render_template("login.html", form=form, logged_in= current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods= ["GET", "POST"])
def show_post(post_id):
    form= CommentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if current_user.is_authenticated:
                with app.app_context():
                    new_comment = Comment(
                        text= request.form["comment"]
                    )
                    db.session.add(new_comment)
                    db.session.commit()
                return redirect(url_for('show_post', post_id= post_id))
            else:
                flash("Please log in to be able to submit a comment.")
                return redirect(url_for('login'))
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post, user= current_user, form= form, logged_in= current_user.is_authenticated)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods= ["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with app.app_context():
                new_post = BlogPost(
                    title=form.title.data,
                    subtitle=form.subtitle.data,
                    body=form.body.data,
                    img_url=form.img_url.data,
                    author=current_user,
                    date=date.today().strftime("%B %d, %Y")
                )
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in= True)


@app.route("/edit-post/<int:post_id>")
@admin_only
def edit_post(post_id):
    with app.app_context():
        post = BlogPost.query.get(post_id)
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
        )
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.subtitle = edit_form.subtitle.data
            post.img_url = edit_form.img_url.data
            post.author = edit_form.author.data
            post.body = edit_form.body.data
            db.session.commit()
            return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit= True, logged_in= True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    with app.app_context():
        post_to_delete = BlogPost.query.get(post_id)
        db.session.delete(post_to_delete)
        db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug= True)
