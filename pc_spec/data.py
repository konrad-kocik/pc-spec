from json import dump, load, JSONDecodeError
from pathlib import Path
from typing import List, Dict, Tuple

from pc_spec.pc import PC
from pc_spec.store import Store


def save_store(store: Store, target_dir: Path):
    """
    Saves given store to JSON file created in given directory.
    If given directory doesn't exist then it is created (together with all missing parent directories).
    :param store: collection of PCs to be saved
    :param target_dir: path to directory where JSON file will be created
    """
    file_path = Path(target_dir, __get_store_file_name())
    __create_dir_if_necessary(target_dir)
    serializable_pcs = __to_serializable_pcs(store.pcs)
    __save_to_json(serializable_pcs, file_path)


def load_store(source_dir: Path) -> Store:
    """
    Loads store from JSON file saved in given directory.
    If given directory doesn't exist then empty store is loaded.
    If JSON file in given directory doesn't exist or is empty then empty store is loaded.
    :param source_dir: path to directory which contains store JSON file
    :return: loaded store
    """
    file_path = Path(source_dir, __get_store_file_name())
    return Store(__get_pcs_from_json_file(file_path)) if file_path.is_file() else Store()


def __get_store_file_name():
    return 'store.json'


def __create_dir_if_necessary(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True)


def __to_serializable_pcs(pcs: List[PC]) -> List[Dict[str, Dict[str, Dict[str, str]]]]:
    return [{pc.name: pc.components} for pc in pcs]


def __save_to_json(serializable: List, file_path: Path):
    with open(file_path, 'w') as json_file:
        dump(serializable, json_file)


def __get_pcs_from_json_file(file_path: Path) -> List[PC]:
    with open(file_path, 'r') as json_file:
        try:
            return[PC(*__unpack_serialized_pc(serialized_pc)) for serialized_pc in load(json_file)]
        except JSONDecodeError:
            return []


def __unpack_serialized_pc(serialized_pc: Dict[str, Dict[str, Dict[str, str]]]) -> \
        Tuple[str, Dict[str, Dict[str, str]]]:
    name = list(serialized_pc.keys())[0]
    components = list(serialized_pc.values())[0]
    return name, components
