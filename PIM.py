import mysql.connector

class Database:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='DBMS',
            password='DBMS',
            host = 'localhost',
            database='pharm',
        )
        if self.conn.is_connected():
            print('Connection is open')
        self.curr = self.conn.cursor(prepared=True)
        self._cursor = self.curr
        try:
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS user_details(
                        ID VARCHAR(255),
                        Password VARCHAR(255),
                        PRIMARY KEY(ID)
                        );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS item_master(
                              ID INT PRIMARY KEY,
                              Product_name VARCHAR(255),
                              HSM VARCHAR(255),
                              GST FLOAT,
                              CGST FLOAT,
                              SGST FLOAT
                              );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS vendor_master(
                              ID INT PRIMARY KEY,
                              Vendor_Name VARCHAR(255),
                              Address VARCHAR(255),
                              Mobile BIGINT,
                              GSTIN VARCHAR(255),
                              Drug_lisc VARCHAR(255)
                              );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS purchase_detail(
                              ID INT PRIMARY KEY,
                              PID INT REFERENCES item_master(ID),
                              PRID INT REFERENCES purchase_reg(ID),
                              RATE FLOAT,
                              QUANTITY INT,
                              AVAILABLE INT,
                              AMOUNT FLOAT,
                              MRP FLOAT,
                              Exp_Date DATE,
                              Manf_Date DATE
                              );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS purchase_reg(
                              ID INT PRIMARY KEY,
                              Billno INT,
                              amount FLOAT,
                              VID INT REFERENCES vendor_master(ID) ON DELETE SET NULL,
                              Vendor_chalan VARCHAR(255),
                              Bill_date date
                              );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS customer_master(
                              ID INT PRIMARY KEY,
                              Customer_Name VARCHAR(255),
                              Address VARCHAR(255),
                              Mobile BIGINT,
                              GSTIN VARCHAR(255)
                              );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS sale_details(
                              ID INT PRIMARY KEY,
                              PID INT REFERENCES item_master(ID),
                              SID INT REFERENCES sale_reg(ID),
                              MRP FLOAT,
                              Quantity INT,
                              Discount FLOAT,
                              SP FLOAT,
                              GST FLOAT
                              );
            ''')
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS sale_reg(
                              ID INT PRIMARY KEY,
                              Billno INT,
                              amount FLOAT,
                              CID INT REFERENCES customer_master(ID),
                              Bill_date date
                              );
            ''')
            self.conn.commit()
        except:
            raise Exception("An error occured with DB initialization!")


    def roll(self):
        self.conn.rollback()


    def check_login(self,username,password):
        try:
            query="SELECT ID FROM user_details WHERE ID=?"
            self.curr.execute(query,(username,))
            if (self.curr.fetchone()[0]!=None):
                query2="SELECT Password FROM user_details WHERE ID=?"
                self.curr.execute(query2,(username,))
                if (self.curr.fetchone()[0] == password) :
                    return True
                else:
                    return False
            else:
                return False
        except:
            print("ERROR FINDING DATA")


    def check_data_exists(self,data,tname,col):
        try:
            query = f"SELECT COUNT(*) FROM {tname} WHERE {col}={data}"
            self.curr.execute(query)
            data=self.curr.fetchone()[0]
            if data!=0:
                return True
            else:
                return False
        except:
            print("ERROR FINDING DATA")


    def getID(self,tname):
        query=f"SELECT MAX(ID) FROM {tname}"
        self.curr.execute(query)
        result = self.curr.fetchone()[0]
        if (result == None):
            return 1
        return ((result)+1)
    
    def getBill(self,tname):
        query=f"SELECT MAX(Billno) FROM {tname}"
        self.curr.execute(query)
        result = self.curr.fetchone()[0]
        if (result == None):
            return 1
        return ((result)+1)

    def getReferenceID(self,tname,col,data):
        try:
            query=f"SELECT MAX(ID) FROM {tname} WHERE {col} = ?"
            self.curr.execute(query,(data,))
            result = self.curr.fetchone()[0]
            return result
        except:
            print("ERROR FINDING DATA")

    def getExisitingProduct(self,id):
        try:
            query=f"SELECT DISTINCT PID FROM purchase_detail WHERE PID = ?"
            items=[]
            for pid in id:
                self.curr.execute(query,(pid,))
                result = self.curr.fetchone()[0]
                if result != None:
                    items.append(result[0])
            query=f"SELECT Product_name FROM item_master WHERE ID=?"
            product=[]
            for id in items:
                self.curr.execute(query,(id,))
                result = self.curr.fetchone()[0]
                if result != None:
                    product.append(result[0])
            return product
        except:
            print("ERROR FINDING DATA")
    

    def getColumn(self,col,tname):
        try:
            query=f"SELECT {col} FROM {tname}"
            self.curr.execute(query)
            result = self.curr.fetchall()
            return result
        except:
            print("ERROR FINDING DATA")

    def getExistingProductName(self):
        try:
            query="SELECT DISTINCT Product_name FROM item_master,purchase_detail WHERE item_master.ID = purchase_detail.PID AND purchase_detail.AVAILABLE != 0"
            self.curr.execute(query)
            result = self.curr.fetchall()
            return result
        except:
            print("ERROR FINDING DATA")

    def updatedetails(self,tname,colname,amount,id):
        try:
            query=f"UPDATE {tname} SET {colname} = ? WHERE ID = ?"
            self.curr.execute(query,(amount,id))
            self.conn.commit()
        except:
            print("ERROR UPDATING")

    def setAvailable(self, amount,pid,exp_date):
        try:
            query = "SELECT AVAILABLE FROM purchase_detail WHERE PID = ? AND Exp_Date = ?"
            self.curr.execute(query,(pid,exp_date))
            result = self.curr.fetchone()[0]
            newQuantity = result-amount
            print(result,amount,newQuantity)
            query = "UPDATE purchase_detail SET AVAILABLE = ? WHERE PID = ? AND Exp_Date = ?"
            self.curr.execute(query,(newQuantity,pid,exp_date))
            self.conn.commit()
        except:
            print("ERROR SETTING AVAILABLE")

    def getMRP(self,tname,col,data):
        try:
            query=f"SELECT MRP FROM purchase_detail WHERE PID = ?"
            self.curr.execute(query,(data,))
            result = self.curr.fetchall()
            return result
        except:
            print("ERROR FINDING DATA")

            
    def getName(self,tname,colname,data):
        try:
            query=f"SELECT {colname} FROM {tname} WHERE ID=?"
            items=[]
            for i in range(len(data)):
                self.curr.execute(query,(data[i],))
                result = self.curr.fetchone()[0]
                items.append(result)
            return items
        except:
            print("ERROR FINDING DATA")

    def getDetails(self,id,tname):
        try:
            query=f"SELECT PID,Manf_Date,Exp_Date,MRP,AVAILABLE FROM {tname} WHERE PID = ? AND AVAILABLE > 0"
            result=[]
            for PID in id:
                self.curr.execute(query,(PID,))
                item=self.curr.fetchall()
                if len(item)!=0:
                    result.append(item)
            items=[]
            for i in range(len(result[0])):
                items.append(result[0][i])
            return items
        except Exception as e:
            print(e)
            print("ERROR FINDING DATA")

    def getIDlist(self,tname,colname,data):
        try:
            query=f"SELECT ID FROM {tname} WHERE {colname} LIKE '{data}%'"
            self.curr.execute(query)
            result = self.curr.fetchall()
            return result
        except:
            print("ERROR FINDING DATA")

    def getExpDate(self,id,MRP):
        try:
            query=f"SELECT Exp_Date FROM purchase_detail WHERE PID = ? AND MRP = ?"
            self.curr.execute(query,(id,MRP))
            result = self.curr.fetchall()
            return [row[0].strftime("%Y-%m-%d") for row in result]
        except:
            print("ERROR FINDING DATA")

    def getGST(self,id):
        try:
            query=f"SELECT GST FROM item_master WHERE ID = ?"
            self.curr.execute(query,(id,))
            result = self.curr.fetchone()[0]
            return result
        except:
            print("ERROR FINDING DATA")

    def getAvailability(self,tname,pid,MRP,Exp_date):
        try:
            query=f"SELECT AVAILABLE FROM {tname} WHERE PID = ? AND MRP = ? AND Exp_Date = ?"
            self.curr.execute(query,(pid,MRP,Exp_date))
            result = self.curr.fetchone()[0]
            return result
        except:
            print("ERROR FINDING DATA")
    
    def getGSTIN(self,vendor):
        try:
            query=f"SELECT GSTIN FROM vendor_master WHERE Vendor_Name = ?"
            self.curr.execute(query,(vendor,))
            result=self.curr.fetchall()
            return result
        except:
            print("ERROR FINDING DATA")

    def deleteData(self,name,gstin):
        try:
            query=f"DELETE FROM vendor_master WHERE Vendor_Name= ? AND GSTIN = ?"
            print(query)
            self.curr.execute(query,(name,gstin))
            print(name,gstin)
            self.conn.commit()
            print(True)
        except:
            print("ERROR DELETING DATA")

    def insert_record(self,tname,form_data):
        if tname == 'item_master':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?,?)",form_data)
            finally:
                self.conn.commit()
        if tname == 'vendor_master':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?,?)",form_data)
            finally:
                self.conn.commit()
        if tname == 'purchase_detail':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?,?,?,?,?,?)",form_data)
            finally:
                self.conn.commit()
        if tname == 'purchase_reg':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?,?)",form_data)
            except:
                print("ERROR INSERTING DATA")
            finally:
                self.conn.commit()
        if tname == 'customer_master':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?)",form_data)
            except:
                print("ERROR INSERTING DATA")
            finally:
                self.conn.commit()
        if tname == 'sale_details':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?,?,?,?)",form_data)
            finally:
                self.conn.commit()
        if tname == 'sale_reg':
            try:
                self.curr.execute(f"INSERT INTO {tname} VALUES (?,?,?,?,?)",form_data)
            finally:
                self.conn.commit()

    
    def __del__(self):
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
                print('Connection closed')
        except Exception as e:
            print(f"Error occurred while closing connection: {e}")