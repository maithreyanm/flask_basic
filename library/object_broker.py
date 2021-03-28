

class ObjectBroker:
    """
    The ObjectBroker is part of the standard project stack, It provides:
     - one-stop shopping for many common objects required throughout the project
     - post-startup object instantiation
     - client access to objects and service without regard to object management, like:
        1. class factoring
        2. singletons
        3. pooling
        4. object initiation
    - access to objects without having to import their modules (no circular references)
    """

    def __init__(self):
        self._ob_dict = {}

    def __setitem__(self, key, value):
        self._ob_dict[key] = value

    def __getitem__(self, key):
        return self._ob_dict[key]

    def __delitem__(self, key):
        self._ob_dict.pop(key)

    def pop(self, key):
        self.__delitem__(key)

    def get(self, key):
        return self._ob_dict.get(key)
        
    @property
    def flapp(self):  # Flask api
        return self['flapp']

    @property
    def config(self):
        return self['config']


ob = ObjectBroker()
