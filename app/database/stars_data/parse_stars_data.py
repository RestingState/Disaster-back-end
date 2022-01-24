from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from astroquery.simbad import Simbad
from app.models.models import Stars
from app import Session

url = 'http://simbad.u-strasbg.fr/simbad/sim-coo?Coord=1+%2B01+00+00.0000000000&Radius=1&Radius.unit=deg&submit=submit+query'
path_x_btn = "//img[@id='CLEAR']"
path_entries_btn = "//select[@name='datatable_length']"
path_coords_set = "//input[@name='Coord']"
path_10000_query = "//option[@value='10000']"
path_sumbit_query_btn = "//input[@name='submit']"
driver = webdriver.Chrome(r"C:\Users\23485\Downloads\chromedriver\chromedriver.exe")
Simbad.remove_votable_fields('coordinates')
Simbad.add_votable_fields('ra', 'dec', 'flux(V)', 'plx', 'sp')
session = Session()


def fill_db(name):
    record = Simbad.query_object(name)[0]
    star_data = Stars()

    if Session().query(Stars).filter_by(name=record[0]).first():
        return

    if str(record[0]) == '' or str(record[0]) == '--':
        star_data.name = None
    else:
        star_data.name = record[0]

    if str(record[1]) == '' or str(record[1]) == '--':
        star_data.right_ascension = None
    else:
        star_data.right_ascension = record[1]

    if str(record[2]) == '' or str(record[2]) == '--':
        star_data.declination = None
    else:
        star_data.declination = record[2]

    if str(record[3]) == '' or str(record[3]) == '--':
        return
    else:
        star_data.flux_visible_light = record[3]

    if str(record[4]) == '' or str(record[4]) == '--':
        star_data.parallax = None
    else:
        star_data.parallax = record[4]

    if str(record[5]) == '' or str(record[5]) == '--':
        star_data.spectral_type = None
    else:
        star_data.spectral_type = record[5]

    session.add(star_data)


def get_data():
    table_id = driver.find_element(By.ID, 'datatable')
    rows = table_id.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        row_info = row.text
        row_info = row_info[row_info.find(' ') + 1:]

        if row_info.find('*') != -1:
            index = row_info.rindex('*')
        else:
            continue

        if index < row_info.find(' '):
            continue

        while row_info[index] != ' ':
            index -= 1
        row_info = row_info[:index]
        index -= 1
        while row_info[index] != ' ':
            index -= 1
        star_name = row_info[:index]
        fill_db(star_name)


def open_browser():
    driver.get(url)

    driver.find_element_by_xpath(path_entries_btn).click()
    time.sleep(1)

    driver.find_element_by_xpath(path_10000_query).click()
    time.sleep(1)

    for i in range(1, 360, 1):
        ra = i
        for j in range(-900, 900, 10):
            dec = int(j / 10)
            data = str(ra) + ' ' + str(dec)
            driver.find_element_by_xpath(path_x_btn).click()
            time.sleep(1)
            coords_input = driver.find_element_by_xpath(path_coords_set)
            coords_input.send_keys(data)
            time.sleep(1)
            driver.find_element_by_xpath(path_sumbit_query_btn).click()
            time.sleep(4)
            get_data()
            session.commit()
            print(data)
    session.close()

    time.sleep(5)


open_browser()
