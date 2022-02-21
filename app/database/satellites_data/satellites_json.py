import requests

import psycopg2

BASE = "https://api.n2yo.com/rest/v1/satellite/"
apiKey = 'WYY6AU-RLC84J-6AEU6S-4T6J'

def insert_sat_data(sat_id,sat_data):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO satellite_data_raw (norad_id,sat_data)
             VALUES(%s,%s) RETURNING norad_id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        # connect to the PostgreSQL database
        conn = psycopg2.connect(user="jwybdxdlrzhdqo", password="43dbc041a5cdd9494c373cc1ba1a74dfb0e06bd0b35783472cf8a2c0d5f471a2",host="ec2-54-78-36-245.eu-west-1.compute.amazonaws.com", port="5432", database="dcdois4sl8pdd2")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (sat_id,sat_data))
        # get the generated id back
        sat_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id


def get_TLE(id):
    response = requests.get(f"{BASE}tle/{id}&apiKey={apiKey}")
    response_json = response.json()
    return response_json

def get_satellite_position(id, observer_lat, observer_lng, observer_alt, seconds):
    response = requests.get(f"{BASE}positions/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{seconds}/&apiKey={apiKey}")
    return response.json()
