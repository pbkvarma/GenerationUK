from extract import df_connect


def create_table():
    conn = df_connect()
    cur = conn.cursor()
    try:

        ## create transactions table ## as ** order_df
        create_order_table = '''CREATE TABLE IF NOT EXISTS order_table(
                                order_id        integer,
                                time_stamp      timestamptz,
                                store_id        integer,
                                total_price      float,
                                customer_id      integer
                                );'''

        ## create product table ## as ** basket_df
        create_product_table = '''CREATE TABLE IF NOT EXISTS product_table(
                                product_id      INT identity(1, 1) PRIMARY KEY NOT NULL,
                                product_name	TEXT,
                                product_flavour    TEXT,  	
                                product_price	 float 
                                );'''

        ## create customer table ## as ** customer_df
        create_customer_table = '''CREATE TABLE IF NOT EXISTS customer_table(
                                customer_id     INT identity(1, 1) PRIMARY KEY NOT NULL,
                                customer_name	TEXT,
                                card_number	    text                          
                                );'''

        ## create store table ## as ** store_df
        create_store_table = '''CREATE TABLE IF NOT EXISTS  store_table(
                                store_id     INT identity(1, 1) PRIMARY KEY NOT NULL,
                                store     	 TEXT
                                );'''

        ## create basket table ## as ** basket_df
        create_basket_table = '''CREATE TABLE IF NOT EXISTS  basket_table(
                                order_id         integer,
                                product_id     	 integer,
                                customer_id      integer,
                                store_id         integer,
                                time_stamp       timestamptz,
                                constraint fk_product
                                    foreign key (product_id) 
                                    REFERENCES product_table (product_id),
                                constraint fk_customer
                                    foreign key (customer_id) 
                                    REFERENCES customer_table (customer_id),
                                constraint fk_store
                                    foreign key (store_id) 
                                    REFERENCES store_table (store_id)
                                );'''

        # executing tables
        cur.execute(
            f' {create_order_table}{create_product_table}{create_customer_table}{create_store_table}{create_basket_table}')
        print('tables have been created!!')
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
