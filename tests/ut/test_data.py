from json import load
from pathlib import Path
from shutil import rmtree
from unittest.mock import Mock

from pytest import fixture

from pc_spec.data import save_store


@fixture
def empty_store():
    store = Mock()
    store.pcs = []
    return store


@fixture
def store(empty_store):
    pc_1 = Mock()
    pc_1.name = 'pc_1'
    pc_1.components = {'cpu': {'name': 'i7-9700K'},
                       'gpu': {'name': 'RTX 3070'}}

    pc_2 = Mock()
    pc_2.name = 'pc_2'
    pc_2.components = {'mobo': {'name': 'ASRock Z390 EXTREME4',
                                'format': 'ATX'}}

    empty_store.pcs = [pc_1, pc_2]
    return empty_store


@fixture
def test_dir_path():
    return Path('test_data', 'test_files')


@fixture
def remove_test_dir(test_dir_path, request):
    def teardown():
        if test_dir_path.is_dir():
            rmtree(test_dir_path.parent)
    request.addfinalizer(teardown)


@fixture
def create_test_dir(test_dir_path):
    if not test_dir_path.is_dir():
        test_dir_path.mkdir(parents=True)


@fixture
def test_file_path(test_dir_path):
    return Path(test_dir_path, 'store.json')


def test_save_store_when_target_dir_is_not_there_then_it_is_created(
        empty_store, test_dir_path, test_file_path, remove_test_dir):
    save_store(store=empty_store, target_dir=test_dir_path)
    __assert_json_file_contains(content=empty_store.pcs, file_path=test_file_path)


def test_save_store_when_target_dir_is_there_then_it_is_used(
        empty_store, test_dir_path, test_file_path, create_test_dir, remove_test_dir):
    save_store(store=empty_store, target_dir=test_dir_path)
    __assert_json_file_contains(content=empty_store.pcs, file_path=test_file_path)


def test_save_store_when_store_not_empty_then_it_is_saved(
        store, test_dir_path, test_file_path, create_test_dir, remove_test_dir):
    content = [{store.pcs[0].name: store.pcs[0].components},
               {store.pcs[1].name: store.pcs[1].components}]
    save_store(store=store, target_dir=test_dir_path)
    __assert_json_file_contains(content=content, file_path=test_file_path)


def __assert_json_file_contains(content, file_path):
    assert file_path.is_file()

    with open(file_path, 'r') as json_file:
        assert load(json_file) == content
