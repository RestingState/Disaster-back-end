import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive


class Exoplanets:
    def __init__(self):  # coordinates == 0
        self.right_ascension = 0
        self.declination = 0
        self.radius = 0

    def __init__(self, ra, dec, rad):  # set coordinates
        self.right_ascension = ra
        self.declination = dec
        self.radius = rad

    def get_Exoplanets_By_Coord(self):
        """
        :return: dict
        """
        try:
            data = NasaExoplanetArchive.query_region(
                table="pscomppars", coordinates=SkyCoord(ra=self.right_ascension * u.deg, dec=self.declination * u.deg),
                radius=self.radius * u.deg)
        except Exception as e:
            return "Error. Wrong data."

        return data

    @staticmethod
    def get_Exoplanets():
        """
        :return: dict (data with fields: "kepid", "kepoi_name", "kepler_name", "koi_fittype", "koi_score", "sky_coord")
        """
        return NasaExoplanetArchive.query_criteria(table="cumulative", select="*")