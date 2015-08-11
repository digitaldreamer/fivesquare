from cornice.schemas import CorniceSchema
from colander import MappingSchema, SchemaNode, String, Boolean, drop


class AuthSchema(MappingSchema):
    email = SchemaNode(String(), location='body', type='str', description="The user's email")
    password = SchemaNode(String(), location='body', type='str', description="The user's password")


class NewUserSchema(MappingSchema):
    email = SchemaNode(String(), location='body', type='str', description="The user's email")
    password = SchemaNode(String(), location='body', type='str', description="The user's password.")


class UserSchema(MappingSchema):
    active = SchemaNode(Boolean(), location='body', type='bool', default=False, missing=False, description="[true|false] Whether or not the user is active")
    email = SchemaNode(String(), location='body', type='str', description="The user's email.")


class UserPasswordSchema(MappingSchema):
    password = SchemaNode(String(), location='body', type='str', description="The user's new password.")
