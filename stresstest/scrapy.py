import time

import requests
from bs4 import BeautifulSoup as bs
import re
import matplotlib.pyplot as plt
# from wordcloud import WordCloud

from lxml import etree

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
            'Accept-Language': 'en-US, en;q=0.5'})
# Deb: Traversal through the Flipkart pages to find the reviews
# taking input
print(
    " https://www.flipkart.com/realme-c35-glowing-green-64-gb/product-reviews/itmafb045222b2cf?pid=MOBGBTHFSKHF8RAU&lid=LSTMOBGBTHFSKHF8RAUQONXWY&marketplace=FLIPKART&page=")
webpagelink = input("please input web ulr in above format : ")
numrpages = input("please enter the number of review pages : ")

for i in range(1, int(numrpages)):
    # url = "https://www.flipkart.com/realme-c35-glowing-green-64-gb/product-reviews/itmafb045222b2cf?pid=MOBGBTHFSKHF8RAU&lid=LSTMOBGBTHFSKHF8RAUQONXWY&marketplace=FLIPKART&page=%d" % i
    # url="https://www.flipkart.com/realme-c35-glowing-green-64-gb/product-reviews/itmafb045222b2cf?pid=MOBGBTHFSKHF8RAU&lid=LSTMOBGBTHFSKHF8RAUQONXWY&marketplace=FLIPKART&page=%d" %i
    url = "https://www.flipkart.com/realme-c35-glowing-black-128-gb/product-reviews/itmafb045222b2cf?pid=MOBGBTHFZZN4ADNF&lid=LSTMOBGBTHFZZN4ADNFEGSZHG&aid=overall&certifiedBuyer=false&sortOrder=MOST_RECENT&page=13"
    url = webpagelink + str(i)
    print(url)
    response = requests.get(url)
    soup = bs(response.content, "html.parser")  # creating soup object to iterate over the extracted content

    # Deb: Parisng the page to find the reviews and ratings for it
    dom = etree.HTML(str(soup))
    time.sleep(2)
    for j in range(3, 11):
        st = "//*[@id=\"container\"]/div/div[3]/div/div[1]/div[2]/div[%d]/div/div/div/div[2]/div/div/div" % j
        rt = "//*[@id=\"container\"]/div/div[3]/div/div/div[2]/div[%d]/div/div/div/div[1]/div" % j
        title = "//*[@id=\"container\"]/div/div[3]/div/div/div[2]/div[%d]/div/div/div/div[1]/p" % j

        # print("Comment NO",i,":")
        try:
            reviews = dom.xpath(st)[0].text
            ratings = dom.xpath(rt)[0].text
            review_title = dom.xpath(title)[0].text

            print("Rating:", ratings, "Review", reviews, "TITLE:", review_title)
            # Deb: Writing the data on the file
            with open("Xiaomi.txt", 'a', encoding="utf-8") as file1:
                file1.write(review_title)
                file1.write("\n")
                file1.write(ratings)
                file1.write(":")
                file1.write(reviews)
                file1.write("\n")
        except IndexError as error:
            print("Error")
