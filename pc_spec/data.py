from json import dump, load, JSONDecodeError
from pathlib import Path
from typing import List, Dict, Tuple

from pc_spec.pc import PC, Components
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


def backup_store(source_dir: Path, target_dir: Path):
    """
    Creates backup copy of original store JSON file.
    If original store JSON file doesn't exist then backup copy is not created.
    If backup copy already exists then 3 files will be created:
        - original file (store.json)
        - new backup file (store.bak.json) with content from original file
        - second backup file (store.bak2.json) with content from old backup file
    :param source_dir: path to directory which contains store JSON file
    :param target_dir: path to directory where backup JSON file(s) will be created
    """
    file_path = Path(source_dir, __get_store_file_name())

    if file_path.is_file():
        backup_file_path = Path(target_dir, __get_store_backup_file_name())

        if backup_file_path.is_file():
            second_backup_file_path = Path(target_dir, __get_store_second_backup_file_name())
            second_backup_file_path.write_text(backup_file_path.read_text())

        backup_file_path.write_text(file_path.read_text())


def __get_store_file_name() -> str:
    return 'store.json'


def __get_store_backup_file_name() -> str:
    return 'store.bak.json'


def __get_store_second_backup_file_name() -> str:
    return 'store.bak2.json'


def __create_dir_if_necessary(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True)


def __to_serializable_pcs(pcs: List[PC]) -> List[Dict[str, Components]]:
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


def __unpack_serialized_pc(serialized_pc: Dict[str, Components]) -> Tuple[str, Components]:
    name = list(serialized_pc.keys())[0]
    components = list(serialized_pc.values())[0]
    return name, components
