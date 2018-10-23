product_table="""CREATE TABLE IF NOT EXISTS products(
						product_id serial PRIMARY KEY,
						product_name VARCHAR(20) NOT NULL,
						price VARCHAR(20) NOT NULL,
						quantity INT NOT NULL
					)"""

sales_table="""CREATE TABLE IF NOT EXISTS sales(
						sales_id serial PRIMARY KEY,
						attendant VARCHAR(20) NOT NULL,
						product VARCHAR(20) NOT NULL,
						price VARCHAR(20) NOT NULL,
						quantity INT NOT NULL
					)"""
user_table="""CREATE TABLE IF NOT EXISTS my_users(
						user_id serial PRIMARY KEY,
						username VARCHAR(20) NOT NULL,
						password VARCHAR(20) NOT NULL,
						confirmpass VARCHAR(20) NOT NULL,
						addres VARCHAR(30) NOT NULL,
						role VARCHAR(10) NOT NULL
					)"""

queries = [product_table, sales_table, user_table]