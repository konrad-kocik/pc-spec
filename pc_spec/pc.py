from typing import Dict, Optional

Spec = Dict[str, str]  # pragma: no mutate
Components = Dict[str, Spec]  # pragma: no mutate


class PC:
    """ Represents computer build. """

    def __init__(self, name: str, components: Optional[Components] = None):
        """
        :param name: name of the PC, i.e. 'My gaming rig'
        :param components: component parts of the PC
        """
        self.__name: str = name
        self.__components: Components = components if components else {}

    @property
    def name(self) -> str:
        """
        Gets name of the PC.
        :return: PC's name
        """
        return self.__name

    @property
    def components(self) -> Components:
        """
        Gets component parts of the PC.
        :return: PC's components
        """
        return self.__components

    def add_component(self, category: str, spec: Optional[Spec] = None):
        """
        Adds new component to the PC.
        If component with given category already exists then nothing will change.
        :param category: type of component to be added, i.e. 'cpu'
        :param spec: specification of component to be added, i.e. {'name': 'i7-9700K', 'freq': '4 GHz'};
                     defaults to None (empty specification, results in empty dict)
        """
        if not self.__component_exists(category):
            self.__components[category] = spec if spec else {}

    def remove_component(self, category: str):
        """
        Removes component from the PC.
        If component with given category doesn't exist then nothing will change.
        :param category: type of component to be removed, i.e. 'cpu'
        """
        if self.__component_exists(category):
            del self.__components[category]

    def swap_component(self, category: str, spec: Optional[Spec] = None):
        """
        Replaces specification of component from given category with new one.
        If component with given category doesn't exist then nothing will change.
        :param category: type of component which specification will be swapped, i.e. 'cpu'
        :param spec: specification of component which will replace old one, i.e. {'name': 'i7-9700K', 'freq': '4 GHz'};
                     defaults to None (empty specification, results in empty dict)
        """
        if self.__component_exists(category):
            self.__components[category] = spec if spec else {}

    def update_component(self, category: str, spec_param_name: str, spec_param_value: str):
        """
        Updates specification of component from given category.
        If component with given category doesn't exist then nothing will change.
        If specification's parameter with given name doesn't exist then it will be added with given value.
        If specification's parameter with given name already exists then it's value will be updated with given one.
        :param category: type of component which specification will be updated, i.e. 'cpu'
        :param spec_param_name: name of specification's parameter which will be updated, i.e. 'freq'
        :param spec_param_value: value of specification's parameter which will replace old one, i.e. '4 GHz'
        """
        if self.__component_exists(category):
            self.__components[category][spec_param_name] = spec_param_value

    def move_component_up(self, category: str):
        """
        Moves component up in the PC.
        If component with given category doesn't exist then nothing will change.
        If component with given category is on the top then nothing will change.
        :param category: type of component to be moved up, i.e. 'cpu'
        """
        if self.__component_exists(category):
            component_id = list(self.__components.keys()).index(category)

            if component_id > 0:
                self.__move_component(category, component_id, shift=-1)

    def move_component_down(self, category: str):
        """
        Moves component down in the PC.
        If component with given category doesn't exist then nothing will change.
        If component with given category is on the bottom then nothing will change.
        :param category: type of component to be moved down, i.e. 'cpu'
        """
        if self.__component_exists(category):
            component_id = list(self.__components.keys()).index(category)

            if component_id < len(self.__components) - 1:
                self.__move_component(category, component_id, shift=1)

    def remove_spec_param(self, category: str, spec_param_name: str):
        """
        Removes given parameter from specification of component from given category.
        :param category: type of component from which specification's parameter will be removed, i.e. 'cpu'
        :param spec_param_name: name of specification's parameter which will be removed, i.e. 'freq'
        """
        if self.__spec_param_exist(category, spec_param_name):
            del self.__components[category][spec_param_name]

    def has_component(self, category: str) -> bool:
        """
        Checks whether component from given category exists.
        Is case-insensitive (i.e. 'cpu' == 'CPU').
        :param category: type of component to be checked, i.e. 'cpu'
        :return: True if component from given category exists, False otherwise
        """
        return self.__component_exists(category)

    def has_spec_param(self, category: str, spec_param_name: str) -> bool:
        """
        Checks whether specification of component from given category has parameter with given name.
        Is case-sensitive for category (i.e. 'cpu' != 'CPU').
        Is case-insensitive for specification's param name (i.e. 'frequency' == 'Frequency').
        :param category: type of component to be checked, i.e. 'cpu'
        :param spec_param_name: name of specification's parameter to be checked, i.e. 'frequency'
        :return: True if specification parameter exists, False otherwise
        """
        return self.__spec_param_exist(category, spec_param_name)

    def __component_exists(self, category: str) -> bool:
        categories = [category.lower() for category in self.__components.keys()]
        return category.lower() in categories

    def __move_component(self, moved_category, current_id, shift):
        new_id = current_id + shift
        moved_spec = self.__components[moved_category]
        reordered_components = {}

        for component_id, component in enumerate(self.__components.items()):
            component_category, component_spec = component

            if component_category != moved_category and shift > 0:
                reordered_components[component_category] = component_spec

            if component_id == new_id:
                reordered_components[moved_category] = moved_spec

            if component_category != moved_category and shift < 0:
                reordered_components[component_category] = component_spec

        self.__components = reordered_components

    def __spec_param_exist(self, category, spec_param_name):
        if not self.__component_exists(category):
            return False

        spec_param_names = [spec_param_name.lower() for spec_param_name in self.__components[category]]
        return spec_param_name.lower() in spec_param_names
