import os

from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

connection = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DATABASE
)


date_key = "date"

base_query = 'SELECT * FROM record WHERE event_date >= {start_date} AND event_date <= {end_date}'

addon_query = " AND {col} {op} {val}"

opdict = {
    "eq": "=",
    "neq": "!=",
    "lt": "<",
    "gt": ">",
    "leq": "<=",
    "geq": ">="
}

def query_overall(query_ob, start_date, end_date):
    s = start_date.strftime("%Y%m%d")
    e = end_date.strftime("%Y%m%d")
    query = base_query.format(start_date = s, end_date = e)

    if query_ob["country"] != "All":
        query += addon_query.format(col="country", op="=", val=f'"{query_ob["country"]}"')
    if query_ob["edeathOp"] != "nf":
        query += addon_query.format(col="death_elephant", op=opdict[query_ob["edeathOp"]], val=query_ob["edeathNum"])
    if query_ob["hdeathOp"] != "nf":
        query += addon_query.format(col="death_human", op=opdict[query_ob["hdeathOp"]], val=query_ob["hdeathNum"])
    if query_ob["einjuryOp"] != "nf":
        query += addon_query.format(col="injury_elephant", op=opdict[query_ob["einjuryhOp"]], val=query_ob["einjuryNum"])
    if query_ob["hinjuryOp"] != "nf":
        query += addon_query.format(col="injury_human", op=opdict[query_ob["hinjuryhOp"]], val=query_ob["hinjuryNum"])


    with connection.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        result = pd.DataFrame.from_records(res, columns = [desc[0] for desc in cursor.description])
        return result

def query_country(country, df):
    df = df.loc[df["Country"] == country]

    return df

def query_numeric_key(df, key, op, num):
    if op == "eq":
        df = df.loc[df[key] == num]
    elif op == "neq":
        df = df.loc[df[key] != num]
    elif op == "gt":
        df = df.loc[df[key] > num]
    elif op == "lt":
        df = df.loc[df[key] < num]
    elif op == "geq":
        df = df.loc[df[key] >= num]
    else:
        df = df.loc[df[key] <= num]
    return df