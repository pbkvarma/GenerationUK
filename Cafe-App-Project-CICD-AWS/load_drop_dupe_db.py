from extract import df_connect


def load_store(store_df):
    conn = df_connect()
    cur = conn.cursor()
    for x in store_df['store']:
        sql = f'''CREATE TABLE temp_data (store TEXT NOT NULL);
                INSERT INTO temp_data(store) VALUES ('{x}');
                INSERT INTO store_table(store)
                SELECT DISTINCT store
                FROM temp_data
                WHERE NOT EXISTS (
                SELECT 'X'
                FROM store_table
                WHERE
                temp_data.store = store_table.store
                );

                DROP TABLE temp_data'''
        cur.execute(sql)
        conn.commit()
    print("Any new store will be inserted")


def load_product(products_df):
    conn = df_connect()
    cur = conn.cursor()
    for x in products_df.values:
        sql = f'''CREATE TABLE temp_product_table (product_name text NOT NULL, product_flavour text NOT NULL, product_price float NOT NULL);
                INSERT INTO temp_product_table(product_name, product_flavour, product_price) VALUES ('{x[0]}', '{x[1]}', '{x[2]}');
                INSERT INTO product_table(product_name, product_flavour, product_price)
                SELECT DISTINCT product_name, product_flavour, product_price
                FROM temp_product_table
                WHERE NOT EXISTS (
                SELECT 'X'
                FROM product_table
                WHERE
                temp_product_table.product_name = product_table.product_name
                AND temp_product_table.product_flavour = product_table.product_flavour
                AND temp_product_table.product_price = product_table.product_price
                );
                DROP TABLE temp_product_table;
                '''
        cur.execute(sql)
        conn.commit()
    print("Any new product will be inserted")


def load_customer(customer_df):
    conn = df_connect()
    cur = conn.cursor()
    for x in customer_df.values:
        sql = f'''CREATE TABLE temp_customer (customer_name text NOT NULL, card_number text NOT NULL);
                INSERT INTO temp_customer(customer_name, card_number) VALUES ('{x[0]}', '{x[1]}');
                INSERT INTO customer_table(customer_name, card_number)
                SELECT DISTINCT customer_name, card_number
                FROM temp_customer
                WHERE NOT EXISTS (
                SELECT 'X'
                FROM customer_table
                WHERE
                temp_customer.customer_name = customer_table.customer_name
                AND temp_customer.card_number = customer_table.card_number
                );
                DROP TABLE temp_customer;
                '''
        cur.execute(sql)
        conn.commit()
    print("Any new customer will be inserted")
