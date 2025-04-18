import pytest
from collections import namedtuple
from fractal_output import Manager, Transformer, Item, Collection, ResourceException


class TestTransformer(object):
    async def test_transform_item(self):
        User = namedtuple('User', 'first_name')

        class UserTransformer(Transformer):
            async def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        user = User('abigail')
        transformer = UserTransformer()
        item = Item(user, transformer)

        manager = Manager()
        result = await manager.create_data(item).to_json()

        assert '{"firstName": "abigail"}' == result

    async def test_transform_collection(self):
        User = namedtuple('User', 'first_name')

        class UserTransformer(Transformer):
            async def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        users = [User('abigail'), User('mary')]
        transformer = UserTransformer()
        item = Collection(users, transformer)

        manager = Manager()
        result = await manager.create_data(item).to_json()

        assert '[{"firstName": "abigail"}, {"firstName": "mary"}]' == result

    async def test_transform_item_empty(self):
        class UserTransformer(Transformer):
            async def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        transformer = UserTransformer()
        item = Item(None, transformer)

        manager = Manager()
        result = await manager.create_data(item).get_data()

        assert not result

    async def test_transform_collection_empty(self):
        class UserTransformer(Transformer):
            async def transform(self, user):
                return {
                    'firstName': user.first_name
                }

        transformer = UserTransformer()
        item = Collection(None, transformer)

        manager = Manager()
        result = await manager.create_data(item).to_json()

        assert '[]' == result

    async def test_transform_default_includes(self):
        User = namedtuple('User', 'first_name telephones address')
        Telephone = namedtuple('Telephone', 'number')
        Address = namedtuple('Address', 'street')

        class TelephoneTransformer(Transformer):
            async def transform(self, telephone):
                return {
                    'number': telephone.number
                }

        class AddressTransformer(Transformer):
            async def transform(self, address):
                return {
                    'street': address.street
                }

        class UserTransformer(Transformer):
            default_includes = [
                'telephones',
                'address',
                'subscription'
            ]

            async def transform(self, user):
                return {
                    'firstName': user.first_name
                }

            async def include_address(self, user):
                return self.item(user.address, AddressTransformer())

            async def include_telephones(self, user):
                return self.collection(user.telephones, TelephoneTransformer())

            async def include_subscription(self, user):
                return self.null()

        user = User(
            first_name='abigail',
            telephones=[Telephone('1')],
            address=Address('lala')
        )

        transformer = UserTransformer()
        item = Item(user, transformer)

        manager = Manager()
        result = await manager.create_data(item).get_data()

        assert 'abigail' == result['firstName']
        assert '1' == result['telephones'][0]['number']
        assert 'lala' == result['address']['street']
        assert not result['subscription']

    async def test_transform_available_includes(self):
        CategoryGroup = namedtuple('CategoryGroup', 'categories')
        Category = namedtuple('Category', 'name items')
        CategoryItem = namedtuple('Item', 'name')

        class CategoryGroupTransformer(Transformer):
            default_includes = ['categories']
            available_includes = ['lala', 'lele']

            async def transform(self, telephone):
                return {}

            async def include_categories(self, group):
                return self.collection(group.categories, CategoryTransformer())

            async def include_lala(self, group):
                return self.null()

            async def include_lele(self, group):
                return self.null()

        class CategoryTransformer(Transformer):
            available_includes = ['items']

            async def transform(self, category):
                return {
                    'name': category.name
                }

            async def include_items(self, category):
                return self.collection(category.items, CategoryItemTransformer())

        class CategoryItemTransformer(Transformer):
            async def transform(self, item):
                return {
                    'name': item.name
                }

        group = CategoryGroup([
            Category('a', [CategoryItem('book')])
        ])

        transformer = CategoryGroupTransformer()
        item = Item(group, transformer)

        manager = Manager()
        result_light = await manager.create_data(item, selected_includes=[]).get_data()
        result_heavy = await manager.create_data(item, selected_includes=['lala', 'categories.items']).get_data()

        assert 'lala' not in result_light
        assert 'lala' in result_heavy
        assert 'items' not in result_light['categories'][0]
        assert 'book' == result_heavy['categories'][0]['items'][0]['name']

    async def test_invalid_include(self):
        User = namedtuple('User', 'first_name address')
        Address = namedtuple('Address', 'street')

        class AddressTransformer(Transformer):
            async def transform(self, address):
                return {
                    'street': address.street
                }

        class UserTransformer(Transformer):
            default_includes = [
                'lala'
            ]

            async def transform(self, user):
                return {
                    'firstName': user.first_name
                }

            async def include_address(self, user):
                return self.item(user.address, AddressTransformer())

        user = User(
            first_name='abigail',
            address=Address('lala')
        )

        transformer = UserTransformer()
        item = Item(user, transformer)
        manager = Manager()

        with pytest.raises(ResourceException):
            await manager.create_data(item)
