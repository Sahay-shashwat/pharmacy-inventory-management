from flask import Flask,render_template,redirect,request,jsonify,json
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
            GST=int(request.form['GST'])
            rate=request.form['Rate']
            id=db.getID('item_master')
            flag=db.check_data_exists(name,'item_master','Product_name')
            if(not flag):
                data=(id,name,HSM,rate,GST,GST/2,GST/2)
                db.insert_record("item_master",data)
                return redirect('dashboard')
            else:
                error='PRODUCT ALREADY EXISTS'
                return render_template('item_master.html',error=error)
        except:
            db.roll()

@app.route("/customer_master")
def customer():
    return render_template("customer_master.html") 

@app.route("/customer_master", methods=["POST","GET"])
def customer_master():
    if request.method=="POST":
        try:
            error= None
            custname=request.form['customer_name']
            add=request.form['address']
            mobile=int(request.form['mobile'])
            gst=request.form['GSTIN']
            id=db.getID('customer_master')
            flag=db.check_data_exists(custname,"customer_master",'Customer_Name')
            if( not flag):
                data=(id,custname,add,mobile,gst)
                db.insert_record("customer_master",data)
                return redirect('dashboard')
            else:
                error='CUSTOMER ALREADY EXISTS'
                return render_template('customer_master.html',error=error)
        except:
            db.roll()

@app.route("/vendor_master")
def vendor():
    return render_template("vendor_master.html") 

@app.route("/vendor_master", methods=["POST","GET"])
def vendor_master():
    if request.method=="POST":
        try:
            error= None
            vname=request.form['vendor_name']
            add=request.form['address']
            mobile=int(request.form['mobile'])
            gst=request.form['GSTIN']
            drug=request.form['drug_lisc']
            id=db.getID('vendor_master')
            flag=db.check_data_exists(vname,"vendor_master",'Vendor_Name')
            if(not flag):
                data=(id,vname,add,mobile,gst,drug)
                db.insert_record("vendor_master",data)
                return redirect('dashboard')
            else:
                error='VENDOR ALREADY EXISTS'
                return render_template('vendor_master.html',error=error)
        except:
            db.roll()

@app.route("/purchase_reg")
def purchase_reg():
    data=db.getColumn("Vendor_Name","vendor_master")
    items=db.getColumn("Product_name","item_master")
    return render_template("purchase_reg.html",data=data,items=items) 

@app.route('/purchase_register', methods=['POST'])
def purchase_register():
    data = request.form
    products = data.getlist('product[]')
    rates = data.getlist('rate[]')
    quantities = data.getlist('quantity[]')
    vendor_name = ((data.getlist('vendor_name')[0]).replace("('","")).replace("',)","")
    challan = data.getlist('challan')[0]
    Bill_date = data.getlist('Bill_date')[0]
    Exp_date = data.getlist('Exp_date')[0]
    Manf_date = data.getlist('Manf_date')[0]
    prid=db.getID("purchase_reg")
    Billno=db.getBill("purchase_reg")
    vid=db.getReferenceID("vendor_master","Vendor_Name",vendor_name)
    formdata=(prid,Billno,0,vid,challan,Bill_date)
    db.insert_record("purchase_reg",formdata)

    sum=0
    for i in range(len(products)):
        id=db.getID("purchase_detail")
        product=products[i].replace("('","").replace("',)","")
        pid=db.getReferenceID("item_master","Product_name",product)
        rate=float(rates[i])
        quantity=int(quantities[i])
        amount=r*q
        sum+=amount
        details=(id,pid,prid,rate,quantity,amount,Exp_date,Manf_date)
        db.insert_record("purchase_detail",details)
    
    db.updatedetails("purchase_detail","AMOUNT",sum,prid)
    return redirect('dashboard')

@app.route("/inventory-repo")
def inventory():
    return render_template("inventory.html") 

@app.route('/get_items', methods=['GET'])
def get_items():
    items=db.getColumn("Product_name","item_master")
    product_options=[]
    for i, name in enumerate(items):
        product_option ={"value": str(i), "text": name}
        product_options.append(product_option)
    return jsonify(product_options)

if __name__ == '__main__':
    app.run(debug=True)