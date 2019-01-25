import instaloader
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import glob
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from autocorrect import spell
from nltk import tokenize


# Get instance
L = instaloader.Instaloader()

# put-in the hastag for which you would like to get the posts
h = 'YemenEnquiryNow'
hh = '#YemenEnquiryNow'
i = 0
for post in L.get_hashtag_posts(h):
	if i >500:
		break
	L.download_post(post, target= hh)
	i+=1
