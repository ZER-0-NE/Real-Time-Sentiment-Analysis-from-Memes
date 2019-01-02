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
h = 'MeToo'
hh = '#MeToo'
# for post in L.get_hashtag_posts(h):
#     # post is an instance of instaloader.Post
#     L.download_post(post, target= hh)

#os.chdir("#metoo")
img = glob.glob("*.jpg") + glob.glob("*.png") + glob.glob("*.jpeg")
for im in img:
	image = cv2.imread(im)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	cv2.imshow("Image", gray)

	# check to see if we should apply thresholding to preprocess the image
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	# make a check to see if median blurring should be done to remove
	# noise
	# gray = cv2.medianBlur(gray, 3)

	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)

	extracted = []
	extracted.append(text)
	map(str.strip, extracted)
	extracted = [a.replace(';', ' ').replace('.', ' ').replace('\n', ' ') for a in extracted]
	# determining whether we are working with a sentence or a paragraph
	num_words = [int(len(sen.split())) for sen in extracted]
	map(str, num_words)
	#print(extracted)
	#print(num_words)

	if num_words[0] <= 20 and num_words[0] > 3:
		analyzer = SentimentIntensityAnalyzer()
		for sentence in extracted:
			vs = analyzer.polarity_scores(sentence)
			print(" SENTIMENT FOR THE SENTENCE /t {:-<65} {}".format(sentence, str(vs)))
	if num_words[0] > 20:
		extracted = str(extracted)
		analyzer = SentimentIntensityAnalyzer()
		sentence_list = tokenize.sent_tokenize(extracted)
		paragraphSentiments = 0.0
		for sentence in sentence_list:
			vs = analyzer.polarity_scores(sentence)
			print("{:-<69} {}".format(sentence, str(vs["compound"])))
			paragraphSentiments += vs["compound"]
			print("AVERAGE SENTIMENT FOR PARAGRAPH: \t" + str(round(paragraphSentiments / len(sentence_list), 4)))






