from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs


def mars_hemi(hemisphere, browser):
    
    url_hemisphere="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)
    browser.click_link_by_partial_text(hemisphere)
    html=browser.html
    soup=bs(html, "html.parser")
    hemi=soup.find("div", class_="downloads")
    hemi_img=hemi.find("a")
    return hemi_img["href"]

def scrape():
    executable_path={"executable_path": "/usr/local/bin/chromedriver"}
    browser=Browser("chrome", **executable_path, headless=False)

    #article title
    url="https://mars.nasa.gov/news/"
    browser.visit(url)
    html=browser.html
    soup=bs(html, "html.parser")
    title=soup.find("div", class_="content_title").text
    #article paragraph
    browser.click_link_by_text(title)
    html=browser.html
    soup=bs(html, "html.parser")
    paragraph=soup.find("div", class_="wysiwyg_content")
    para=paragraph.find('p').text

    #mars picture
    url_image="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    home_url='https://www.jpl.nasa.gov'
    browser.visit(url_image)
    html=browser.html
    soup=bs(html, "html.parser")
    mars_img=soup.find("li", class_="slide")
    mars_src=mars_img.find("a")
    mars_src["data-fancybox-href"]
    featured_image_url=home_url+mars_src["data-fancybox-href"]

    #mars weather
    url_weather="https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html=browser.html
    soup=bs(html, "html.parser")
    mars_w=soup.find("div", class_="js-tweet-text-container").text.rstrip()

    #mars facts
    facts_url="https://space-facts.com/mars/"
    mars_table=pd.read_html(facts_url)
    df=mars_table[0]
    df.columns=["Measurements","Values"]
    df_facts=df.set_index('Measurements')
    mars_facts=df_facts.to_html()
    mars_facts_final=mars_facts.replace('\n','')

    #mars hemisphere
    cerberus_link=mars_hemi("Cerberus", browser)
    schiaparelli_link=mars_hemi("Schiaparelli", browser)
    syrtis_major_link=mars_hemi("Syrtis Major",browser)
    valles_marineris_link=mars_hemi("Valles Marineris", browser)

    hemisphere_image_urls=[
    {"title": "Valles_Marineris_Hemisphere", "img_url":valles_marineris_link},
    {"title": "Cerberus_Hemisphere", "img_url":cerberus_link},
    {"title": "Shiaparelli_Hemisphere", "img_url":schiaparelli_link},
    {"title": "Syrtis_Major_Hemisphere", "img_url": syrtis_major_link}
    ]

    mars_data={
        "title":title,
        "paragraph":para,
        "mars_pic":featured_image_url,
        "mars_weather":mars_w,
        "mars_facts":mars_facts_final,
        hemisphere_image_urls[0]["title"]:hemisphere_image_urls[0]["img_url"],
        hemisphere_image_urls[1]["title"]:hemisphere_image_urls[1]["img_url"],
        hemisphere_image_urls[2]["title"]:hemisphere_image_urls[2]["img_url"],
        hemisphere_image_urls[3]["title"]:hemisphere_image_urls[3]["img_url"]
    }

    return mars_data

