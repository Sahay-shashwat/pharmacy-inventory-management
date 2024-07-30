from flask import Flask,render_template,redirect,request,jsonify,json,url_for
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
            id=db.getID('item_master')
            flag=db.check_data_exists(name,'item_master','Product_name')
            if(not flag):
                data=(id,name,HSM,GST,GST/2,GST/2)
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
            custname=request.form['customer_name'].replace("('","").replace("',)","")
            add=request.form['address']
            mobile=int(request.form['mobile'])
            gst=request.form['GSTIN'].replace("(,","").replace("',)","")
            id=db.getID('customer_master')
            flag=db.check_data_exists(gst,"customer_master",'GSTIN')
            if(not flag):
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
            vname=request.form['vendor_name'].replace("('","").replace("',)","")
            add=request.form['address']
            mobile=int(request.form['mobile'])
            gst=request.form['GSTIN']
            drug=request.form['drug_lisc']
            id=db.getID('vendor_master')
            flag=db.check_data_exists(gst,"vendor_master",'GSTIN')
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
    Exp_date = data.getlist('Exp_date[]')
    Manf_date = data.getlist('Manf_Date[]')
    MRP=data.getlist("MRP[]")
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
        available=quantity
        exp_date=Exp_date[i]
        manf_date=Manf_date[i]
        amount=rate*quantity
        mrp=float(MRP[i])
        sum+=amount
        details=(id,pid,prid,rate,quantity,available,amount,mrp,exp_date,manf_date)
        db.insert_record("purchase_detail",details)
    
    db.updatedetails("purchase_reg","amount",sum,prid)
    return jsonify({'message': 'Form submission successful'}), 200


@app.route("/customer_register", methods=['POST'])
def customer_register():
    data=request.form
    custname=data.getlist('customer_name')[0].replace("('","").replace("',)","")
    BillDate=data.getlist('Bill_date')[0]
    custID=db.getReferenceID("customer_master","Customer_Name",custname)
    products=data.getlist('product[]')
    Exp_Date=data.getlist('Exp_date[]')
    quantity=data.getlist('quantity[]')
    discount=data.getlist('Discount[]')
    mrp=data.getlist("MRP[]")

    SRID=db.getID("sale_reg")
    Billno=db.getBill("sale_reg")

    formdata=(SRID,Billno,0,custID,BillDate)
    db.insert_record("sale_reg",formdata)

    sum=0
    for i in range(len(products)):
        id=db.getID("sale_details")
        product=products[i].replace("('","").replace("',)","")
        pid=db.getReferenceID("item_master","Product_name",product)
        MRP=float(mrp[i])
        Discount=float(discount[i])
        SP = MRP - (Discount/100*MRP)
        GSTper = db.getGST(pid)
        GST=GSTper/100*SP
        quantities=int(quantity[i])
        Exp_date=Exp_Date[i]
        db.setAvailable(quantities,pid,Exp_date)

        sum+=(SP*quantities)

        form_data=(id,pid,SRID,MRP,quantities,Discount,SP,GST)
        db.insert_record("sale_details",form_data)

    db.updatedetails("sale_reg","amount",sum,SRID)
    return jsonify({'message': 'Form submission successful'}), 200

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

@app.route('/inventory',methods=['GET'])
def inventory_repo():
    try:
        search_query=request.args.get('inventory').replace("('","").replace("',)","")
        id=db.getIDlist("item_master","Product_name",search_query)
        for i in range(len(id)):
            id[i]=id[i][0]
        data=db.getDetails(id,"purchase_detail")
        for i in range(len(data)):
            data[i]=list(data[i])
        medicine_id=[]
        name=[]
        for i in range(len(data)):
            medicine_id.append(data[i][0])
        name=db.getName("item_master","Product_name",medicine_id)
        for i in range(len(name)):
            data[i][0]=name[i]

        for i in range(len(data)):
            data[i][1]=data[i][1].strftime("%Y-%m-%d")
            data[i][2]=data[i][2].strftime("%Y-%m-%d")
        result=[]
        for i,item in enumerate(data):
            result.append({"index":str(i),"value":item})
        return jsonify(result)
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error":"Failed to retrieve inventory data"},500)
    
@app.route("/customer_reg")
def customer_reg():
    data=db.getColumn("Customer_Name","customer_master")
    items=db.getExistingProductName()
    return render_template("customer_reg.html",data=data,items=items) 

@app.route('/get_items_customer', methods=['GET'])
def get_items_consumer():
    items=db.getExistingProductName()
    product_options=[]
    for i, name in enumerate(items):
        product_option ={"value": str(i), "text": name}
        product_options.append(product_option)
    return jsonify(product_options)

@app.route("/getMRP", methods=['GET'])
def getMRP():
    product_name=request.args.get('product').replace("('","").replace("',)","")
    product_id=db.getReferenceID("item_master","Product_name",product_name)
    mrp=db.getMRP("item_master","Product_id",product_id)
    MRP=[]
    for i,name in enumerate(mrp):
        MRP.append({"value":str(i),"MRP":name})
    return jsonify(MRP)

@app.route("/getExpDate", methods=['GET'])
def getExpDate():
    medicine = request.args.get('medicine', None).replace("('","").replace("',)","")
    MRP = request.args.get('MRP')
    id=db.getReferenceID("item_master","Product_name",medicine)
    items=db.getExpDate(id,MRP)
    expDate=[]
    for i,name in enumerate(items):
        expDate.append({"value":str(i),"ExpDate":name})
    return jsonify(expDate)


@app.route('/get_available_quantity', methods=['GET'])
def get_available_quantity():
    medicine = request.args.get('medicine', None).replace("('","").replace("',)","")
    MRP = request.args.get('MRP')
    Exp_date=request.args.get('Exp_date')
    pid=db.getReferenceID("item_master","Product_name",medicine)
    available_quantity = db.getAvailability("purchase_detail",pid,MRP,Exp_date)
    return jsonify({'available_quantity': available_quantity})

if __name__ == '__main__':
    app.run(debug=True)