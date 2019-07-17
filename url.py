from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from flask_restful import Resource
from bs4 import BeautifulSoup
import json
from flask import  request
import requests
import time

class Url(Resource):

  def get(self):
    url = request.args.get('url')
    return scrape(url)

def getBeautifulSoup_viaBrowser(url, delay=0):
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
  driver.set_window_size(1120, 850)
  driver.get(url)
  time.sleep(delay)
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  driver.quit()
  return soup

def getBeautifulSoup_viaGet(url):
  response = requests.get(url)
  return BeautifulSoup(response.text, 'html.parser')

def scrapeCastorama(url):
  soup = getBeautifulSoup(url)
  the_title = soup.find("meta", property="og:title").get('content')
  the_url = soup.find("meta", property="og:url").get('content')
  the_image = soup.find("meta", property="og:image").get('content')
  the_description = soup.find("meta", attrs={'name': "description"}).get('content')
  the_price = soup.find("meta", itemprop="price").get('content')
  the_priceCurrency = soup.find("meta", itemprop="priceCurrency").get('content')

  data = {
    'label': the_title,
    'url': the_url,
    'images': [
      the_image
    ],
    'price': {
      'amount': the_price,
      'currency': the_priceCurrency
    },
    'extra_data': {
      'description': the_description
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
    the_title = product['name']
    the_url = product['url']
    the_image = product['image']
    the_description = product['description']
    the_price = product['offers']['price']
    the_priceCurrency = product['offers']['priceCurrency']
    data = {
      'label': the_title,
      'url': the_url,
      'images': [
        the_image
      ],
      'price': {
        'amount': the_price,
        'currency': the_priceCurrency
      },
      'extra_data': {
        'description': the_description
      }
    }
  return data

def scrapeAmazon(url):
  soup = getBeautifulSoup(url)
  data_metrics = soup.find("div", id="cerberus-data-metrics")

  the_price = data_metrics.get('data-asin-price')
  the_priceCurrency = data_metrics.get('data-asin-currency-code')
  the_description = soup.find("meta", attrs={'name': 'description'}).get('content')
  the_title = soup.find("meta", attrs={'name': 'title'}).get('content')
  the_url = url
  the_image = soup.find("img", id="landingImage").get('src')

  data = {
    'label': the_title,
    'url': the_url,
    'images': [
      the_image
    ],
    'price': {
      'amount': the_price,
      'currency': the_priceCurrency
    },
    'extra_data': {
      'description': the_description
    }
  }

  return data

def getBeautifulSoup(url):
  return getBeautifulSoup_viaGet(url)

def scrape(url):
  data = {
    "error": "This website is not yet covered by scraping"
  }
  if 'castorama.fr' in url:
    data = scrapeCastorama(url)
  elif 'leroymerlin.fr' in url:
    data = scrapeLeroyMerlin(url)
  elif 'amazon.fr' in url:
    data = scrapeAmazon(url)
  elif 'amazon.com' in url:
    data = scrapeAmazon(url)
  # LMES doesn't work :
  # - no "og:image"      meta tag
  # - no "price"         meta tag
  # - no "priceCurrency" meta tag
  #    elif 'leroymerlin.es'            in url:
  #        data = scrapeCastorama(url)
  return data