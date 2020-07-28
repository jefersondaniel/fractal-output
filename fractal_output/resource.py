import json


class Resource(object):
    def __init__(self, data, transformer):
        self.data = data
        self.transformer = transformer


class Item(Resource):
    def apply_transformer(self, selected_includes=None, include_stack=None):
        if not self.data:
            return Result(None)

        if not include_stack:
            include_stack = []

        result = self.transformer.transform(self.data)

        for include in self.transformer.default_includes:
            self.process_include(result, include, selected_includes, include_stack)

        for include in self.transformer.available_includes:
            include_full_path = '.'.join(include_stack + [include])
            if not selected_includes or include_full_path not in selected_includes:
                continue
            self.process_include(result, include, selected_includes, include_stack)

        return Result(result)

    def process_include(self, result, include, selected_includes, include_stack):
        method_name = 'include_{}'.format(include)
        if not hasattr(self.transformer, method_name):
            raise ResourceException('Transformer must contain method: {}'.format(method_name))
        method_instance = getattr(self.transformer, method_name)
        include_result = method_instance(self.data).apply_transformer(selected_includes, include_stack + [include])
        result[include] = include_result.get_data()


class Collection(Resource):
    def apply_transformer(self, selected_includes=None, include_stack=None):
        if not self.data:
            return Result([])

        result = []

        for value in self.data:
            item = Item(value, self.transformer)
            result.append(item.apply_transformer(selected_includes, include_stack).get_data())

        return Result(result)


class Null(Resource):
    def __init__(self):
        super(Null, self).__init__(None, None)

    def apply_transformer(self, selected_includes=None, include_stack=None):
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
