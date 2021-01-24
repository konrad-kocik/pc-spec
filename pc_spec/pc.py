class PC:
    def __init__(self):
        self.__components = {}

    @property
    def components(self):
        return self.__components

    def add_component(self, name, spec):
        if not self.__components.get(name):
            self.__components[name] = spec

    def remove_component(self, name):
        if self.__components.get(name):
            del self.__components[name]
