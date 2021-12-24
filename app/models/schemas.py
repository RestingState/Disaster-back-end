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
