# -*- coding: utf8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base
from ..utilities import Utility
from ..models.FormProperty import FormProperty
import datetime

import pprint


class Form(Base):
    __tablename__ = 'Form'

    pk_Form = Column(BigInteger, primary_key=True)

    name = Column(String(100, 'French_CI_AS'), nullable=False, unique=True)
    tag = Column(String(300, 'French_CI_AS'), nullable=True)
    creationDate = Column(DateTime, nullable=False)
    modificationDate = Column(DateTime, nullable=True)
    curStatus = Column(Integer, nullable=False)
    obsolete = Column(Boolean, nullable=False)
    isTemplate = Column(Boolean, nullable=False)
    context = Column(String(50, 'French_CI_AS'), nullable=False)
    originalID = Column(Integer, nullable=True)
    propagate = Column(Boolean, nullable=False)

    # Relationship
    fieldsets = relationship("Fieldset", cascade="all")
    inputs = relationship("Input", cascade="all")
    Properties = relationship("FormProperty", cascade="all")
    FormFile = relationship("FormFile", cascade="all")
    FormTrad = relationship("FormTrad", cascade="all")

    # Constructor
    def __init__(self, **kwargs):
        """
        Constructor
        :param kwargs:dict Dicth with initialized values
        :return:
        """
        self.name = kwargs['name']
        self.tag = kwargs['tag']
        self.creationDate = datetime.datetime.now()
        self.modificationDate = datetime.datetime.now()
        self.curStatus = "1"
        self.obsolete = kwargs['obsolete']
        self.isTemplate = kwargs['isTemplate']
        self.context = kwargs['context']
        self.propagate = kwargs['propagate']

    # Update form values
    def update(self, **kwargs):
        """
        Update form attributes with dict
        :param kwargs: dict
        :return:
        """
        self.name = kwargs['name']
        self.tag = kwargs['tag']
        self.modificationDate = datetime.datetime.now()
        self.isTemplate = kwargs['isTemplate']
        self.context = kwargs['context']
        self.propagate = kwargs['propagate']
        self.obsolete = kwargs['obsolete']

    def get_fieldsets(self):
        """
        Return all form fieldsets
        :return: form fieldsets as json
        """
        fieldsets = []
        for each in self.fieldsets:
            if each.curStatus != 4:
                fieldsets.append(each.toJSON())
        return fieldsets

    def get_formtrad(self):
        """
        Return all form fieldsets
        :return: form fieldsets as json
        """
        trads = []
        for each in self.FormTrad:
            trads.append(each.toJSON())
        return trads

    def to_json(self):
        """
        Return form as json without relationship
        :return: form as json without relationship
        """

        return {
            "id": self.pk_Form,
            "name": self.name,
            "tag": self.tag,
            "creationDate": "" if self.creationDate == 'NULL' or self.creationDate is None else self.creationDate.strftime("%d/%m/%Y - %H:%M:%S"),
            "modificationDate": "" if self.modificationDate == 'NULL' or self.modificationDate is None else self.modificationDate.strftime("%d/%m/%Y - %H:%M:%S"),
            "curStatus": self.curStatus,
            "obsolete": self.obsolete,
            "isTemplate": self.isTemplate,
            "context": self.context,
            "propagate": self.propagate,
            "originalID": self.originalID
        }

    # Serialize a form in JSON object
    def toJSON(self):
        json = self.to_json()
        json['translations'] = self.getTranslations()
        return json

    def addFormProperties(self, jsonobject):
        for prop in self.Properties:
            jsonobject[prop.name] = prop.getvalue()
        jsonobject['fileList'] = []
        for fileAssoc in self.FormFile:
            jsonobject['fileList'].append(fileAssoc.toJSON())
        return jsonobject

    def recuriseToJSON(self, withschema=True):
        json = self.toJSON()
        inputs = {}

        loops = 0
        allInputs = self.inputs

        for each in allInputs:
            inputs[loops] = each.toJSON()
            loops += 1

        if withschema:
            json['schema'] = inputs

        json['fieldsets'] = self.get_fieldsets()
        json['translations'] = self.getTranslations()

        json = self.addFormProperties(json)

        return json

    def hasCircularDependencies(self, allParents, session):
        toret = true
        for FormInput in self.inputs:
            if FormInput.type == 'ChildForm':
                childFormName = FormInput.getProperty('childFormName')
                if childFormName in allParents:
                    return true
                else:
                    tempAllParents = allParents
                    tempAllParents.append(self.name)
                    SubForm = session.query(Form).filter_by(
                        name=childFormName).first()
                    toret = toret and (SubForm is None or not SubForm.hasCircularDependencies(
                        tempAllParents, session))
        return (not toret)

    #get translations from FormTrad
    def getTranslations(self):
        translations = dict()
        allTrad = self.FormTrad
        for each in allTrad:
            translations[each.fk_Language] = each.toJSON()
        return translations 
    
    # Add Input to the form
    def addInput(self, newInput):
        self.inputs.append(newInput)

    # Add fieldset to the form
    def addFieldset(self, fieldset):
        self.fieldsets.append(fieldset)

    # Add FormFile to the form
    def addFile(self, newFile):
        self.FormFile.append(newFile)

    # return a list of all form's inputs id
    def getInputsIdList(self):
        inputsIdList = []
        for i in self.inputs:
            inputsIdList.append(i.pk_Input)
        return inputsIdList

    def addProperty(self, prop):
        self.Properties.append(prop)

    def updateProperties(self, properties):
        for prop in properties:
            if properties[prop] == None:
                properties[prop] = ''
            formProperty = FormProperty(
                prop, properties[prop], Utility._getType(properties[prop]))
            self.updateProperty(formProperty)

    def updateProperty(self, prop):
        for formprop in self.Properties:
            if formprop.name == prop.name:
                formprop.update(prop.name, prop.value,
                                prop.creationDate, prop.valueType)
                break

    @classmethod
    def getColumnList(cls):
        return [
            'name',
            'tag',
            'translations',
            'schema',
            'fieldsets',
            'obsolete',
            'isTemplate',
            'context',
            'propagate'
        ]
