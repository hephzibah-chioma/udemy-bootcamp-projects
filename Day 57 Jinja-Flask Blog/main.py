from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)
post = Post()

@app.route('/')
def home():
    all_posts = post.get_posts()
    first_post = all_posts[0]
    second_post = all_posts[1]
    third_post = all_posts[2]
    return render_template("index.html", first= first_post, second= second_post, third= third_post)

@app.route("/post/<num>")
def to_post(num):
    all_posts = post.get_posts()
    first_post = all_posts[0]
    second_post = all_posts[1]
    third_post = all_posts[2]
    return render_template("post.html", num= num, first= first_post, second= second_post, third= third_post)


if __name__ == "__main__":
    app.run(debug=True)
