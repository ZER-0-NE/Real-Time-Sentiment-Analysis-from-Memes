import os, sys, glob
import cv2
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from autocorrect import spell
from nltk import tokenize
import pdb

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/upload', methods = ['GET', 'POST'])
def home_and_upload():
	s = "No text was gathered from the image. Please try again!"
	if request.method == 'POST':
		target = os.path.join(APP_ROOT, UPLOAD_FOLDER)
		if not os.path.isdir(target):
			os.mkdir(target)
		else:
			for f in glob.glob(target + "/*"):
				os.remove(f)
		file = request.files['file']
		if file and allowed_file(file.filename):
			for file in request.files.getlist("file"):
				filename = secure_filename(file.filename)
				destination = "/".join([target, filename])
				file.save(destination)
				for im in os.listdir(target):
					image = cv2.imread(os.path.join(target, im))
					gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

					# check to see if we should apply thresholding to preprocess the image
					gray = cv2.threshold(gray, 0, 255,
						cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

					# make a check to see if median blurring should be done to remove
					# noise
					gray = cv2.medianBlur(gray, 3)

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
					if num_words[0] <= 20 and num_words[0] > 3:
						analyzer = SentimentIntensityAnalyzer()
						for sentence in extracted:
							vs = analyzer.polarity_scores(sentence)
							s = (""" SENTIMENT FOR THE SENTENCE:
									 {:-<65} \
									 Positive: {} \
									 Negative: {} \
									 Neutral: {} \
									 Compound: {}\
								""".format(sentence, vs["pos"], vs["neg"], vs["neu"], vs["compound"]))
					if num_words[0] > 20:
						extracted = str(extracted)
						analyzer = SentimentIntensityAnalyzer()
						sentence_list = tokenize.sent_tokenize(extracted)
						paragraphSentiments = 0.0
						for sentence in sentence_list:
							vs = analyzer.polarity_scores(sentence)
							s = '''{:-<69}
							'''.format(sentence)
							paragraphSentiments += vs["compound"]
							s += '''AVERAGE SENTIMENT FOR PARAGRAPH: 
								''' + str(round(paragraphSentiments / len(sentence_list), 4))


	return render_template('upload.html', output = s)

@app.route('/about')
def about():
	return render_template('about.html')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':
	app.run(debug = True)


