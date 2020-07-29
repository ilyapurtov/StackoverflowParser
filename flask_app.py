# ========================================================================

# To use this application source code you should to be installed next modules:

# flask => pip install flask
# requests => pip install requests
# beautifulsoup4 => pip install bs4

# <=== Next step ===>

# Go to https://www.whatismybrowser.com/detect/what-is-my-user-agent
# Copy your user agent from that website
# Paste it to 32 line (replace USER_AGENT)

# Done

# ========================================================================



from flask import Flask, render_template, flash, get_flashed_messages, Markup, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config['SECRET_KEY'] = "sdfl;keysozinuopcsinu8097z!)892b9niosc()*)!@"

url = "https://ru.stackoverflow.com/"

# Please replace USER_AGENT to your user agent
HEADERS = {'user-agent': 'USER_AGENT'}

r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

# Here we get all questions from main page of the stackoverflow
items = soup.findAll("div", class_="question-summary")


@app.route("/")
def index():
    global items
    for item in items:
    	# Return questions html to index file
        flash(Markup(item))
    return render_template("index.html")

    
@app.route('/questions/<path:q>')
def question(q):
    global HEADERS

    # Here we are connecting to the ru.stackoverflow.com/questions/<user-request>
    question_request = requests.get("https://ru.stackoverflow.com/questions/" + q, headers=HEADERS)
    q_soup = BeautifulSoup(question_request.content, "html.parser")
    for q_item in q_soup.find("div", {"id": "mainbar"}):
    	# Return question html to question file
        flash(Markup(q_item))
    return render_template("question.html");


# If url not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# If user request cannot be handled 
@app.errorhandler(500)
@app.errorhandler(405)
def internal_server_error(e):
    return render_template("500.html")
    

if __name__ == "__main__":
	# Running application
    app.run(debug=True)