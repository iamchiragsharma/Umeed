import os
import csv
from flask import Flask,render_template,url_for,request
from werkzeug.utils import secure_filename

from testing_var import test
from sentiment import get_profile,profile_hashtag_analyzer,get_tweet_data
from upload import allowed_file
from explicit import explicit_img_detector

app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = './static/upload'

suspect = {}


@app.route('/')
def index():
    states_trends = test()
    return render_template("index.html",states_trends=states_trends)


@app.route('/profile',methods=["GET","POST"])
def profile():
    global suspect
    if request.method == "POST":
        twitter_id = request.form.get("tweetbox")
        if twitter_id.startswith("#"):
            hashtag_data = profile_hashtag_analyzer(twitter_id)
            return render_template("hashtag.html",hashtag_data=hashtag_data)
        else:
            user_profile = get_profile(twitter_id)
            user_data = profile_hashtag_analyzer(twitter_id)
            suspect = user_profile
            return render_template("profile.html",user_profile=user_profile,user_data=user_data)

@app.route('/suspectprofiles',methods=["GET","POST"])
def suspectprofiles():
    global suspect
    if request.method == "POST":
        with open("datalogs/suspect.csv","a+") as csvFile:
            writer = csv.writer(csvFile)
            row = [suspect['name'],suspect['username'],suspect['profile_photo'],suspect['likes_count'], suspect['tweets_count'], suspect['followers_count'], suspect['following_count']]
            writer.writerow(row)
        
        with open("datalogs/suspect.csv","r") as csvFile:
            reader = csv.reader(csvFile)
            suspects = [row for row in reader]
        
    suspects = reversed(suspects)
    return render_template("suspectprofiles.html",suspects=suspects)

@app.route("/hashtag_profile/<twitter_id>")
def hashtag_profile(twitter_id):
    user_profile = get_profile(twitter_id)
    user_data = profile_hashtag_analyzer(twitter_id)
    suspect = user_profile
    return render_template("profile.html",user_profile=user_profile,user_data=user_data)

@app.route("/tweet_profile/<tweet_id>")
def tweet_profile(tweet_id):
    """Takes Tweet Id and Analyzes Media Content Attached to It"""
    tweet_data = get_tweet_data(tweet_id)
    tweet_media = { 'tweet_id' : tweet_id, 'tweet_media_urls' : [entity['media_url'] for entity in tweet_data._json['extended_entities']['media']] }
    tweet_media_nudity = [explicit_img_detector(url) for url in tweet_media['tweet_media_urls']]
    return render_template("tweet_profile.html",tweet_media = tweet_media,tweet_media_nudity=tweet_media_nudity)

@app.route('/uploader')
def uploader():
   return render_template('uploader.html')
	
@app.route('/explicit', methods = ['GET', 'POST'])
def explicit():
   if request.method == 'POST':
      f = request.files['file']
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename))
      f.save(filepath)
      return render_template('explicit.html',filepath=filepath)

if __name__ == '__main__':
    app.run(debug=True)





# {% for state_row in states_trends[key] | batch(3, '&nbsp;') %}
# {% for key,value in states_trends.items() %}
# {% for trend in states_trends[key] %}

# {% endfor %}
# {% endfor %}

# <div class="btn-group" role="group" aria-label="Basic example">
# <button type="button" class="btn btn-danger">Sexual : 2 </button>
# <button type="button" class="btn btn-danger">Hate Speech/Voilence : 2</button>
# <button type="button" class="btn btn-danger">Child Predator : No </button>
# </div>