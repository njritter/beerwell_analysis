import re
import bs4
import dill


# Beer class

class Beer:
    ''' A beer class '''
    def __init__(self, beer_profile, beer_reviews):
        self.name = 'hai'
        self.brewery = 'there'
        self.abv = 0
        self.num_reviews = 0
        self.num_ratings = 0
        self.ratings = []
        self.reviews = []
        self.vector = []

    def get_reviews_from_page(page):
        pass

    def clean_raw_review(raw_review):  # Clean single raw review
        # Deal with reviews that have newlines ... this could prob be better
        myStringList = str(raw_review).splitlines()
        myBigStr = ''
        for i in myStringList:
            myBigStr = myBigStr + ' ' + i

        # Regex pattern that seems to get review text with not too much noise
        REV_RE = re.compile(r'(?<=<\/span><br><br>)(.*?)(?=<br><br>)')
        matches = REV_RE.findall(myBigStr)
        clean_review = ' '.join(matches)

        return clean_review


# ABV
# BA Score

# Average Vector Description
# 10? highly relevant features from vector
# matches = re.findall('(?<=<\/span><br><br>)(.*?)(?=<br><br>)', myBigStr)


# Addition (of other beers and particular words)
# Subtraction
