from flask import Flask
from database import User, db


app = Flask(__name__)


@app.route("/")
def hello():
    # for the purpose of this test, we always rollback current transaction so that if connection to database was lost app will still work
    db.session.rollback()

    users = User.query.all()
    usernames = [user.username for user in users]
    return "Hello World from users {}\n".format(", ".join(usernames))

if __name__ == "__main__":
    app.run()

