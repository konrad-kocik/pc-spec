from typing import List, Optional

from pc_spec.pc import PC


class Store:
    """ Represents collection of PCs. """

    def __init__(self):
        self.__pcs: List[PC] = []

    @property
    def pcs(self) -> List[PC]:
        """
        Gets all PCs from the store.
        :return: store's PCs
        """
        return self.__pcs

    def add_pc(self, pc: PC):
        """
        Adds new PC to the store.
        If PC with same name already exists then nothing will change.
        :param pc: PC to be added
        """
        if not self.__search_pc(pc.name):
            self.__pcs.append(pc)

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

    def __search_pc(self, name: str) -> Optional[PC]:
        for pc in self.__pcs:
            if pc.name == name:
                return pc
        return None
