

class Manager(object):
    async def create_data(self, item, selected_includes=None):
        return await item.apply_transformer(
            selected_includes=selected_includes
        )
