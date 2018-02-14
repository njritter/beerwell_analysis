
# PURPOSE: Save cleaned text reviews from each beer into a text file. Seems
# like most convenient form to have text data in for NLP libraries.
#
# INPUT: A .pkd with list of review pages (soup objects) for a beer
# OUTPUT: A list of cleaned beer reviews (strings) ... or write to text file.
#
# Notes:
#

import bs4
import re
import dill


def get_unclean_reviews_from_page(beerSoup):
    unclean_reviews = beerSoup.select('#rating_fullview_content_2')
    return unclean_reviews


def remove_newlines(unclean_review):
    myStringList = str(unclean_review).splitlines()
    myReviewsString = ''
    for i in myStringList:
        myReviewsString = myReviewsString + ' ' + i
    return myReviewsString


def get_indiv_reviews(reviews):
    myReviews = []
    matches = re.findall('rating_fullview_content_2(.*?)"username"', reviews)
    for i in matches:
        myReviews.append(i)
    return myReviews


def get_reviews_with_text(indiv_reviews):
    reviews_with_text = []
    for i in indiv_reviews:
        if re.search('characters', i):
            reviews_with_text.append(i)
    return reviews_with_text


def clean_reviews(reviews_with_text):
    clean_reviews = []
    for i in reviews_with_text:
        clean_review = re.findall('<br\/><br\/>(.*?)<br\/><br\/>', i)
        if clean_review:
            clean_reviews.append(clean_review)
    return clean_reviews


def get_clean_reviews_from_page(beerSoup):
    # INPUT: bs4 object of html page with beer reviews
    # OUTPUT: List of text from reviews on page
    unclean_reviews = get_unclean_reviews_from_page(beerSoup)
    less_unclean_reviews = remove_newlines(unclean_reviews)
    indiv_unclean_reviews = get_indiv_reviews(less_unclean_reviews)
    unclean_reviews_with_text = get_reviews_with_text(indiv_unclean_reviews)
    list_of_clean_reviews = clean_reviews(unclean_reviews_with_text)
    return list_of_clean_reviews


def get_clean_reviews_for_beer(beer_review_soups):
    # Pull out all cleaned text reviews for a beer
    all_clean_reviews = []
    for i in beer_review_soups:
        clean_reviews = get_clean_reviews_from_page(i)
        for j in clean_reviews:
            myString = j[0]
            myString = myString.replace('<br>', '') # remove '<br>''
            all_clean_reviews.append([myString]) # not 100% sure why [] needed
    return all_clean_reviews


# Main

# Load raw beer profiles. The rbr_???.pkd files are pickled lists of bs4
# objects of each review page for a beer.
path = '/Users/Drazi/Dropbox/beerwell_data/data/rbr/rbr_'

for i in range(1, 251):
    beer_review_soups = dill.load(open(path + str(i) + '.pkd', 'rb'))
    # Pull out all cleaned text reviews for a beer
    all_clean_reviews = get_clean_reviews_for_beer(beer_review_soups)
    # Write reviews for beer to text file.
    f = open('reviews_' + str(i) + '.txt', 'w')
    for i in all_clean_reviews:
        f.write(i[0] + '\n')
