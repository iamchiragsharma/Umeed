from flask import Flask,render_template,url_for,request
from testing_var import test

from sentiment import get_profile,profile_hashtag_analyzer


app = Flask(__name__,static_url_path='/static')


@app.route('/')
def index():
    states_trends = test()
    return render_template("index.html",states_trends=states_trends)


@app.route('/profile',methods=["GET","POST"])
def profile():
    if request.method == "POST":
        twitter_id = request.form.get("tweetbox")
        user_profile = get_profile(twitter_id)
        user_data = profile_hashtag_analyzer(twitter_id)
        return render_template("profile.html",user_profile=user_profile,user_data=user_data)


if __name__ == '__main__':
    app.run(debug=True)






# {% for state_row in states_trends[key] | batch(3, '&nbsp;') %}
# {% for key,value in states_trends.items() %}
# {% for trend in states_trends[key] %}

# {% endfor %}
# {% endfor %}