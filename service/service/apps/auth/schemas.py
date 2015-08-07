from cornice.schemas import CorniceSchema
from colander import MappingSchema, SchemaNode, String, Boolean, drop


class AuthSchema(MappingSchema):
    email = SchemaNode(String(), location='body', type='str')
    password = SchemaNode(String(), location='body', type='str')


class NewUserSchema(MappingSchema):
    email = SchemaNode(String(), location='body', type='str')
    password = SchemaNode(String(), location='body', type='str')


class UserSchema(MappingSchema):
    active = SchemaNode(Boolean(), location='body', type='bool', missing=False)
    email = SchemaNode(String(), location='body', type='str')


class UserPasswordSchema(MappingSchema):
    password = SchemaNode(String(), location='body', type='str')
