# Author: Bharat Penumathsa
# Last tested for functionality on 24.05.22 at 16:00
# import os.system and os.name to use in clear function
import json
import csv
import pymysql
import os
from dotenv import load_dotenv
from csv import DictReader
from csv import DictWriter
from os import system, name

def clear(): # Defines clear function
    if name == 'nt': # For windows os.name is 'nt'
        clear_screen = system('cls')
clear() # Calling clear function to clear screen

def get_alltable_rows():
    try:
        load_dotenv()
        host = os.environ.get("mysql_host")
        user = os.environ.get("mysql_user")
        password = os.environ.get("mysql_pass")
        database = os.environ.get("mysql_db")

        # Load_envfile()
        # Establish a database connection
        connection = pymysql.connect(
            host,
            user,
            password,
            database
        )
        # A cursor is an object that represents a DB cursor,
        # which is used to manage the context of a fetch operation.
        cursor = connection.cursor()
        print("Connected to MySQL")
        products_select_query = "SELECT * FROM products"
        couriers_select_query = "SELECT * FROM couriers"
        orders_select_query = "SELECT * FROM orders"
        orders_status_query = "SELECT * FROM order_status"
        cursor.execute(products_select_query)
        products_records = cursor.fetchall()
        cursor.execute(couriers_select_query)
        couriers_records = cursor.fetchall()
        cursor.execute(orders_select_query)
        orders_records = cursor.fetchall()
        cursor.execute(orders_status_query)
        status_records = cursor.fetchall()
        connection.commit()
        cursor.close()
    except pymysql.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print('The pymysql connection is closed')
    return products_records, couriers_records, orders_records, status_records

# Function call to run env, connection, query and returns output table rows in tuple format
products_records, couriers_records, orders_records, status_records = get_alltable_rows()
# Print(list(products_records))
keys1 = ('product_id','product_name', 'product_price')
keys2 = ('courier_id','courier_name', 'courier_phone')
keys3 = ('order_id','customer_name','customer_address', 'customer_phone', 'courier', 'status','items')
keys4 = ('status_id','status')
#Coverts tuple rows to dictionaries
urban_brew_products = [dict(zip(keys1, values)) for values in products_records]
urban_brew_couriers = [dict(zip(keys2, values)) for values in couriers_records]
urban_brew_orders = [dict(zip(keys3, values)) for values in orders_records]
orders_status = [dict(zip(keys4, values)) for values in status_records]

#Function to export products, couriers, and orders data to csv files
def file_write():
    with open("products.csv",'w',encoding='UTF8', newline='') as product_file, open("couriers.csv",'w',encoding='UTF8', newline='') as courier_file, open("orders.csv", 'w',encoding='UTF8', newline='') as orders_dict_file:
        urban_brew_products_fieldnames = ['product_id','product_name','product_price']
        urban_brew_couriers_filednames = ['courier_id','courier_name','courier_phone']
        urban_brew_orders_filednames = ['order_id','customer_name','customer_address','customer_phone','courier','status','items']
        urban_brew_products_writer = csv.DictWriter(product_file,fieldnames=urban_brew_products_fieldnames)
        urban_brew_couriers_writer = csv.DictWriter(courier_file,fieldnames=urban_brew_couriers_filednames)
        urban_brew_orders_writer = csv.DictWriter(orders_dict_file,fieldnames=urban_brew_orders_filednames)
        urban_brew_products_writer.writeheader()
        urban_brew_couriers_writer.writeheader()
        urban_brew_orders_writer.writeheader()
        urban_brew_products_writer.writerows(urban_brew_products)
        urban_brew_couriers_writer.writerows(urban_brew_couriers)
        urban_brew_orders_writer.writerows(urban_brew_orders)

#Creating list for order status
#orders_status = ["recieved", "preparing", "ready for delivery"]

# Main menu functionality
def main_menu(urban_brew_products,urban_brew_couriers,urban_brew_orders,orders_status):
    print("\n     You are in Main Menu      ")
    print("Please choose your option from 0, 1, 2 or 3:\n")
    #Menu repository (" 0	To Exit\n 1	View Products Menu\n 2	Add New Product\n 3	Update Existing Product\n 4	Delete a Product")
    print(" [0]	To Exit\n [1]	View Products Menu\n [2]	View Couriers Menu\n [3]	View Orders Menu\n")
    user_input = int(input('Please select 0 or 1 or 2 or 3:\n'))

    #function to exit app
    if user_input == 0:
        file_write() #saves the files in the csv format
        print("\nYou choose to EXIT the app")
        exit()
    
    #Products menu functionality
    elif user_input == 1:
        print("\nYou are in the product menu\n")
        print(" [0]	Main menu\n [1]	View Products\n [2]	Add New Product\n [3]	Update Existing Product\n [4]	Delete a Product")
        user_input = int(input('\nPlease select any number 0 to 4:\n'))
        if user_input == 0:
            def return_main_menu(): #function to return to main menu
                return main_menu(urban_brew_products,urban_brew_couriers,urban_brew_orders,orders_status)
            return_main_menu()

        elif user_input == 1: #prints product list
            def urban_brew_products_list():
                get_alltable_rows()
                print("These are the products available:\n")
                #prints product items in new line with product 'id'
                #get_alltable_rows()
                for product in urban_brew_products:
                    print(product['product_id'], product['product_name'])
                return(urban_brew_products)
            urban_brew_products_list()

        elif user_input == 2: #create or append a new product to the list 
            def urban_brew_products_appendlist():
                #new_product = {}
                print("Create a New Product:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    print("Connected to MySQL")
                    print('Please type new product Id which is not in the below list')
                    id_list = list()
                    for product in urban_brew_products:
                        id_list.append(product['product_id'])
                    print(id_list)
                    new_id = int(input('Product Id: '))
                    print('Please type new product name')
                    new_product_name = input('Product Name: ')
                    print('Please type in price of the new product')
                    new_product_price= float(input('Price: '))
                    cursor.execute("INSERT INTO `products` (`product_id`,`product_name`, `product_price`) VALUES ('{}', '{}','{}')".format(new_id, new_product_name, new_product_price))
                    connection.commit()
                    print(cursor.rowcount, "New product inserted successfully into products table")
                    cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                    if connection:
                        connection.close()
                        print('The pymysql connection is closed')
                return(urban_brew_products)
            urban_brew_products_appendlist()
        
        elif user_input == 3: #update or replace an existing product with new product to the list
            def urban_brew_products_replacelist():
                print("These are the products available:\n")
                #prints product items in new line with product 'id'
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    print("Connected to MySQL")
                    print('Please type product id which has to be updated')
                    for product in urban_brew_products:
                        print(product['product_id'], product['product_name'])
                    print('\nTo update or replace existing product...,\nchoose the id accociated with the product from above:')
                    user_input_product_id = int(input(''))
                    product_select_query = """select * from products where product_id = %s"""
                    cursor.execute(product_select_query,user_input_product_id)
                    record = cursor.fetchone()
                    print(record)
                    print('Type in newproduct name\n')
                    user_input_newproduct_name = input('name: ')
                    if len(user_input_newproduct_name) == 0:
                        user_input_newproduct_name = product['product_name']
                    else:
                        user_input_newproduct_name = user_input_newproduct_name 
                    print('Type in newproduct price\n')
                    user_input_newproduct_price = input('price: ')
                    if len(user_input_newproduct_price) == 0:
                        user_input_newproduct_price = product['product_price']
                    else:
                        user_input_newproduct_price = user_input_newproduct_price
                    product_update = """Update products set product_name = %s, product_price = %s where product_id = %s"""
                    user_input = (user_input_newproduct_name,user_input_newproduct_price,user_input_product_id)
                    cursor.execute(product_update, user_input)
                    connection.commit()
                    print("Updated record ")
                    cursor.execute(product_select_query,user_input_product_id)
                    record = cursor.fetchone()
                    print(record)
                    cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                    if connection:
                        connection.close()
                        print('The pymysql connection is closed')               
            urban_brew_products_replacelist()

        elif user_input == 4: #delete an existing product from the list
            def urban_brew_products_deletelist():
                print("These are the products available:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    print("Connected to MySQL")
                    print('Please type product id which has to be deleted')
                    for product in urban_brew_products:
                        print(product['product_id'], product['product_name'])
                    print('\nTo delete existing product...,\nchoose the id accociated with the product from above:')
                    user_input_product_id = int(input(''))
                    product_select_query = """select * from products where product_id = %s"""
                    cursor.execute(product_select_query,user_input_product_id)
                    record = cursor.fetchone()
                    print(record)
                    product_delete_query = """Delete from products where product_id = %s"""
                    cursor.execute(product_delete_query, user_input_product_id)
                    connection.commit()
                    #print('number of rows deleted', cursor.rowcount)
                    cursor.execute(product_delete_query, user_input_product_id)
                    records = cursor.fetchall()
                    if len(records) == 0:
                        print("Product record deleted successfully ")
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                        if connection:
                            connection.close()
                            print('The pymysql connection is closed')
                return(urban_brew_products)
            urban_brew_products_deletelist()

    elif user_input == 2: #Couriers menu
        print("\nYou are in the Couriers menu\n")
        print(" [0]	Main menu\n [1]	View Couriers\n [2]	Add New Courier\n [3]	Update Existing Courier\n [4]	Delete a Courier")
        user_input = int(input('\nPlease select any number 0 to 4:\n'))

        if user_input == 0:
            def return_main_menu():#function to return to main menu
                return main_menu(urban_brew_products,urban_brew_couriers,urban_brew_orders,orders_status)
            return_main_menu()

        elif user_input == 1: #prints couriers list
            def urban_brew_couriers_list():
                get_alltable_rows()
                print("These are the couriers available:\n")
                for courier in urban_brew_couriers:
                    print(courier['courier_id'], courier['courier_name'], courier['courier_phone'])
            urban_brew_couriers_list()

        elif user_input == 2: #create or append a new courier to the list 
            def urban_brew_couriers_appendlist():
                get_alltable_rows()
                print("Create a New Courier:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    # print("Connected to MySQL")
                    print('Please type new courier id which is not in the below list')
                    id_list = list()
                    for courier in urban_brew_couriers:
                     id_list.append(courier['courier_id'])
                    print(id_list)
                    new_id = int(input('Courier id: '))
                    print('Please type new courier name')
                    new_courier_name = input('Courier name: ')
                    print('Please type in phone of the new courier')
                    new_courier_phone= input('Courier phone: ')
                    cursor.execute("INSERT INTO `couriers` (`courier_id`,`courier_name`, `courier_phone`) VALUES ('{}', '{}','{}')".format(new_id, new_courier_name, new_courier_phone))
                    connection.commit()
                    print(cursor.rowcount, "New courier inserted successfully into couriers table")
                    cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                    if connection:
                        connection.close()
                        print('The pymysql connection is closed')
            urban_brew_couriers_appendlist()

        elif user_input == 3: #update or replace an existing courier with new courier to the list
            def urban_brew_couriers_replacelist():
                print("These are the couriers available:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    get_alltable_rows()
                    # print("Connected to MySQL")
                    print('Please type courier id which has to be updated')
                    for courier in urban_brew_couriers:
                        print(courier['courier_id'], courier['courier_name'])
                    print('\nTo update or replace existing courier...,\nchoose the id accociated with the product from above:')
                    user_input_courier_id = int(input(''))
                    courier_select_query = """select * from couriers where courier_id = %s"""
                    cursor.execute(courier_select_query,user_input_courier_id)
                    record = cursor.fetchone()
                    print(record)
                    print('Type in new courier name\n')
                    user_input_newcourier_name = input('name: ')
                    if len(user_input_newcourier_name) == 0:
                        user_input_newcourier_name = courier['courier_name']
                    else:
                        user_input_newcourier_name = user_input_newcourier_name 
                    print('Type in new courier phone\n')
                    user_input_newcourier_phone = input('phone: ')
                    if len(user_input_newcourier_phone) == 0:
                        user_input_newcourier_phone = courier['courier_phone']
                    else:
                        user_input_newcourier_phone = user_input_newcourier_phone
                    courier_update = """Update couriers set courier_name = %s, courier_phone = %s where courier_id = %s"""
                    user_input = (user_input_newcourier_name,user_input_newcourier_phone,user_input_courier_id)
                    cursor.execute(courier_update, user_input)
                    connection.commit()
                    print("Updated record ")
                    cursor.execute(courier_select_query,user_input_courier_id)
                    record = cursor.fetchone()
                    print(record)
                    cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                    if connection:
                        connection.close()
                        print('The pymysql connection is closed')
            urban_brew_couriers_replacelist()

        elif user_input == 4: #delete an existing courier
            def urban_brew_couriers_deletelist():
                print("These are the couriers available:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    get_alltable_rows()
                    print("Connected to MySQL")
                    print('Please type courier id which has to be deleted')
                    for courier in urban_brew_couriers:
                        print(courier['courier_id'], courier['courier_name'])
                    print('\nTo delete existing courier...,\nchoose the id accociated with the courier from above:')
                    user_input_courier_id = int(input(''))
                    courier_select_query = """select * from couriers where courier_id = %s"""
                    cursor.execute(courier_select_query,user_input_courier_id)
                    record = cursor.fetchone()
                    print(record)
                    courier_delete_query = """Delete from couriers where courier_id = %s"""
                    cursor.execute(courier_delete_query, user_input_courier_id)
                    connection.commit()
                    #print('number of rows deleted', cursor.rowcount)
                    cursor.execute(courier_delete_query, user_input_courier_id)
                    records = cursor.fetchall()
                    if len(records) == 0:
                        print("Courier record deleted successfully ")
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                        if connection:
                            connection.close()
                            print('The pymysql connection is closed')
            urban_brew_couriers_deletelist()

    #Orders menu functionality
    elif user_input == 3:
        print("\nYou are in the Orders menu\n")
        print(" [0]	Main Menu\n [1]	View Orders\n [2]	New Order\n [3]	Update Order Status\n [4]	Update Existing Order\n [5]	Delete a order\n")
        user_input = int(input('\nPlease select any number 0 to 5:\n'))

        if user_input == 0:
            def return_main_menu():#function to return to main menu
                return main_menu(urban_brew_products,urban_brew_couriers,urban_brew_orders,orders_status)
            return_main_menu()
        
        elif user_input == 1: #prints orders list
            def urban_brew_orders_list():
                print("These are the orders available:\n")
                #print(orders_records)
                get_alltable_rows()
                for order in urban_brew_orders:
                    print(f"{order['order_id']},{order['customer_name']},{order['customer_address']},{order['customer_phone']},{order['courier']},{order['status']},{order['items']}\n")
            urban_brew_orders_list()
        
        elif user_input == 2: # To create new order
            def urban_brew_append_orderslist():
                print("Create a New Order:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    print("Connected to MySQL")
                    get_alltable_rows()
                    print('Please type new order id which is not in the below list')
                    orderid_list = list()
                    for order in urban_brew_orders:
                        orderid_list.append(order['order_id'])
                    print(orderid_list)
                    new_order_id = int(input(''))
                    print('Please type new customer name')
                    new_order_customer_name = input('Name: ')
                    print('Please type new customer address')
                    new_order_customer_address = input('Address: ')
                    print('Please type new customer phone number')
                    new_order_customer_phone = input('Phone: ')
                    print("These are the couriers available:\n")
                    for courier in urban_brew_couriers:
                        print(courier['courier_id'], courier['courier_name'])
                    print('Choose the id accociated with the courier from the above:')
                    user_input_courier_id = int(input(''))
                    new_order_courier = user_input_courier_id
                    new_order_status = orders_status[1]['status']
                    for product in urban_brew_products:
                        print(product['product_id'], product['product_name'])
                    print('\nChoose the products with thier id from the above list seperated by space: ')
                    user_input_product_items = list(map(int, input('').split()))
                    new_order_items = user_input_product_items
                    cursor.execute("INSERT INTO `orders`(`customer_name`,`customer_address`, `customer_phone`, `courier`, `status`,`items`) VALUES ('{}','{}','{}','{}','{}','{}')".format(new_order_customer_name, new_order_customer_address, new_order_customer_phone, new_order_courier, new_order_status, new_order_items))
                    connection.commit()
                    print(cursor.rowcount, "New order inserted successfully into orders table")
                    cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                    if connection:
                        connection.close()
                        print('The pymysql connection is closed')
            urban_brew_append_orderslist()

        elif user_input == 3:
            def urban_brew_update_ordersstatus():
                print("These are the orders available:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    print("Connected to MySQL")
                    #print("Connected to MySQL")
                    print("These are the orders available:\n")
                    orders_select_query = "SELECT * FROM orders"
                    cursor.execute(orders_select_query)
                    orders_records = cursor.fetchall()
                    print(orders_records)
                    user_order_id = int(input('Please choose order id to change order status:'))
                    print(orders_status)
                    updated_order_status= int(input("choose new order status id from the list above: "))
                    if updated_order_status == 1:
                        updated_order_status = "recieved"
                    elif updated_order_status == 2:
                        updated_order_status = "preparing"
                    elif updated_order_status == 3:
                        updated_order_status = "ready for delivery"
                    order_update = """Update orders set status = %s where order_id = %s"""
                    user_input = (updated_order_status,user_order_id )
                    cursor.execute(order_update, user_input)
                    connection.commit()
                    #print("Updated order status ")
                    #cursor.execute(product_select_query,user_input_product_id)
                    #record = cursor.fetchone()
                    #print(record)
                    cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                        if connection:
                            connection.close()
                            print('The pymysql connection is closed')
            urban_brew_update_ordersstatus()
        
        elif user_input == 4:
            def urban_brew_update_existingorders():
                print("These are the orders available:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    print("Connected to MySQL")
                    get_alltable_rows()
                    orders_select_query = "SELECT * FROM orders"
                    cursor.execute(orders_select_query)
                    orders_records = cursor.fetchall()
                    print(orders_records)
                    print('Please type order id which has to be updated')
                    order_id = int(input(''))
                    print('Please type customer name to update')
                    customer_name = input('Name: ')
                    print('Please type customer address to update')
                    customer_address = input('Address: ')
                    print('Please type customer phone number to update')
                    customer_phone = input('Phone: ')
                    products_select_query = "SELECT * FROM products"
                    cursor.execute(products_select_query)
                    products_records = cursor.fetchall()
                    print(products_records)
                    for product in urban_brew_products:
                        print(product['product_id'], product['product_name'])
                    print('\nChoose the products with thier id from the above list seperated by space: ')
                    user_input_product_items = list(map(int, input('').split()))
                    items = user_input_product_items
                    print(items)
                    couriers_select_query = "SELECT * FROM couriers"
                    cursor.execute(couriers_select_query)
                    couriers_records = cursor.fetchall()
                    for courier in urban_brew_couriers:
                        print(courier['courier_id'], courier['courier_name'])
                    print('\nTo update existing courier...,\nchoose the id accociated with the courier from above:')
                    courier_id = int(input(''))
                    print(courier_id)
                    status_select_query = "SELECT * FROM order_status"
                    cursor.execute(status_select_query)
                    status_records = cursor.fetchall()
                    print(status_records)
                    update_input_status_id = int(input(''))
                    if update_input_status_id == 1:
                        update_input_status_id = "recieved"
                    elif update_input_status_id == 2:
                        update_input_status_id = "preparing"
                    elif update_input_status_id == 3:
                        update_input_status_id = "ready for delivery"
                    order_update = f"UPDATE orders SET customer_name =\'{customer_name}\', customer_address = \'{customer_address}\', customer_phone = {customer_phone}, courier = {courier_id}, status = \'{update_input_status_id}\', items = \'{items}\' WHERE order_id ={order_id};"
                    cursor.execute(order_update) 
                    connection.commit()
                    cursor.close()
                    # print("Updated order ")
                    # cursor.execute(order_update, order_id)
                    # record = cursor.fetchone()
                    # print(record)
                    #cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                        if connection:
                            connection.close()
                            print('The pymysql connection is closed')
            urban_brew_update_existingorders()

        elif user_input == 5:
            def urban_brew_delete_orders():
                print("These are the current Orders:\n")
                try:
                    load_dotenv()
                    host = os.environ.get("mysql_host")
                    user = os.environ.get("mysql_user")
                    password = os.environ.get("mysql_pass")
                    database = os.environ.get("mysql_db")
                    connection = pymysql.connect(
                        host,
                        user,
                        password,
                        database
                    )
                    cursor = connection.cursor()
                    #get_alltable_rows()
                    print("Connected to MySQL")
                    print('Please type order id which has to be deleted')
                    for order in urban_brew_orders:
                        print(order['order_id'], order['customer_name'], order['customer_phone'], order['items'])
                    print('\nTo delete existing order...,\nchoose the id accociated with the courier from above:')
                    user_input_order_id = int(input(''))
                    order_select_query = """select * from orders where order_id = %s"""
                    cursor.execute(order_select_query,user_input_order_id)
                    record = cursor.fetchone()
                    print(record)
                    order_delete_query = """Delete from orders where order_id = %s"""
                    cursor.execute(order_delete_query, user_input_order_id)
                    connection.commit()
                    #print('number of rows deleted', cursor.rowcount)
                    cursor.execute(order_delete_query, user_input_order_id)
                    records = cursor.fetchall()
                    if len(records) == 0:
                        print("Courier record deleted successfully ")
                        cursor.close()
                except pymysql.Error as error:
                    print("Failed to read data from table", error)
                finally:
                        if connection:
                            connection.close()
                            print('The pymysql connection is closed')
            urban_brew_delete_orders()
    #function call to export data to csv files         
    file_write()
    return  main_menu(urban_brew_products, urban_brew_couriers, urban_brew_orders, orders_status)

# Calling main function "main_menu" with products, couriers, orders, order status as arguments
main_menu(urban_brew_products, urban_brew_couriers, urban_brew_orders, orders_status)

        