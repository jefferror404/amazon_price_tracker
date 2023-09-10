import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

my_email = "YOUR EMAIL"
password = "YOUR PASSWORD"

#Check your httpheader details using the link below:
#https://myhttpheader.com/

headers = {
    "User-Agent": "YOUR USER AGENT",
    "Accept": "YOUR ACCEPT",
    "authority": "www.amazon.com",
    "pragma": "no-cache",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "Accept-Language": "YOUR ACCEPT LANGUAGE",

}
amazon_url = "https://www.amazon.de/-/en/VS15A6031R1-EG-cordless-handheld-replaceable/dp/B0933MJBZ7/ref=sr_1_4?crid=2FNXPGYLXVXAR&keywords=samsung+vacuum&qid=1694344581&sprefix=samsung+vacuum%2Caps%2C107&sr=8-4"

response = requests.get(url=amazon_url, headers=headers)
amazon_site = response.text
#print(amazon_site)

soup = BeautifulSoup(amazon_site, "lxml")
price_whole = float(soup.find("span", class_="a-price-whole").getText().split(".")[0].replace(",", ""))
price_fraction = float(soup.find("span", class_="a-price-fraction").getText())
print(price_whole)
print(price_fraction)
price = price_whole + price_fraction/100
print(price)

product_name = soup.find("span", id="productTitle", class_="a-size-large product-title-word-break").getText().strip()
print(product_name)

target_price = 270
#Use the below link to search for the historical price trend of your target product
# and set your target price for the price alert
#https://camelcamelcamel.com/

if price < target_price:
    message = f"{product_name} is now {price}."
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{amazon_url}".encode("utf-8")
                            )
