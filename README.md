<h1 align="center">
  Real Time Sentiment Analysis from Memes
</h1>

<p align="center">
  <img  src=/static/images/2.jpg/>
</p>


This project shows a simple way of doing sentiment analysis in your web-browser with the help of the vaderSentiment tool. This web-application is mainly suitable(and made) for memes and texts that appear in social-media bodies. The motivation for this project originates from the fact that there exists no such application which could analyze the sentiment from memes. Though memes being highly contextual and sarcastic, we believe the vaderSentiment tool is of great help in this regard. 
Typical Threshold values have been defined as below for a compound score used for analyzing the sentiment: 

- Positive sentiment: compound score >= 0.05 
- Neutral sentiment: (compound score > -0.05) and (compound score < 0.05) 
- Negative sentiment: compound score <= -0.05 



## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [vaderSentiment](https://github.com/cjhutto/vaderSentiment).

```bash
pip install vaderSentiment
```
### Other Dependencies:

- OpenCV
- Flask


## Usage

```python
python run.py
```


<h2 align="center">
  Successful attempts:
</h2>

<p align="center">
  <img  src=/static/images/pic1.jpg/>
</p>


<p align="center">
  <img  src=/static/images/pic2.jpg/>
</p>


<p align="center">
  <img  src=/static/images/pic3.jpg/>
</p>


<p align="center">
  <img  src=/static/images/pic4.jpg/>
</p>




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
