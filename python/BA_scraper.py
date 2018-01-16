import re
import requests
from bs4 import BeautifulSoup
import dill
import sys
sys.setrecursionlimit(10000)  # to save beer reviews/profiles

# Code for scraping beer info from BeerAdvocate.com. Currently looking
# at only the top 250 beers found on:
# "https://www.beeradvocate.com/lists/top/"
#
# Returns html page/pages for each beer/reviews.

# Helper functions


def get_beer_links():
    # The url here is assumed to be "https://www.beeradvocate.com/lists/top/",
    # and this function returns links for all 250 beers
    # linked to on this page. Not be a very generalizable function.
    url = "https://www.beeradvocate.com/lists/top/"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    cells = soup.find_all("td", attrs={"class": "hr_bottom_light"})
    beer_stubs = [c.find_all("a")[0]['href'] for c in cells if c.find_all("a")]
    beer_links = []
    for i in beer_stubs:
        beer_links.append('https://www.beeradvocate.com' + i)
    return beer_links


def get_beer_profile(beer_link):
    # Get html of beer/profile page for beer link. bs4 object returned
    beer_profile = BeautifulSoup(requests.get(beer_link).text, 'html.parser')
    return beer_profile


def get_num_ratings(beer_soup):
    # Takes soup object of beer profile page and returns integer number of
    # ratings for the beer.
    ratings = beer_soup.find_all(class_="ba-ratings")  # bs4.element.ResultSet
    ratings = str(ratings[0])  # first result should be text with num ratings
    ratings = re.findall('(?<=>)(.*?)(?=<)', ratings)  # list with num ratings
    ratings = re.sub(',', '', str(ratings[0]))  # get rid of commas
    return int(ratings)


def get_beer_reviews(beer_link):
    # Scrape all beer reviews for a beer. The beer/profile page
    # contains a maximum of 25 comments. Which comments appear
    # is reflected in the URL of the page, e.g.
    # .../beer/profile/17981/110635/?view=beer&sort=&start=50
    # will display all the normal beer/profile stuff as well as
    # ratings/reviews 50 - 75. Here, we iterate through each page
    # and scrape ratings/reviews.
    beer_reviews = []
    soup = BeautifulSoup(requests.get(beer_link).text, 'html.parser')
    num_ratings = get_num_ratings(soup)

    num_pages = int(num_ratings / 25)  # 25 reviews per page
    for page_num in range(int(num_pages)):
        index = page_num * 25
        url = beer_link + '?view=beer&sort=&start=' + str(index)
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        beer_reviews.append(soup)

    return beer_reviews


# MAIN

beer_links = get_beer_links()  # Get links from top 250 beer page

count = 1
for i in beer_links:
    profile = get_beer_profile(i)
    reviews = get_beer_reviews(i)
    dill.dump(profile, open('rbp_' + str(count) + '.pkd', 'w'))
    dill.dump(reviews, open('rbr_' + str(count) + '.pkd', 'w'))
    count += 1
