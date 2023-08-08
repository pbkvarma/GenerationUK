import psycopg2
import psycopg2.extras as extras

from extract import *


def create_orders_df(df):
    """
    - Returns a df containing orders and the accompanying information
    - branch_id and cust_id columns rely on data which has to be loaded into 
    the db first (for the queries)
    """
    orders_df_without_ids = df[['timestamp', 'store',
                                'customer_name', 'cash_or_card', 'card_number', 'total_price']]

    #Check for duplicates
    orders_df_without_ids = orders_df_without_ids.drop_duplicates()

    #Query branch_ids and cust_ids from their tables and populate into orders_table
    branch_vals = [val for val in orders_df_without_ids['store']]
    branch_ids = []
    conn = df_connect()
    cur = conn.cursor()
    for branch_val in branch_vals:
        sql = \
            f'''
            SELECT store_id
            FROM store_table
            WHERE store = '{branch_val}'
            '''
        cur.execute(sql)
        record = cur.fetchone()
        #Returns a tuple with id at idx = 0
        branch_ids.append(record[0])

    cust_vals = [val for val in orders_df_without_ids['customer_name']]
    cust_ids = []
    conn = df_connect()
    cur = conn.cursor()
    for cust_val in cust_vals:
        sql = \
            f'''
            SELECT customer_id
            FROM customer_table
            WHERE customer_name = '{hash_value(cust_val)}'
            '''
        cur.execute(sql)
        record = cur.fetchone()
        cust_ids.append(record[0])

    conn.close()

    #Make new df with the new columns
    orders_df = pd.DataFrame(orders_df_without_ids, columns=[
                             'time_stamp', 'branch_id', 'cust_id', 'payment_type', 'total_price'])

    #Populate id columns with queried values
    orders_df['branch_id'] = branch_ids
    orders_df['cust_id'] = cust_ids

    return orders_df


def create_basket_df(df):
    """
    - Returns a df containing individual products from each order
    - cols: order_id, product_id
    """
    products_df = fetch_products(df)

    #Create order_id for every product in each order
    products_df['order_id'] = products_df.index

    #Names and flavours of all individual products from every order
    product_names = []

    #TODO: refactor this? Repeating code from create_products_df()
    for product in products_df['basket_items']:
        details = product.split(' - ')
        if 'Flavoured' in product:
            product_and_flavour = f'{details[0]} {details[1]}'
            product_names.append(product_and_flavour)
        else:
            product_no_flavour = f'{details[0]} Original'
            product_names.append(product_no_flavour)

    #Query products table to get all the product_names and product_ids
    conn = df_connect()
    cur = conn.cursor()

    sql = \
        '''
        SELECT product_id, product_name, product_flavour
        FROM product_table
        '''
    cur.execute(sql)

    #List of tuples where each tuple is a row in products table
    products = cur.fetchall()

    #Dict - keys: product_names, values: product_ids (from products table)
    products_dict = {}

    for product in products:
        product_name = f'{product[1]} {product[2]}'
        product_id = str(product[0])
        products_dict[product_name] = product_id

    #Get product_ids from products_dict
    product_ids = [products_dict.get(product_name)
                   for product_name in product_names]

    #Create dict to be loaded into df which is then loaded to db
    basket_dict = {
        'product_id': product_ids,
        'order_id': products_df['order_id']
    }

    basket_df = pd.DataFrame(basket_dict)

    return basket_df


def execute_values(df, table):
    conn = df_connect()
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    # SQL query to execute

    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cur = conn.cursor()
    try:
        extras.execute_values(cur, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    print("the latest order has been inserted")
