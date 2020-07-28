Fractal Output
======================================

|Build Status| |Version| |Pyversions|

Provides a presentation and transformation layer for complex data output, the like found in RESTful APIs, and works really well with JSON. Think of this as a view layer for your JSON/YAML/etc. Based on https://fractal.thephpleague.com/

Documentation
~~~~~~~~~~~~~

Usage
^^^^^

Install:
''''''''

.. code:: bash

   $ pip install fractal_output

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: python

    from fractal_output import Manager, Transformer, Item

    class UserTransformer(Transformer):
        def transform(self, user):
            return {
                'id': user.id,
                'firstName': user.first_name
            }

    user = YourUserClass()
    transformer = UserTransformer()
    item = Item(user, transformer)

    manager = Manager()
    manager.create_data(item).to_json()

''''

.. |Build Status| image:: https://travis-ci.org/jefersondaniel/fractal-output.svg
   :target: https://travis-ci.org/jefersondaniel/fractal-output

.. |Version| image:: https://badge.fury.io/py/fractal_output.svg
   :target: https://pypi.python.org/pypi/fractal_output

.. |Pyversions| image:: https://img.shields.io/pypi/pyversions/fractal_output.svg
   :target: https://pypi.python.org/pypi/fractal_output
