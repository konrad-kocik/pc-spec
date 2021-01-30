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
        :param spec: component's specification which will replace old one, i.e. {'name': 'i7-9700K', 'freq': '4 GHz'};
                     defaults to None (empty specification, results in empty dict)
        """
        if self.__component_exists(category):
            self.__components[category] = spec if spec else {}

    def update_component(self, category: str, param_name: str, param_value: str):
        """
        Updates specification of component from given category.
        If component with given category doesn't exist then nothing will change.
        If specification's parameter with given name doesn't exist then it will be added with given value.
        If specification's parameter with given name already exists then it's value will be updated with given one.
        :param category: type of component which specification will be updated, i.e. 'cpu'
        :param param_name: name of specification's parameter which will be updated, i.e. 'freq'
        :param param_value: value of specification's parameter which will replace old one, i.e. '4 GHz'
        """
        if self.__component_exists(category):
            self.__components[category][param_name] = param_value

    def __component_exists(self, category: str) -> bool:
        return category in self.__components.keys()
