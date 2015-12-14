from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

@app.route('/<username>/')
def profile():
    return "It's the profile page for user %s" % username

@app.route("/hello/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
