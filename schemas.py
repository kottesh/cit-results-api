from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True, load_only=True)
