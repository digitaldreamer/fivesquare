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


class ReviewSchema(MappingSchema):
    text = SchemaNode(String(), location='body', type='str')
    tags = SchemaNode(String(), location='body', type='str', missing='')
    rating = SchemaNode(Integer(), location='body', type='int', validator=OneOf([1, 2, 3, 4, 5]))
