from pc_spec.pc import PC


class Store:
    """ Represents collection of computer builds. """

    def __init__(self):
        self.__pcs = []

    @property
    def pcs(self) -> list:
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
        if pc.name not in [pc.name for pc in self.__pcs]:
            self.__pcs.append(pc)

    def get_pc(self, name: str) -> PC:
        """
        Gets PC from the store.
        If PC with given name doesn't exist then nothing is returned.
        :param name: name of PC to be searched
        :return: PC with given name, None if not found
        """
        for pc in self.__pcs:
            if pc.name == name:
                return pc

    def remove_pc(self, name: str):
        """
        Removes PC from the store.
        If PC with given name doesn't exist then nothing will change.
        :param name: name of PC to be removed
        """
        for pc in self.__pcs:
            if pc.name == name:
                self.__pcs.remove(pc)
                return
