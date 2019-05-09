import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = User.fetch_one(query=["email", "==", email_address])
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    # create a secret number
    secret_number = random.randint(1, 30)

    # see if user already exists
    user = User.fetch_one(query=["email", "==", email])

    if not user:
        # create a User object
        user = User(name=name, email=email, secret_number=secret_number)
        user.create()  # save the object into a database

    # save user's email into a cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = (request.form.get("guess"))
    if guess.upper() == "Q":
        # message = "Thank you. Your game is over."
        message = "Game is over."
        response = make_response(render_template("result.html", message=message))
        return response
    if guess.isdigit():
        pass
    else:
        message = "You can only enter numbers.Try again."
        response = make_response(render_template("result.html", message=message))
        return response

    guess = int(request.form.get("guess"))

    email_address = request.cookies.get("email")

    # get user from the database based on her/his email address
    user = User.fetch_one(query=["email", "==", email_address])

    if guess == user.secret_number:
        message = "Congrats!. Secret number is {0}".format(str(guess))

        # create a new random secret number
        new_secret = random.randint(1, 30)

        # update the user's secret number in the User collection
        User.edit(obj_id=user.id, secret_number=new_secret)
    elif guess > user.secret_number:
        message = "Try something smaller."
    elif guess < user.secret_number:
        message = "Try something bigger."

    return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)