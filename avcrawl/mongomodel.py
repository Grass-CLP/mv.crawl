#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/6.
# email to LipsonChan@yahoo.com
#

from mongoengine import connect, DynamicDocument
from mongoengine.fields import *

from config import mongodb_conf

connect(mongodb_conf['name'], host=mongodb_conf['host'], port=mongodb_conf['port'])


def field_value(field, value):
    """
    Converts a supplied value to the type required by the field.
    If the field requires a EmbeddedDocument the EmbeddedDocument
    is created and updated using the supplied data.
    :param field:
    :param value:
    :return:
    """
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
    """
    Update an document to match the supplied dictionary.
    :param doc:
    :param data:
    :return:
    """

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
        if key in doc._fields:
            value = field_value(doc._fields[key], value)
        setattr(doc, key, value)


class Config(DynamicDocument):
    code = StringField(primary_key=True)
    pass


class TagGroup(DynamicDocument):
    code = StringField(primary_key=True)
    pass


class Tag(DynamicDocument):
    code = StringField(primary_key=True)
    pass


class Role(DynamicDocument):
    code = StringField(primary_key=True)
    pass


class Publish(DynamicDocument):
    code = StringField(primary_key=True)
    pass


class Video(DynamicDocument):
    code = StringField(primary_key=True)
    img = StringField()
    roles = ListField(ReferenceField(Role))  # for move roles
    # tags = ListField(ReferenceField(Tag))
    pass
