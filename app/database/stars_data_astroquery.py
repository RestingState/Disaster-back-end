from astroquery.simbad import Simbad
from app import Session
from app.models.models import Star


def update_stars_info(ra: str, dec: str, radius: str):
    session = Session()

    Simbad.remove_votable_fields('coordinates')
    Simbad.add_votable_fields('ra', 'dec', 'flux(V)', 'plx', 'sp')
    result_table1 = Simbad.query_criteria(f'region(box, GAL, {ra} {dec}, {radius})', otype='*')

    if not result_table1:
        return

    for record in result_table1:
        star_data = Star()

        if Session().query(Star).filter_by(name=record[0]).first():
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


ra = 0
dec = -90
radius = '1d 1d'

for i in range(1, 360):
    for j in range(1, 181):
        update_stars_info(str(ra), str(dec), radius)
        print(ra, dec)
        dec = j - 90
    dec = -90
    ra = i
