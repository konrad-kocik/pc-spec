from typing import List, Dict, Optional

from pc_spec.pc import PC

Spec = Dict[str, str]  # pragma: no mutate
Components = Dict[str, Spec]  # pragma: no mutate


class Store:
    """ Represents collection of PCs. """

    def __init__(self, pcs: Optional[List[PC]] = None):
        """
        :param pcs: collection of PCs which will be stored
        """
        self.__pcs: List[PC] = pcs if pcs else []

    @property
    def pcs(self) -> List[PC]:
        """
        Gets all PCs from the store.
        :return: store's PCs
        """
        return self.__pcs

    def add_pc(self, name: str, components: Optional[Components] = None):
        """
        Adds new PC to the store.
        If PC with same name already exists then nothing will change.
        :param name: name of PC to be added
        :param components: component parts of PC to be added
        """
        if not self.__search_pc(name):
            self.__pcs.append(PC(name=name, components=components))

    def get_pc(self, name: str) -> Optional[PC]:
        """
        Gets PC from the store.
        If PC with given name doesn't exist then nothing is returned.
        :param name: name of PC to be searched
        :return: PC with given name, None if not found
        """
        return self.__search_pc(name)

    def remove_pc(self, name: str):
        """
        Removes PC from the store.
        If PC with given name doesn't exist then nothing will change.
        :param name: name of PC to be removed
        """
        if pc := self.__search_pc(name):
            self.__pcs.remove(pc)

    def has_pc(self, name: str) -> bool:
        """
        Checks whether PC with given name exists.
        Is case-insensitive (i.e. 'my pc' == 'My PC').
        :param name: name of PC to be searched
        :return: True if PC with given name exists, False otherwise
        """
        return bool(self.__search_pc(name))

    def __search_pc(self, name: str) -> Optional[PC]:
        for pc in self.__pcs:
            if pc.name.lower() == name.lower():
                return pc
        return None
