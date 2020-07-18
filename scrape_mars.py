from bs4 import BeautifulSoup as bs
from splinter import Browser


import re
import pandas as pd
import time


def _init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scraper():

    browser = _init_browser()


    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)
    time.sleep(2)


    html = browser.html
    soup = bs(html, 'html.parser')
    news = soup.find('ul',class_='item_list').find('li', class_='slide')
    title = news.find('div', class_='content_title').text
    #title
    news_content = news.find('div', class_='article_teaser_body').text
    #news_content


    #Getting featured photo from JPL

    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    time.sleep(2)

    html = browser.html
    soup= bs(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_path = soup.find('img', class_='fancybox-image')['src']
    image_url = 'https://www.jpl.nasa.gov' + image_path
    #image_url

    #Twitter Scrape
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = bs(html, 'html.parser')
    weather = soup.find('span', text = re.compile('InSight sol')).text
    weather = weather.replace('InSight s', 'S') 
    #weather


    #Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(2)   

    html = browser.html

    table = pd.read_html(html)
    #table

    mars_facts_df = pd.DataFrame(table[0])
    mars_facts_df = mars_facts_df.rename(columns = {0: 'Description', 1: 'Value'})
    mars_facts_df = mars_facts_df.set_index('Description')

    mars_facts_df.index.name=None

    mars_facts_htmltable = mars_facts_df.to_html(header =False)
    mars_facts_htmltable = mars_facts_htmltable.replace('\n','')
    #mars_facts_htmltable


    #Hemisphere Images Scrape
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(2)

    html = browser.html

    soup = bs(html,'html.parser')
    #soup

    hemi_names = []
    hemi_urls = []
    count = 0


    result = soup.find_all('a', class_='itemLink product-item')
    result


    for a in result:
        try:
            hemi_name=a.find('h3').text
            hemi_names.append(hemi_name)
        except:
            count +=1
            
    #hemi_names

    for name in hemi_names:
        
        time.sleep(2)
        
        hemi_dict = {}
        
        browser.click_link_by_partial_text(name)
        time.sleep(2)
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        image_path = soup.find('img', class_='wide-image')['src']
        
        image_url = 'https://astrogeology.usgs.gov' + image_path
        
        hemi_dict['Title'] = name
        hemi_dict['url']=image_url
        
        hemi_urls.append(hemi_dict)
        
        browser.back()
        

        meta_data = {}

    meta_data['title'] = title
    meta_data['content']= news_content
    meta_data['featured_image']= image_url
    meta_data['weather'] = weather
    meta_data['facts']=mars_facts_htmltable
    meta_data['hemisphere_images']=hemi_urls


    return(meta_data)