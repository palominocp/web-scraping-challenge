from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {'executable_path': '/Users/cpalo_000/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # NASA Mars News
    browser = init_browser()
    mars_data = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_section = soup.find('ul', class_='item_list')

    mars_data['news_title'] = news_section.find('h3').text
    mars_data['news_p'] = news_section.find(class_='rollover_description_inner').text

    # JPL Mars Space Images - Featured Image

    main_url = 'https://www.jpl.nasa.gov'
    url = main_url + '/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(10)

    html = browser.html
    soup = bs(html, 'html.parser')

    feat_img = soup.find('a', class_='button fancybox')

    mars_data['featured_image_url'] = main_url + feat_img.get('data-fancybox-href')

    # Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(10)

    html = browser.html
    soup = bs(html, 'html.parser')

    weather = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

    mars_data['mars_weather'] = weather[0].text

    # Mars Facts

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    url = 'https://space-facts.com/mars/'
    # Use Panda's 'read_html' to parse the url
    tables = pd.read_html(url)
    # Use Pandas to convert the data to a HTML table string
    mars_data['facts_html'] = pd.DataFrame.to_html(tables[0])

    # Mars Hemispheres

    urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    
    titles = ['Valles Marineris Hemisphere', 'Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere']

    i = 0
    hemisphere_image_urls = []
    for url in urls:
        print(url)
        browser.visit(url)
        time.sleep(10)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_full = soup.find('div', class_='downloads')
        targetimg = img_full.find_all('li')
        hemisphere_image_urls.append({'title': titles[i], 'img_url': targetimg[0].find('a').get('href')})
        i = i + 1
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_data