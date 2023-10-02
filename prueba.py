import requests
from bs4 import BeautifulSoup
import json
from flask import Flask
from selenium import webdriver
from pymongo import MongoClient
from bson.json_util import dumps


driver = webdriver.Chrome()

url = 'http://quotes.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

data = {'quotes': []}
quotes_divs = soup.find_all(class_='quote')

for quote_div in quotes_divs:
    text = quote_div.find(class_='text').get_text()
    author = quote_div.find(class_='author').get_text()
    tags = [tag.get_text() for tag in quote_div.find_all(class_='tag')]

    data['quotes'].append({
        'text': text,
        'author': author,
        'tags': tags
    })

with open('quotes.json', 'w') as f:
    json.dump(data, f)
driver.quit()


# Conexión a la base de datos
url = "mongodb+srv://Angela:Angie123@cluster0.lik93ug.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
db = client["prueba"]
collection = db["Angela"]

# Carga los datos del archivo .json
with open('quotes.json', 'r') as f:
    data = json.load(f)

collection.insert_one(data)

app = Flask(__name__)
MONGO_URI = "mongodb+srv://Angela:Angie123@cluster0.lik93ug.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)


@app.route('/')
def home():
    url = "mongodb+srv://Angela:Angie123@cluster0.lik93ug.mongodb.net/?retryWrites=true&w=majority"
    cliente = MongoClient(url)
    db = cliente["prueba"]
    collections = db["Angela"]

    data = list(collections.find())

    return dumps(data)


if __name__ == '__main__':
    app.run(debug=True)