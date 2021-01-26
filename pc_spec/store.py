from pc_spec.pc import PC


class Store:
    def __init__(self):
        self.__pcs = []

    @property
    def pcs(self):
        return self.__pcs

    def add_pc(self, pc: PC):
        if pc.name not in [pc.name for pc in self.__pcs]:
            self.__pcs.append(pc)

    def get_pc(self, name: str):
        for pc in self.__pcs:
            if pc.name == name:
                return pc

    def remove_pc(self, name: str):
        for pc in self.__pcs:
            if pc.name == name:
                self.__pcs.remove(pc)
                return
