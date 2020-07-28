import pytest
from collections import namedtuple
from fractal_output import Manager, Transformer, Item, Collection, ResourceException


class TestTransformer(object):
    def test_transform_item(self):
        User = namedtuple('User', 'first_name')

        class UserTransformer(Transformer):
            def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        user = User('abigail')
        transformer = UserTransformer()
        item = Item(user, transformer)

        manager = Manager()
        result = manager.create_data(item).to_json()

        assert '{"firstName": "abigail"}' == result

    def test_transform_collection(self):
        User = namedtuple('User', 'first_name')

        class UserTransformer(Transformer):
            def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        users = [User('abigail'), User('mary')]
        transformer = UserTransformer()
        item = Collection(users, transformer)

        manager = Manager()
        result = manager.create_data(item).to_json()

        assert '[{"firstName": "abigail"}, {"firstName": "mary"}]' == result

    def test_transform_item_empty(self):
        class UserTransformer(Transformer):
            def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        transformer = UserTransformer()
        item = Item(None, transformer)

        manager = Manager()
        result = manager.create_data(item).get_data()

        assert not result

    def test_transform_collection_empty(self):
        class UserTransformer(Transformer):
            def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        transformer = UserTransformer()
        item = Collection(None, transformer)

        manager = Manager()
        result = manager.create_data(item).to_json()

        assert '[]' == result

    def test_transform_includes(self):
        User = namedtuple('User', 'first_name telephones address')
        Telephone = namedtuple('Telephone', 'number')
        Address = namedtuple('Address', 'street')

        class TelephoneTransformer(Transformer):
            def transform(self, telephone):
                return {
                    'number': telephone.number
                }

        class AddressTransformer(Transformer):
            def transform(self, address):
                return {
                    'street': address.street
                }

        class UserTransformer(Transformer):
            includes = [
                'telephones',
                'address',
                'subscription'
            ]

            def transform(self, user):
                return {
                    'firstName': user.first_name
                }

            def include_address(self, user):
                return self.item(user.address, AddressTransformer())

            def include_telephones(self, user):
                return self.collection(user.telephones, TelephoneTransformer())

            def include_subscription(self, user):
                return self.null()

        user = User(
            first_name='abigail',
            telephones=[Telephone('1')],
            address=Address('lala')
        )

        transformer = UserTransformer()
        item = Item(user, transformer)

        manager = Manager()
        result = manager.create_data(item).get_data()

        assert 'abigail' == result['firstName']
        assert '1' == result['telephones'][0]['number']
        assert 'lala' == result['address']['street']
        assert not result['subscription']

    def test_invalid_include(self):
        User = namedtuple('User', 'first_name address')
        Address = namedtuple('Address', 'street')

        class AddressTransformer(Transformer):
            def transform(self, address):
                return {
                    'street': address.street
                }

        class UserTransformer(Transformer):
            includes = [
                'lala'
            ]

            def transform(self, user):
                return {
                    'firstName': user.first_name
                }

            def include_address(self, user):
                return self.item(user.address, AddressTransformer())

        user = User(
            first_name='abigail',
            address=Address('lala')
        )

        transformer = UserTransformer()
        item = Item(user, transformer)
        manager = Manager()

        with pytest.raises(ResourceException):
            manager.create_data(item)
