# -*- coding: utf8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base
import datetime


# Input Class
class Input(Base):

    __tablename__ = "Input"

    pk_Input      = Column(BigInteger, primary_key=True)

    fk_form       = Column(ForeignKey('Form.pk_Form'), nullable=False)

    name          = Column(String(100, 'French_CI_AS'), nullable=False)
    labelFr       = Column(String(300, 'French_CI_AS'), nullable=False)
    labelEn       = Column(String(300, 'French_CI_AS'), nullable=False)
    required      = Column(Boolean, nullable=False)
    readonly      = Column(Boolean, nullable=False)
    fieldSize     = Column(String(100, 'French_CI_AS'), nullable=False)
    endOfLine     = Column(Boolean, nullable=False)
    startDate     = Column(DateTime, nullable=False)
    curStatus     = Column(Integer, nullable=False)
    order         = Column(SmallInteger, nullable=True)
    type          = Column(String(100, 'French_CI_AS'), nullable=False)
    editorClass   = Column(String(100, 'French_CI_AS'), nullable=True)
    fieldClass    = Column(String(100, 'French_CI_AS'), nullable=True)
    
    # linked field section
    linkedFieldTable             = Column(String(100, 'French_CI_AS'), nullable=True)
    linkedFieldIdentifyingColumn = Column(String(100, 'French_CI_AS'), nullable=True)
    linkedField                  = Column(String(100, 'French_CI_AS'), nullable=True)
    formIdentifyingColumn        = Column(String(100, 'French_CI_AS'), nullable=True)

    Form        = relationship('Form')
    Properties  = relationship("InputProperty", cascade="all")

    # constructor
    def __init__(self, name, labelFr, labelEn, required, readonly, fieldSize, endOfLine, type, editorClass, fieldClass, linkedFieldTable, linkedFieldIdentifyingColumn, linkedField, formIdentifyingColumn, order):
        self.name        = name
        self.labelFr     = labelFr
        self.labelEn     = labelEn
        self.required    = required
        self.readonly    = readonly
        self.fieldSize   = fieldSize
        self.endOfLine   = endOfLine
        self.type        = type
        self.editorClass = editorClass
        self.fieldClass  = fieldClass
        self.linkedField = linkedField
        self.curStatus   = "1"
        self.order       = order

        # linked field
        self.linkedFieldTable             = linkedFieldTable
        self.linkedFieldIdentifyingColumn = linkedFieldIdentifyingColumn
        self.linkedField                  = linkedField
        self.formIdentifyingColumn        = formIdentifyingColumn

        self.startDate = datetime.datetime.now()

    # Update form values
    def update(self, **kwargs):
        self.name        = kwargs['name']
        self.labelFr     = kwargs['labelFr']
        self.labelEn     = kwargs['labelEn']
        self.required    = kwargs['required']
        self.readonly    = kwargs['readonly']
        self.fieldSize   = kwargs['fieldSize']
        self.endOfLine   = kwargs['endOfLine']
        self.editorClass = kwargs['editorClass']
        self.fieldClass  = kwargs['fieldClass']
        self.order       = kwargs['order']

        # linked field
        self.linkedFieldTable             = kwargs['linkedFieldTable']
        self.linkedFieldIdentifyingColumn = kwargs['linkedFieldIdentifyingColumn']
        self.linkedField                  = kwargs['linkedField']
        self.formIdentifyingColumn        = kwargs['formIdentifyingColumn']


    # Return convert object to JSON object
    def toJSON(self):
        JSONObject = {
            "id"          : self.pk_Input,
            "labelFr"     : self.labelFr,
            "labelEn"     : self.labelEn,
            "required"    : self.required,
            "endOfLine"   : self.endOfLine,
            "readonly"    : self.readonly,
            "fieldSize"   : self.fieldSize,
            "editorClass" : self.editorClass,
            "fieldClass"  : self.fieldClass,
            "type"        : self.type,
            "order"        : self.order,
            "name" : self.name,

            # linked field 

            "linkedFieldTable"             : self.linkedFieldTable,
            "linkedFieldIdentifyingColumn" : self.linkedFieldIdentifyingColumn,
            "linkedField"                  : self.linkedField,
            "formIdentifyingColumn"        : self.formIdentifyingColumn
        }
        return JSONObject

    # add property to the configurated input
    def addProperty(self, prop):
        self.Properties.append(prop)

    # get Column list except primary key and managed field like curStatus and startDate
    @classmethod
    def getColumnsList(cls):
        return [
            'name',
            'labelFr',
            'labelEn',
            'required',
            'readonly',
            'fieldSize',
            'endOfLine',
            'type',
            'editorClass',
            'fieldClass',
            'linkedFieldTable',
            'linkedFieldIdentifyingColumn',
            'linkedField',
            'formIdentifyingColumn',
            'order'
        ]