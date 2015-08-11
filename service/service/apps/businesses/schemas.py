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
    lat = SchemaNode(Float(), location='querystring', type='float', default=0, description='the latitude of the center')
    lng = SchemaNode(Float(), location='querystring', type='float', default=0, description='the longitude of the center')
    distance = SchemaNode(Float(), location='querystring', type='float', default=1, description="the distance from the center to restrict search in miles or km depending on the units")
    units = SchemaNode(String(), location='querystring', type='str', validator=OneOf(['imperial', 'metric']), default='imperial', description="[imperial|metric] the units to search in miles or km")
    limit = SchemaNode(Integer(), location='querystring', type='int', default=100, description="the max number of returned businesses")
    offset = SchemaNode(Integer(), location='querystring', type='int', default=0, description="the skipped businesses in the list")


class NewBusinessSchema(MappingSchema):
    name = SchemaNode(String(), location='body', type='str', description="the business name")
    street1 = SchemaNode(String(), location='body', type='str', description="the business street 1")
    street2 = SchemaNode(String(), location='body', type='str', missing='', default='', description="the business street 2")
    city = SchemaNode(String(), location='body', type='str', description="the business city")
    state = SchemaNode(String(), location='body', type='str', description="the business state")
    postal_code = SchemaNode(String(), location='body', type='str', missing='', default='', description="the business postal code")


class BusinessSchema(MappingSchema):
    reviews = SchemaNode(Boolean(), location='querystring', type='bool', default=False, description="[true|false] a flag to tell to include the reviews or not")
