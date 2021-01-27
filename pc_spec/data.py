from json import dump
from pathlib import Path
from typing import List, Dict

from pc_spec.pc import PC
from pc_spec.store import Store


def save_store(store: Store, target_dir: Path):
    """
    Saves given store to JSON file created in given directory.
    If given directory doesn't exist then it is created (together with all missing parent directories).
    :param store: collection of PCs to be saved
    :param target_dir: path to directory where JSON file will be created
    """
    file_path = Path(target_dir, 'store.json')
    __create_dir_if_necessary(target_dir)
    serializable_pcs = __to_serializable_pcs(store.pcs)
    __save_to_json(serializable_pcs, file_path)


def __create_dir_if_necessary(dir_path: Path):
    if not dir_path.is_dir():
        dir_path.mkdir(parents=True)


def __to_serializable_pcs(pcs: List[PC]) -> List[Dict[str, Dict[str, Dict[str, str]]]]:
    return [{pc.name: pc.components} for pc in pcs]


def __save_to_json(serializable: List, file_path: Path):
    with open(file_path, 'w') as json_file:
        dump(serializable, json_file)
