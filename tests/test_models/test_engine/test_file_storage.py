#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage, State, City
import os


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except BaseException:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_delete(self):
        """ New object is correctly added to __objects and delete"""
        new = BaseModel()
        new2 = BaseModel()
        self.assertTrue(len(storage.all().values()) == 2)
        storage.delete(new2)
        self.assertTrue(len(storage.all().values()) == 1)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        # print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_get_obj_by_id(self):
        """
        Tests the FileStorage.get() function to verify that it
        returns the expected object specified by id
        :return:
        """
        new = BaseModel()
        new2 = BaseModel()
        new.save()
        new2.save()
        storage.reload()
        b_model = storage.get(BaseModel, new.id)
        # Test should return None if ID not exist
        b_model_none_exist = storage.get(BaseModel, "Not Exists ID")
        b_model_c_id_none_exist = storage.get("Bogus", "Not Exists ID")
        # print(b_model.__dict__['id'])
        self.assertEqual(b_model.__dict__['id'], new.id)
        self.assertNotEqual(b_model.__dict__['id'], new2.id)
        self.assertNotEqual(b_model.__dict__['id'], new2.id)
        self.assertEqual(b_model_none_exist, None)
        self.assertEqual(b_model_c_id_none_exist, None)

    def test_count_objects(self):
        """ Tests the Number of objects in file storage as well as
        the number of class instances available
        """
        new = BaseModel()
        new2 = BaseModel()
        new3 = State()
        new4 = City()
        new.save()
        new3.save()
        new4.save()
        new2.save()
        storage.reload()
        all_models = storage.count()
        all_b_models = storage.count(BaseModel)
        self.assertEqual(all_models, 4)
        self.assertEqual(all_b_models, 2)


if __name__ == '__main__':
    suite_loader = unittest.TestLoader()
    test = test_fileStorage()
    suite1 = suite_loader.loadTestsFromTestCase(test)
    suite = unittest.TestSuite([suite1])
    unittest.TextTestRunner(verbosity=3).run(suite)
    # unittest.main(test_fileStorage,verbosity=5)
