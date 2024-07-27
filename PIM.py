import mysql.connector

class Database:
    
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='DBMS',
            password='asdqwe123',
            host = 'localhost',
            database='DBMS'
            )
        if self.conn.is_connected():
            print('Connection is open')
        else:
            print("Error connecting")
        self.curr = self.conn.cursor()
        try:
            self.curr.execute('''
                CREATE TABLE IF NOT EXISTS user_details(
                        ID VARCHAR(255),
                        Password VARCHAR(255),
                        PRIMARY KEY(ID)
                        );
            ''')
            self.curr.execute ('''
                CREATE TABLE IF NOT EXISTS item_master(
                        ID INT PRIMARY KEY,
                        product_name varchar(255) NOT NULL,
                        HSM_Code varchar(255),
                        GST_per float,
                        SGST_per float,
                        CGST_per float
                        );
            ''') 
            self.curr.execute ('''
                CREATE TABLE IF NOT EXISTS vendor_master(
                        ID INT PRIMARY KEY,
                        PID INT REFERENCES item_master(ID),
                        Name varchar(255) NOT NULL,
                        Address VARCHAR(255), 
                        mobile VARCHAR(255),
                        GSTIN varchar(255),
                        drug_lisc varchar(255)
                        );
            ''')
            self.curr.execute ('''
                CREATE TABLE IF NOT EXISTS purchase_table(
                        Bill_No INT PRIMARY KEY,
                        PID INT REFERENCES item_master(ID),
                        CP FLOAT,
                        SP FLOAT,
                        Manf_Date Date,
                        Exp_Date Date,
                        Purchase_Date Date
                        );
            ''')
            self.curr.execute ('''
                CREATE TABLE IF NOT EXISTS purchase_register(
                        ID INT PRIMARY KEY,
                        Bill_No INT REFERENCES purchase_table(Bill_No),
                        Amount FLOAT,
                        VID INT REFERENCES vendor_master(ID)
                        );
            ''')
            self.curr.execute ('''
                CREATE TABLE IF NOT EXISTS customer_master(
                        ID INT PRIMARY KEY,
                        Name varchar(255) NOT NULL,
                        Address VARCHAR(255), 
                        mobile VARCHAR(255),
                        GSTIN varchar(255),
                        );
            ''')
            self.curr.execute ('''
                CREATE TABLE IF NOT EXISTS sale_table(
                        Bill_No INT PRIMARY KEY,
                        PID INT REFERENCES item_master(ID),
                        MRP FLOAT,
                        DISCOUNT FLOAT,
                        SP FLOAT,
                        GST FLOAT,
                        Sale_Date Date
                        );
            ''') 
            self.curr.execure('''
                CREATE TABLE IF NOT EXISTS Sale_register(
                              ID INT PRIMARY KEY,
                              Bill_No INT REFERENCES sale_master(Bill_No),
                              Amount FLOAT,
                              CID INT REFERENCES customer_master(ID)    
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
            print(username)
            if (self.curr.fetchone()[0]!=None):
                query2="SELECT Password FROM user_details WHERE ID=?"
                table_pass=self.curr.execute(query2,(username,))
                if (self.curr.fetchone()[0] == password) :
                    return True
                else:
                    return False
            else:
                return False
        except:
            print("ERROR FINDING DATA")

    def __del__(self):
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
                print('Connection closed')
        except Exception as e:
            print(f"Error occurred while closing connection: {e}")
