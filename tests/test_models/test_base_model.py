#!/usr/bin/python3
from models.base_model import BaseModel, Base
from datetime import datetime
import unittest
from uuid import UUID
import json
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'basemodel test not supported')
class test_basemodel(unittest.TestCase):
    """ test class for base_model class"""

    def __init__(self, *args, **kwargs):
        """ init the test class of basemodel"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ this is the  set up method of the test class"""
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
            self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        k = self.value()
        self.assertEqual(type(k), self.value)

    def test_kwargs(self):
        k = self.value()
        copy = k.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is k)

    def test_kwargs_int(self):
        k = self.value()
        copy = k.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Test the  save method"""
        k = self.value()
        k.save()
        key = self.name + "." + k.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ test the str method for  the model"""
        k = self.value()
        self.assertEqual(str(k), '[{}] ({}) {}'.format(self.name, k.id,
                         k.__dict__))

    def test_todict(self):
        k = self.value()
        n = k.to_dict()
        self.assertEqual(k.to_dict(), n)
        self.assertIsInstance(self.value().to_dict(), dict)
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        mdl = self.value()
        mdl.firstname = 'Celestine'
        mdl.lastname = 'Akpanoko'
        self.assertIn('firstname', mdl.to_dict())
        self.assertIn('lastname', mdl.to_dict())
        self.assertIn('firstname', self.value(firstname='Celestine').to_dict())
        self.assertIn('lastname', self.value(lastname='Akpanoko').to_dict())
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        datetime_now = datetime.today()
        mdl = self.value()
        mdl.id = '012345'
        mdl.created_at = mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': mdl.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(mdl.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='u-b34', age=13).to_dict(),
                {
                    '__class__': mdl.__class__.__name__,
                    'id': 'u-b34',
                    'age': 13
                }
            )
            self.assertDictEqual(
                self.value(id='u-b34', age=None).to_dict(),
                {
                    '__class__': mdl.__class__.__name__,
                    'id': 'u-b34',
                    'age': None
                }
            )
        # Tests to_dict output contradiction
        mdl_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(mdl_d.to_dict(), mdl_d.__dict__)
        self.assertNotEqual(
            mdl_d.to_dict()['__class__'],
            mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """ test kwargs again using  none"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ test the  kwargs with one argument"""
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """ test id attribute for  the model"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ test tje newly  created at attribute"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ test the  updated at attribute"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
