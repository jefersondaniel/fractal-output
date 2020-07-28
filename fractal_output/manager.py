

class Manager(object):
    def create_data(self, item, selected_includes=None):
        return item.apply_transformer(
            selected_includes=selected_includes
        )
