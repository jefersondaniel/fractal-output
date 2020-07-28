import json


class Resource(object):
    def __init__(self, data, transformer):
        self.data = data
        self.transformer = transformer


class Item(Resource):
    def apply_transformer(self):
        if not self.data:
            return Result(None)

        result = self.transformer.transform(self.data)

        for include in self.transformer.includes:
            method_name = 'include_{}'.format(include)
            if not hasattr(self.transformer, method_name):
                raise ResourceException('Transformer must contain method: {}'.format(method_name))
            method_instance = getattr(self.transformer, method_name)
            include_result = method_instance(self.data).apply_transformer()
            result[include] = include_result.get_data()

        return Result(result)


class Collection(Resource):
    def apply_transformer(self):
        if not self.data:
            return Result([])

        result = []

        for value in self.data:
            item = Item(value, self.transformer)
            result.append(item.apply_transformer().get_data())

        return Result(result)


class Null(Resource):
    def __init__(self):
        super(Null, self).__init__(None, None)

    def apply_transformer(self):
        return Result(None)


class Result(object):
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self.data)

    def get_data(self):
        return self.data


class ResourceException(Exception):
    pass
