# MISSION TO MARS SCRAPING PROJECT #

# Project dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo


# Function to point to the chromedriver in Misstion_to_Mars folder
def init_browser():
    executable_path = {'executable_path':"C:\\Users\\dwint\\web-scraping-challenge\\Mission_to_Mars\\chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

# Declare Scrape function and create Mission_to_Mars Dictionary
def scrape():
    browser = init_browser()
    mars_data = {}

    # SCRAPE MARS NEWS #
    # Visit and scrape NASA Mars News url 
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)

    # Create html object and parse with BeautifulSoup
    html_article = browser.html
    soup = BeautifulSoup(html_article, 'html.parser')

    # Scrape and print the latest Mars news title and paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Place Mars info into Data Dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p


    # SCRAPE MARS IMAGES # 
    # Visit and scrape NASA JPL space images
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)

    # Create html object and parse with BeautifulSoup
    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')

    # Scrape image url from the style tag 
    mars_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Main website url 
    main_url = "https://www.jpl.nasa.gov"

    # Combine main website url with scrapped image url
    featured_image_url = main_url + mars_image_url

    # Display image
    featured_image_url

    # Place Mars image into Data Dictionary
    mars_data['featured_image_url'] = featured_image_url


    # SCRAPE MARS WEATHER # 
    # Visit and scrape Mars weather twitter
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)

    # Create html object and parse with BeautifulSoup
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Scrape and print recent Mars weather
    mars_tweet = soup.find('div', class_='js-tweet-text-container')
    mars_weather = mars_tweet.p.text 

    # Display image
    mars_weather

    # Place Mars image into Data Dictionary
    mars_data['mars_weather'] = mars_weather


    # SCRAPE MARS FACTS # 
    # Visit and scrape Mars facts at https://space-facts.com/mars/ using pandas
    mars_facts_df = pd.read_html('https://space-facts.com/mars/')[2]

    # Use Mars facts to create DataFrame
    mars_facts_df.columns=["Mars Feature", "Fact"]

    # Convert DataFrame to html
    mars_facts_df = mars_facts_df.to_html()

    # Place Mars facts
    mars_data['mars_table'] = mars_facts_df


    # SCRAPE MARS HEMISPHERE IMAGES #
    # Visit the US Astrogeology website using splinter
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    # Create html object and parse with BeautifulSoup
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Create a Hemisphere Image list using the dictionary for each hemisphere title and image url string. 
    # Hemisphere Image list code fashioned after coding by vabigdatamover @ https://github.com/vabigdatamover/web-scraping-challenge/blob/master/Missions_to_Mars/mission_to_mars.ipynb
    hemisphere_image_list = []

    hemisphere_titles = soup.find_all('h3')

    for i in range(len(hemisphere_titles)):
        hemisphere_title = hemisphere_titles[i].text
        print(hemisphere_title)
    
        hemisphere_images = browser.find_by_tag('h3')
        hemisphere_images[i].click()
    
        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
    
        hemi_img_url = soup.find('img', class_='wide-image')['src']
        hemi_img_url = "https://astrogeology.usgs.gov" + hemi_img_url
        print(hemi_img_url)
    
        hemisphere_dict = {"title": hemisphere_title, "img_url":hemi_img_url}
        hemisphere_image_list.append(hemisphere_dict)
    
        browser.back()

        mars_data['hemisphere_image_list'] = hemisphere_image_list

        browser.quit()

        # Display mars_data dictionary
        return mars_data

