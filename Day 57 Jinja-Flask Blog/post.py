import requests


class Post:
    def __init__(self):
        blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
        response = requests.get(url= blog_url)
        all_posts = response.json()
        self.all_posts = all_posts

    def get_posts(self):
        posts = self.all_posts
        return posts