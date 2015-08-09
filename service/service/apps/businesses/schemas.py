from cornice.schemas import CorniceSchema
from colander import (
    MappingSchema,
    SchemaNode,
    String,
    Integer,
    Float,
    Boolean,
    OneOf,
    drop,
)


class BusinessesSchema(MappingSchema):
    lat = SchemaNode(Float(), location='querystring', type='float', default=0)
    lng = SchemaNode(Float(), location='querystring', type='float', default=0)
    distance = SchemaNode(Float(), location='querystring', type='float', default=1)
    units = SchemaNode(String(), location='querystring', type='str', validator=OneOf(['imperial', 'metric']), default='imperial')
    limit = SchemaNode(Integer(), location='querystring', type='int', default=100)
    offset = SchemaNode(Integer(), location='querystring', type='int', default=0)


class NewBusinessSchema(MappingSchema):
    name = SchemaNode(String(), location='body', type='str')
    street1 = SchemaNode(String(), location='body', type='str')
    street2 = SchemaNode(String(), location='body', type='str', missing='', default='')
    city = SchemaNode(String(), location='body', type='str')
    state = SchemaNode(String(), location='body', type='str')
    postal_code = SchemaNode(String(), location='body', type='str', missing='', default='')

class BusinessSchema(MappingSchema):
    reviews = SchemaNode(Boolean(), location='querystring', type='bool', default=False)
