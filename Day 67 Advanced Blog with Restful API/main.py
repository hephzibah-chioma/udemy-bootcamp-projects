from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime
import calendar


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")



@app.route('/')
def get_all_posts():
    with app.app_context(): 
        posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)

# {{url_for('edit_post', post_id=post.id)}}
@app.route("/post/<int:index>")
def show_post(index):
    with app.app_context():
        requested_post = BlogPost.query.filter_by(id= index).first()
        return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/new-post", methods= ["GET", "POST"])    
def new_post():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            blog_title = form.title.data
            blog_subtitle = form.subtitle.data
            blog_author = form.author.data
            blog_img_url = form.img_url.data
            blog_body = form.body.data
            today = datetime.now()
            blog_date = f"{calendar.month_name[today.month]} {today.day}, {today.year}"
            with app.app_context():
                blog_post = BlogPost(title= blog_title, subtitle= blog_subtitle, author= blog_author, date= blog_date, img_url= blog_img_url, body= blog_body)
                db.session.add(blog_post)
                db.session.commit()
            return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form= form, h1= "New Post")

@app.route("/edit-post/<post_id>", methods= ["GET", "POST"])
def edit_post(post_id):
    with app.app_context():
            post_to_edit = BlogPost.query.filter_by(id= post_id).first()
            form = CreatePostForm(title= post_to_edit.title,
                                  subtitle= post_to_edit.subtitle,
                                  author= post_to_edit.author,
                                  img_url= post_to_edit.img_url,
                                  body= post_to_edit.body)
    if request.method == "POST":
        if form.validate_on_submit():
            with app.app_context():
                post_to_edit = BlogPost.query.filter_by(id= post_id).first()
                post_to_edit.title = form.title.data
                post_to_edit.subtitle = form.subtitle.data
                post_to_edit.author = form.author.data
                post_to_edit.img_url = form.img_url.data
                post_to_edit.body = form.body.data
                db.session.commit()
            return redirect(url_for('show_post', index= post_id))
    return render_template('make-post.html',form= form, h1= "Edit Post")

@app.route("/delete/<id>")
def delete_post(id):
    with app.app_context():
        post_to_delete = BlogPost.query.filter_by(id=id).first()
        db.session.delete(post_to_delete)
        db.session.commit()
    return redirect(url_for('get_all_posts'))

if __name__ == "__main__":
    app.run(debug=True)