from flask import Flask,render_template,redirect,request
app = Flask(__name__)

from PIM import Database
db=Database()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method== "POST":
        try:
            error=None
            username = request.form['username']
            password = request.form['password']
            flag=db.check_login(username,password)
            if (flag):
                return redirect('dashboard')
            else:
                error='INVALID USERNAME OR PASSWORD'
                return render_template('login.html',error=error)
        except:
            db.roll()


if __name__ == '__main__':
    app.run(debug=True)