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

    soup = BeautifulSoup(page.text, 'html.parser')
    #num = soup.find('a', attrs={'class':'btn disabled'})
    #btn btn-default / btn disabled
    links = soup.find_all('a', attrs={'class':'btn disabled'}, href=True)
    for l in links:
        print (l['href'])

# Test for a new branch
