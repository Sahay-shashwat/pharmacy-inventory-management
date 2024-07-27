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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/item_master")
def item():
    return render_template("item_master.html")

@app.route("/item_master", methods=["POST","GET"])
def item_master():
    if request.method=="POST":
        try:
            error=None
            name=request.form['product_name']
            HSM=request.form['HSM']
            GST=request.form['GST']
            id=db.getID(item_master)
            flag=db.check_data_exists(name,'item_master','Product_name')
            if(flag):
                data=(id,name,HSM,GST,GST/2,GST/2)
                db.insert_record("item_master",data)
                return redirect('item_master')
            else:
                error='PRODUCT ALREADY EXISTS'
                return render_template('item_master',error=error)
        except:
            db.roll()

if __name__ == '__main__':
    app.run(debug=True)