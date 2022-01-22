import json
import requests
from app.api.horizon_api_objects_list import objects_list
from app.models.models import PlanetCoordinates


class Planet:
    """
    Class for getting planets and other space objects info using horizons api.
    """

    month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    @staticmethod
    def __object_name_code(object_name):
        """
        object_name: str

        Returns object code for the object_name according to api.
        """

        if not object_name:
            return 'wrong name'

        return objects_list.get(object_name, 'wrong name')

    @staticmethod
    def get_dec_and_ra_in_time_interval(object_name, start_time, stop_time, step_unit='d', step_int=1):
        """
        object_name: str(like 'Mars'(list is provided in planet_list.py))
        start_time: str('YYYY-MMM-DD {HH:MN}')
        stop_time: str('YYYY-MMM-DD {HH:MN}')
        step_unit: str, Default = 'd'
        step_int: int, Default = 1

        Returns dict where keys are dates(like '1111-Jan-01 00:00')
        and values are dicts with keys
        'dec' for declination(HH MM SS.ff{ffff} in str) and
        'ra' for right accession(sDD MN SC.f{ffff} in str)

        step_unit possible values:
        'd' - days
        'h' - hours
        'm' - minutes
        'y' - years
        'mo' - months
        """

        step_units = ['d', 'h', 'm', 'y', 'mo']
        if step_unit not in step_units:
            raise ValueError('Wrong step_unit provided')
        elif step_int <= 0 or not isinstance(step_int, int):
            raise ValueError('Wrong step_int provided')

        step_size = f'{step_int}%20{step_unit}'

        object_code = Planet.__object_name_code(object_name)
        if object_code == 'wrong name':
            raise ValueError('Wrong space object name')

        url = f"https://ssd.jpl.nasa.gov/api/horizons.api" \
              f"?format=json" \
              f"&COMMAND='{object_code}'" \
              f"&OBJ_DATA='NO'" \
              f"&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'" \
              f"&CENTER='500@399'" \
              f"&START_TIME='{start_time}'&STOP_TIME='{stop_time}'&STEP_SIZE='{step_size}'" \
              f"&QUANTITIES='2'"

        try:
            response = json.loads(requests.get(url).text)
            # print(response)
            data = response['result']
        except Exception:
            raise RuntimeError('Api error')
        # print(data)

        if 'Bad dates -- start must be earlier than stop' in data:
            raise ValueError('Bad dates -- start must be earlier than stop')
        elif 'Cannot interpret date' in data:
            raise ValueError('Cannot interpret date.')
        elif 'Observer table for observer=target disallowed.' in data:
            raise RuntimeError('Can not get position from the observing point')
        elif 'error' in response.keys():
            print(response['error'])
            raise RuntimeError('Api error')
        elif '$$SOE' not in data:
            raise RuntimeError('Api error')
        elif not data:
            raise RuntimeError('Api error')

        lines = data.split('\n')
        mode = 'do not read'
        result = dict()

        for line in lines:
            if line == '$$SOE':
                mode = 'read'
                continue
            if line == '$$EOE':
                mode = 'do not read'

            if mode == 'read':
                info = dict()
                info['ra'] = line[23:34]
                info['dec'] = line[35:]
                date = line[1:12].split('-')
                result[f'{date[0]}-{Planet.month_dict[date[1]]}-{date[2]}'] = info

        return result


def load_planet_coordinates(planet, coordinates, session):
    for key, value in coordinates.items():
        dec = value.get('dec', None)
        ra = value.get('ra', None)
        if not dec or not ra:
            return 'error'
        try:
            data = PlanetCoordinates(planet_id=planet.id, date=key, dec=dec, ra=ra)
            session.add(data)
            session.commit()
        except Exception:
            return 'error'
    return None


# Examples
# print(Planet.get_dec_and_ra_in_time_interval('Mercury', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Venus', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Mars', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Jupiter', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Saturn', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Uranus', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Neptune', '2021-01-01', '2021-01-10'))
# print(Planet.get_dec_and_ra_in_time_interval('Mars', '2021-01-01', '2022-12-01', step_unit='mo', step_int=2))
