from cornice.schemas import CorniceSchema
from colander import MappingSchema, SchemaNode, String, Integer, Boolean, drop


class BusinessesSchema(MappingSchema):
    limit = SchemaNode(Integer(), location='querystring', type='int', default=100)
    offset = SchemaNode(Integer(), location='querystring', type='int', default=0)
