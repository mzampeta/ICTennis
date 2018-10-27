import requests
import os
from bs4 import BeautifulSoup

my_username = os.environ.get('IC_USER')
my_password = os.environ.get('IC_PASS')

with requests.Session() as c:
    url = 'https://union.ic.ac.uk/acc/tennis/booking/login'
    c.get(url)
    payload = {'cid_user': my_username, 'cid_pass': my_password}
    c.post(url, data=payload)
    page = c.get('https://union.ic.ac.uk/acc/tennis/booking')
#Start scrapping
soup = BeautifulSoup(page.text, 'html.parser')
#num = soup.find('a', attrs={'class':'btn disabled'})
tables = soup.find_all('table')
for t in tables:
    #to find the parent tag and display DATA
    for trs in t.find_all('tr'):
        tds = trs.find_all('td')
        print (tds[1].text+" level at "+tds[0].text+" is: "+tds[3].text)
