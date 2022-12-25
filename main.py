import random 
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles

#Global Variables
app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/reviews", StaticFiles(directory="reviews"), name="reviews")
username = os.environ.get('PROXY_USER')
password = os.environ.get('PROXY_PASS')
product_title = ""
reviewList = []

# Models
class Product(BaseModel):
    url: str

### Routes ###

# Home
@app.get("/")
def read_root():
    return FileResponse("public/index.html")


@app.post("/product")
async def getProductProfile(product: Product):
  print(product.url)
  data = await extractProfile(product.url)
  return {"imageURL": data['imageURL'], "title": data['title']}


@app.post('/postURL')
async def fetchProduct(product: Product):
  print(product.url)
# Validate amazon url
# Extract reviews
  reviewFile = await fetchAndScrap(product.url)
  return reviewFile
  

### Amazon Scrapper ###

# Using Random Proxy
def getRandomProxy():

  proxy_list = [
    "185.199.229.156:7492",
    "185.199.228.220:7300",
    "185.199.231.45:8382",
    "188.74.210.207:6286",
    "188.74.183.10:8279",
    "188.74.210.21:6100",
    "45.155.68.129:8133",
    "154.95.36.199:6893",
    "45.94.47.66:8110",
    "144.168.217.88:8780",
  ]

  ipport = random.choice(proxy_list)

  proxy = {
    "http": f"http://{username}:{password}@{ipport}",
    "https": f"http://{username}:{password}@{ipport}"
  }
  # print(proxy)
  return proxy
  # response = requests.get('http://checker.soax.com/api/ipinfo', proxies=proxy)

async def extractReviews(reviewURL, pageNumber):
  resp = requests.get(reviewURL, proxies=getRandomProxy())
  
  soup = BeautifulSoup(resp.text, 'html.parser')
  # print(soup)
  reviews = soup.findAll('div',{'data-hook': "review"})
  # print(reviews)
  for item in reviews:
    # with open('outputs/file.html', 'w', encoding="utf-8") as f:
    #   f.write(str(item))
    review = {
      'productTitle': soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip(),
      'ReviewTitle': item.find('a', {'data-hook': 'review-title'}).text.strip(),
      'Rating': item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
      'Review body': item.find('span', {'class': 'a-size-base review-text review-text-content',
       'data-hook': 'review-body'}).text.strip(),
    }
    reviewList.append(review)
    # break # only get 1 review
  

async def getTotalPages(url):
  statuscode = 0
  attempts = 0
  global product_title

  while(statuscode != 200):
    print("Sending request...")
    resp = requests.get(url, proxies=getRandomProxy())
    print("Response Status:",resp.status_code)
    statuscode = resp.status_code
    attempts += 1
    if(attempts > 24):
      raise Exception("Out of proxy")
    
  
  soup = BeautifulSoup(resp.text, 'html.parser')
  

  totalReviews = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'})
  totalPages = totalReviews.text.strip().split(', ')[1].split(' ')[0]
  print("NEW TOTAL PAGES",totalPages)
  product_title = soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip()[0:16].replace(' ', '').replace(',', '')
 
  print("product title",product_title)
  return int(totalPages)

async def fetchAndScrap(productURL):
  productReviewURL = productURL.replace('/dp/', '/product-reviews/')
  print("SCRAPPING..",productReviewURL)
  totalPages = await getTotalPages(productReviewURL)
  print("TOTAL PAGES:", totalPages)

  print("Total Reviews: ",totalPages,"Total Pages:", totalPages//10)

  
  for i in range(totalPages//10):
    print(f"Scrapping for Page {i+1}/{totalPages//10}...")
    try:
      reviewURL = productReviewURL + '?pageNumber=' + str(i)
      await extractReviews(reviewURL, i)
    except Exception as e:
      print("Error occured", e)
    
  # print(reviewList)

  df = pd.DataFrame(reviewList)
  print("Product Title:", product_title)
  
  filename = product_title + '.xlsx'
  print("Saving to excel file...", filename)
  
  df.to_excel('reviews/'+filename, index=False)
  print("Reviews:", "Total Reviews scrapped:", len(reviewList))
  return {"result": "Total Reviews scrapped:" + str(len(reviewList)), "filename": filename}



async def extractProfile(url):
  statuscode = 0
  while(statuscode != 200):
    print("Sending request...")
    resp = requests.get(url, proxies=getRandomProxy())
    print("Response Status:",resp.status_code)
    statuscode = resp.status_code
  
  soup = BeautifulSoup(resp.text, 'html.parser')
  image = soup.find('img', {'id': 'landingImage'}).attrs['src']
  product_title = soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip()[0:64]
 
  print(image,product_title)

  mydict = {"imageURL": image, "title": product_title}
  print(mydict)
  return mydict


