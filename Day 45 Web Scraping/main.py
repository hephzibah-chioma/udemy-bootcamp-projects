from bs4 import BeautifulSoup
import requests

response = requests.get(url="https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
response.encoding = "utf-8"
empire_webpage = response.text

soup = BeautifulSoup(empire_webpage, "html.parser")
result = soup.find_all(name= "h3", class_= "title")
movies = [rank.getText() for rank in result]
movies.reverse()

with open("movies.txt", "w") as file:
    for movie in movies:
        file.write(f"{movie}\n")

