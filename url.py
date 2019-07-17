from flask_restful import Resource
from bs4 import BeautifulSoup
import re
import json
from flask import  request
import requests

class Url(Resource):

  def get(self):
    url = request.args.get('url')
    return scrape(url)



  def getBeautifulSoup_viaBrowser(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
    driver.set_window_size(1120, 850)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()


def getBeautifulSoup_viaGet(url):
  response = requests.get(url)
  return BeautifulSoup(response.text, 'html.parser')


def scrapeCastorama(url):
  soup = getBeautifulSoup(url)
  title = soup.find("meta", property="og:title")
  url = soup.find("meta", property="og:url")
  image = soup.find("meta", property="og:image")
  description = soup.find("meta", attrs={'name': "description"})
  price = soup.find("meta", itemprop="price")
  priceCurrency = soup.find("meta", itemprop="priceCurrency")

  data = {
    'label': title.get('content'),
    'url': url.get('content'),
    'images': [
      image.get('content')
    ],
    'price': {
      'amount': price.get('content'),
      'currency': priceCurrency.get('content')
    },
    'extra_data': {
      'description': description.get('content')
    }
  }

  return data


def scrapeLeroyMerlin(url):
  soup = getBeautifulSoup(url)
  metadata = soup.findAll("script", type="application/ld+json")

  product = None
  for meta in metadata:
    meta_json = json.loads(meta.text)
    if '@type' in meta_json and meta_json['@type'] == "Product":
      product = meta_json

  data = None
  if product is not None:
    data = {
      'label': product['name'],
      'url': product['url'],
      'images': [
        product['image']
      ],
      'price': {
        'amount': product['offers']['price'],
        'currency': product['offers']['priceCurrency']
      },
      'extra_data': {
        'description': product['description']
      }
    }
  return data


def getBeautifulSoup(url):
  return getBeautifulSoup_viaGet(url)


def scrape(url):
  data = None
  if 'castorama.fr' in url:
    data = scrapeCastorama(url)
  elif 'leroymerlin.fr' in url:
    data = scrapeLeroyMerlin(url)
  return data