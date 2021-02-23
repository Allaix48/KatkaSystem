from unittest import TestCase
from application.models import  User, UserEncoder
import  json

class TestUserSerialisation(TestCase):
    def test_serialize(self):
        usr = User(None,"test","pass",User.ROLE_USER)
        print(usr)
        usr_json = json.dumps(usr.serialize(), sort_keys=True)
        print(usr_json)
        self.assertEqual(usr_json,'{"id": null, "role": 1, "username": "test"}')

    def test_deserialize(self):
        usr_json = '{"id": null, "role": 1, "password":"pass" ,"username": "test"}'
        usr = User.init_json(usr_json)
        print(usr)
        self.assertEqual(usr, User(None,"test","pass",1))