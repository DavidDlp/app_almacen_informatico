import pandas as pd
from db import engine

conn = engine

def getProductMoreBuy():
    query = """SELECT COUNT(b.product_id) Quantity, a.product_name Product_Name
                             FROM products a
                             INNER JOIN orders b
                             ON a.id_product = b.product_id
                             GROUP BY product_name
                             ORDER BY Quantity DESC
                             """

    dates = pd.read_sql_query(query, conn)
    return dates

def getProductMoreApplyFor():
    query = """SELECT COUNT(b.product_id) Quantity, a.product_name Product_Name
                             FROM products a
                             INNER JOIN applyFor b
                             ON a.id_product = b.product_id
                             GROUP BY product_name
                             ORDER BY Quantity DESC
                             """
    dates = pd.read_sql_query(query, conn)
    return dates




