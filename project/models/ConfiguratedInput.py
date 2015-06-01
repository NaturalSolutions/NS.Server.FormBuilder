# -*- coding: utf8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base
import datetime


# Configurated input
# A configurated input cans have one or more property
class ConfiguratedInput(Base):

    __tablename__ = 'ConfiguratedInput'

    pk_ConfiguratedInput = Column(BigInteger, primary_key=True)

    name                 = Column(String(100, 'French_CI_AS'), nullable=False)
    labelFr              = Column(String(300, 'French_CI_AS'), nullable=False)
    labelEn              = Column(String(300, 'French_CI_AS'), nullable=False)
    required             = Column(Boolean, nullable=False)
    readonly             = Column(Boolean, nullable=False)
    fieldSize            = Column(String(100, 'French_CI_AS'), nullable=False)
    endOfLine            = Column(Boolean, nullable=False)
    startDate            = Column(DateTime, nullable=False)
    curStatus            = Column(Integer, nullable=False)

    type                 = Column(String(100, 'French_CI_AS'), nullable=False)
    editorClass          = Column(String(100, 'French_CI_AS'), nullable=True)
    fieldClass           = Column(String(100, 'French_CI_AS'), nullable=True)

    Properties           = relationship("ConfiguratedInputProperty", cascade="all")

    # constructor
    def __init__(self, name, labelFr, labelEn, required, readonly, fieldSize, endOfLine, type, editorClass, fieldClass):
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
        self.curStatus   = "1"

        self.startDate = datetime.datetime.now()

    # Return convert object to JSON object
    def toJSON(self):
        JSONObject = {
            "labelFr"     : self.labelFr,
            "labelEn"     : self.labelEn,
            "required"    : self.required,
            "endOfLine"   : self.endOfLine,
            "readonly"    : self.readonly,
            "fieldSize"   : self.fieldSize,
            "editorClass" : self.editorClass,
            "fieldClass"  : self.fieldClass,
            "type"        : self.type
        }

        for prop in self.Properties:
            JSONObject[prop.name] = prop.getvalue()

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
        ]