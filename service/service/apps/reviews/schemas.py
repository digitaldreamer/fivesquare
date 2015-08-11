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
    text = SchemaNode(String(), location='body', type='str', description='the review text')
    tags = SchemaNode(String(), location='body', type='str', missing='', description='the freeform tags separated by ":"  i.e. "hello:world"')
    rating = SchemaNode(Integer(), location='body', type='int', validator=OneOf([1, 2, 3, 4, 5]), description="[1|2|3|4|5] the five star rating")
