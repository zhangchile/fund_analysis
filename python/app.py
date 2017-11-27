# this is app entry 

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://guba.eastmoney.com/news,of160222,730973591.html"

page = urlopen(url)

soup = BeautifulSoup(page)

print (soup.prettify())