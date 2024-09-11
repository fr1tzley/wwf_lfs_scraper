import datetime
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

create_table_query = """
CREATE TABLE record(
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200),
  article MEDIUMTEXT,
  event_date DATE,
  publish_date DATE, 
  link VARCHAR(300),
  query VARCHAR(300),
  google_url VARCHAR(200),
  source VARCHAR(100),
  avg_relative_humidity_2m FLOAT(23),
  avg_temperature_2m FLOAT(23),
  daylight_duration FLOAT(23),
  precipitation_hours FLOAT(23),
  precipitation_sum FLOAT(23),
  rain_sum FLOAT(23),
  snowfall_sum FLOAT(23),
  sunshine_duration FLOAT(23),
  temperature_2m_max FLOAT(23),
  temperature_2m_min FLOAT(23),
  weather_code FLOAT(3),
  wind_speed_max FLOAT(23),
  death_human INT,
  death_elephant INT,
  injury_human INT,
  injury_elephant INT,
  latitude FLOAT(23),
  longitude FLOAT(23),
  country VARCHAR(100),
  state VARCHAR(100),
  village_place VARCHAR(100)
)
"""

insert_row_query = """
INSERT INTO record(title, article, event_date, publish_date, link, query, google_url, source, avg_relative_humidity_2m, avg_temperature_2m, daylight_duration, precipitation_hours, precipitation_sum, rain_sum, snowfall_sum, sunshine_duration, 
temperature_2m_max, temperature_2m_min, weather_code, wind_speed_max, death_human, death_elephant, injury_human, injury_elephant, latitude, longitude, country, state, village_place)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

"""

check_date_exists_query = """
SELECT count(*) FROM record WHERE publish_date = %s
"""


def make_table():
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
        connection.commit()

def check_date(date):
  with connection.cursor() as cursor:
    cursor.execute(check_date_exists_query,  (date,))
    result = cursor.fetchall()[0][0]
    return result > 0

def add_row(row):
  with connection.cursor() as cursor:
    cursor.execute(insert_row_query, 
      (row["Title"],
      row["Article"],
      row["Date (Event)"],
      row["Date Published"],
      row["Links"],
      row["Query"],
      row["Google URL"],
      row["Source"],
      row["average_relative_humidity_2m"],
      row["average_temperature_2m"],
      row["daylight_duration"],
      row["precipitation_hours"],
      row["precipitation_sum"],
      row["rain_sum"],
      row["snowfall_sum"],
      row["sunshine_duration"],
      row["temperature_2m_max"],
      row["temperature_2m_min"],
      row["weather_code"],
      row["wind_speed_10m_max"],
      row["death_human"],
      row["death_elephant"],
      row["injury_human"],
      row["injury_elephant"],
      row["lat"],
      row["lon"],
      row["Country"],
      row["State"],
      row["Village/Place"]))
    connection.commit()
