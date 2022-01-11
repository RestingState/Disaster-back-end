from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    password = fields.Str()
    city_id = fields.Int()
    username = fields.Str()


# class CategorySchema(Schema):
#     id = fields.Int()
#     name = fields.Str()


class SatellitesSchema(Schema):
    norad_id = fields.Int()
    satname = fields.Str()
    owner = fields.Str()
    launchdate = fields.Date()
    launchsite = fields.Str()
    inclination = fields.Str()
    ascending_node_longitude = fields.Str()
    eccentricity = fields.Str()
    pericenter_argument = fields.Str()
    average_anomaly = fields.Str()
    call_frequency = fields.Str()


class StarsSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    right_ascension = fields.Str()
    declination = fields.Str()
    flux_visible_light = fields.Str()
    parallax = fields.Str()
    spectral_type = fields.Str()
