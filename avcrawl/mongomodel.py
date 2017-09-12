from mongoengine import *
from mongoengine.fields import *

connect('avproject', host='localhost', port=27019)


def field_value(field, value):
    '''
    Converts a supplied value to the type required by the field.
    If the field requires a EmbeddedDocument the EmbeddedDocument
    is created and updated using the supplied data.
    '''
    if field.__class__ in (ListField, SortedListField):
        # return a list of the field values
        return [
            field_value(field.field, item)
            for item in value]

    elif field.__class__ in (
            EmbeddedDocumentField,
            GenericEmbeddedDocumentField,
            ReferenceField,
            GenericReferenceField):

        embedded_doc = field.document_type()
        update_document(embedded_doc, value)
        return embedded_doc
    else:
        return value


def update_document(doc, data):
    ''' Update an document to match the supplied dictionary.
    '''
    for key, value in data.iteritems():
        if hasattr(doc, key):
            value = field_value(doc._fields[key], value)
            setattr(doc, key, value)
        else:
            # handle invalid key
            pass

    return doc


def update_dynamic_doc(doc, data):
    for key, value in data.iteritems():
        if (key in doc._fields):
            value = field_value(doc._fields[key], value)
        setattr(doc, key, value)


class Config(DynamicDocument):
    _id = StringField()
    pass


class TagGroup(DynamicDocument):
    _id = StringField()
    pass


class Tag(DynamicDocument):
    _id = StringField()
    pass


class Role(DynamicDocument):
    _id = StringField()
    pass


class Publish(DynamicDocument):
    _id = StringField()
    pass


class Video(DynamicDocument):
    _id = StringField()
    img = StringField()
    # tags = ListField(ReferenceField(Tag))
    pass
