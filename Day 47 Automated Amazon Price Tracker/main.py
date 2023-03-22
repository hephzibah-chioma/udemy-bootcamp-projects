import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

product_url = "https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B08MVGF24M/ref=sr_1_3?crid=ACZWAF4GTHZD&keywords=sony%2Bwh-1000xm4&qid=1673972334&sprefix=sony%2B%2Caps%2C594&sr=8-3&th=1"
product = product_url.split("/")[3]

http_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
}

response = requests.get(url= product_url, headers= http_header)
amazon_data = response.text

soup = BeautifulSoup(amazon_data, "lxml")
price = float(soup.find(class_ = "a-offscreen").getText().split("$")[1])

my_email = "hephzi2002.udo@gmail.com"
my_password = "msjmixgprwjntnye"

if price < 200:
    with smtplib.SMTP("smtp.gmail.com") as server:
        server.starttls()
        server.login(user=my_email, password=my_password)
        server.sendmail(from_addr=my_email, to_addrs=my_email, msg= f"Subject: Amazon Price Alert!\n{product} is now {price}!\n{product_url}")