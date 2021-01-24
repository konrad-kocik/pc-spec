class PC:
    def __init__(self):
        self.__components = {}

    @property
    def components(self):
        return self.__components

    def add_component(self, category, spec):
        if not self.__component_exists(category):
            self.__components[category] = spec

    def remove_component(self, category):
        if self.__component_exists(category):
            del self.__components[category]

    def swap_component(self, category, spec):
        if self.__component_exists(category):
            self.__components[category] = spec

    def update_component(self, category, param_name, param_value):
        if self.__component_exists(category):
            self.__components[category][param_name] = param_value

    def __component_exists(self, category):
        if self.__components.get(category):
            return True
        return False
