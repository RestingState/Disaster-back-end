import time
import astropy.coordinates as coord
from astroquery.simbad import Simbad
from app import Session
from app.models.models import Stars
import astropy.units as u


def update_stars_info(ra: str, dec: str, radius: str):
    session = Session()

    Simbad.remove_votable_fields('coordinates')
    Simbad.add_votable_fields('ra', 'dec', 'flux(V)', 'plx', 'sp', 'otype')
    result_table1 = Simbad.query_region(coord.SkyCoord(f"{ra} {dec}", frame='icrs'), radius=radius)
    if not result_table1:
        print('no data')
        return
    for record in result_table1:
        if record[6] == 'Star' or str(record[6]).find('*') != -1:
            pass
        else:
            continue

        star_data = Stars()

        if Session().query(Stars).filter_by(name=record[0]).first():
            continue

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
            continue
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

    session.commit()
    session.close()


ra = 'h0m0s'
radius = '0.5d'
minus = True

for i in range(0, 24):
    rightasc = str(i) + ra
    hours = -6
    minutes = 0
    dec = f'{hours}h{minutes}m0s'
    update_stars_info(rightasc, str(dec), radius)
    print(rightasc, dec)
    minus = True
    for j in range(0, 180):
        if hours < 0 or minus:
            if minutes - 4 < 0:
                minutes = 60 + minutes - 4
                hours += 1
            else:
                if hours == 0 and minutes - 4 == 0:
                    minus = False
                minutes -= 4
        else:
            if minutes + 4 >= 60:
                minutes = minutes + 4 - 60
                hours += 1
            else:
                minutes += 4
        if minus and hours == 0:
            dec = f'-{hours}h{minutes}m0s'
        else:
            dec = f'{hours}h{minutes}m0s'
        update_stars_info(rightasc, str(dec), radius)
        print(rightasc, dec)
