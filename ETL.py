import pandas as pd
import pyodbc

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-GARLJAI;"
                       "Database = Trg_Py_db;"
                      "Trusted_Connection=yes;",
                      autocommit=True)

sql_ecom_custom = """select  customer_id,
	customer_unique_id,
	customer_zip_code_prefix,
	customer_city,
	customer_state from ecom.dbo.customer with (nolock)"""
df1 =pd.read_sql(sql_ecom_custom,cnxn)
df1.shape

cursor = cnxn.cursor() #when connection is used as function
cursor.execute('DROP Table Trg_Py_db.dbo.sell_info')
cursor.execute('DROP Table Trg_Py_db.dbo.Customer')
cursor.commit()
#creating_target seller_table
table_seller_create = ('''IF NOT EXISTS (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME ='sell_info')
    create table Trg_Py_db.dbo.sell_info (
    seller_id varchar (25) not null,
    seller_zip_code_prefix int,
    seller_city varchar(25),
    seller_state varchar(25),
    Primary Key(seller_id)
    )''')
cursor.execute(table_seller_create)
cursor.commit()
# cnxn.commit()
#creating_target customer_table
table_Customer_create = ('''IF NOT EXISTS (select * from INFORMATION_SCHEMA.TABLES where TABLE_NAME ='Customer')
   CREATE TABLE Trg_Py_db.dbo.Customer(
	customer_id varchar(50) NOT NULL,
	customer_unique_id varchar  (50) NULL,
	customer_zip_code_prefix varchar (50) NULL,
	customer_city varchar (50) NULL,
	customer_state varchar (50) NULL,
    Primary Key(customer_id)
    )''')

cursor.execute(table_Customer_create)
cnxn.commit()

# trg_customer_table_insert = ("""INSERT INTO Trg_Py_db.dbo.Customer
#     (customer_id,
# 	customer_unique_id,
# 	customer_zip_code_prefix,
# 	customer_city,
# 	customer_state)
# 	VALUES(%s,%s,%s,%s,%s)
# 	""")



for i in range(len(df1)):
	cursor.execute('''INSERT INTO Trg_Py_db.dbo.Customer 
	(customer_id,
	customer_unique_id,
	customer_zip_code_prefix,
	customer_city,
	customer_state) VALUES (?,?,?,?,?)''',df1.customer_id[i],
                   df1.customer_unique_id[i],df1.customer_zip_code_prefix[i],df1.customer_city[i],df1.customer_state[i])


# for i, row in df1.iterrows():
#     cursor.execute(trg_customer_table_insert,sql_ecom_custom.customer_id[i])
# cnxn.close()

