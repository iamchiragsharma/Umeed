import csv
from flask import Flask,render_template,url_for,request
from testing_var import test

from sentiment import get_profile,profile_hashtag_analyzer


app = Flask(__name__,static_url_path='/static')

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