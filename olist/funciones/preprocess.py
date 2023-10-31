import numpy as np
import pandas as pd

def transformar_columnas_datetime(dataframe, columnas):
    for columna in columnas:
        dataframe[columna] = pd.to_datetime(dataframe[columna])
    return dataframe


def tiempo_de_espera(orders, is_delivered=True):
    # filtrar por entregados y crea la varialbe tiempo de espera
    if is_delivered:
        orders = orders.query("order_status=='delivered'").copy()
    # compute wait time
    orders.loc[:, 'tiempo_de_espera'] = \
        (orders['order_delivered_customer_date'] -
         orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')
    return orders

def tiempo_de_espera_esperado(orders, is_delivered=True):
    # filtrar por entregados y crea la varialbe tiempo de espera
    if is_delivered:
        orders = orders.query("order_status=='delivered'").copy()
    # compute wait time
    orders.loc[:, 'tiempo_de_espera_esperado'] = \
        (orders['order_estimated_delivery_date'] -
         orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')
    return orders

def real_vs_esperado(orders, columna1, columna2):
    resultado = orders[columna1] - orders[columna2]
    resultado[resultado < 0] = 0
    orders['Real_vs_Esperado'] = resultado

    return orders


def puntaje_d_compra(df):
    df['5estrellas'] = df['review_score'].map(lambda x: 1 if x == 5 else 0)
    df['1estrella'] = df['review_score'].map(lambda x: 1 if x == 1 else 0)
    columnas_permitidas = ["order_id", "5estrellas", "1estrella", "review_score"]
    df = df[columnas_permitidas]
    return df

def calcular_numero_productos(df):
    df1 = df.copy()
    order_items_df = df1["order_items"].copy()
    df= order_items_df.groupby("order_id").agg(num_de_produc=("product_id","count")).reset_index()
    return df

def vendedores_unicos(df):
    df2=df.copy()
    d_df = df2["order_items"].copy()
    df= d_df.groupby("order_id").agg(vendedores_unicos=("seller_id","nunique"))
    return df

def calcular_precio_y_transporte(df):
    df3=df.copy()
    pyt=df3["order_items"].copy()
    df=pyt.groupby("order_id").agg(precio=("price","sum"),
                                    transporte=("freight_value","sum"))
    return df