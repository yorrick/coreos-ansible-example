from flask import Flask
from database import User


app = Flask(__name__)


@app.route("/")
def hello():
    users = User.query.all()
    usernames = [user.username for user in users]
    return "Hello World from users {}\n".format(", ".join(usernames))

if __name__ == "__main__":
    app.run()

