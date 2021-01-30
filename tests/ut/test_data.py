from json import load, dump
from pathlib import Path
from shutil import rmtree
from unittest.mock import Mock

from pytest import fixture

from pc_spec.data import save_store, load_store


@fixture
def empty_store():
    store = Mock()
    store.pcs = []
    return store


@fixture
def store(pc_1_name, pc_1_components, pc_2_name, pc_2_components):
    pc_1 = Mock()
    pc_1.name = pc_1_name
    pc_1.components = pc_1_components

    pc_2 = Mock()
    pc_2.name = pc_2_name
    pc_2.components = pc_2_components

    store = Mock()
    store.pcs = [pc_1, pc_2]
    return store


@fixture
def pc_1_name():
    return 'pc_1'


@fixture
def pc_1_components():
    return {'cpu': {'name': 'i7-9700K'},
            'gpu': {'name': 'RTX 3070'}}


@fixture
def pc_2_name():
    return 'pc_2'


@fixture
def pc_2_components():
    return {'mobo': {'name': 'ASRock Z390 EXTREME4',
                     'format': 'ATX'}}


@fixture
def test_dir_path():
    return Path('test_data', 'test_files')


@fixture
def create_test_dir(test_dir_path):
    if not test_dir_path.is_dir():
        test_dir_path.mkdir(parents=True)


@fixture
def remove_test_dir(test_dir_path, request):
    def teardown():
        if test_dir_path.is_dir():
            rmtree(test_dir_path.parent)
    request.addfinalizer(teardown)


@fixture
def test_file_path(test_dir_path):
    return Path(test_dir_path, 'store.json')


@fixture
def create_empty_test_file(create_test_dir, test_file_path):
    if not test_file_path.is_file():
        test_file_path.touch()


@fixture
def create_test_file(test_file_path, create_empty_test_file, pc_1_name, pc_1_components, pc_2_name, pc_2_components):
    store = [{pc_1_name: pc_1_components},
             {pc_2_name: pc_2_components}]

    with open(test_file_path, 'w') as test_file:
        dump(store, test_file)


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


def test_save_store_when_saving_to_same_file_then_file_is_overridden(
        empty_store, store, test_dir_path, test_file_path, create_test_dir, remove_test_dir):
    save_store(store=store, target_dir=test_dir_path)
    save_store(store=empty_store, target_dir=test_dir_path)
    __assert_json_file_contains(content=empty_store.pcs, file_path=test_file_path)


def test_load_store_when_file_is_not_there_then_empty_store_is_loaded(test_dir_path):
    store = load_store(source_dir=test_dir_path)
    assert store.pcs == []


def test_load_store_when_empty_file_is_there_then_empty_store_is_loaded(
        test_dir_path, create_empty_test_file, remove_test_dir):
    store = load_store(source_dir=test_dir_path)
    assert store.pcs == []


def test_load_store_when_file_is_there_then_store_is_loaded(
        test_dir_path, create_test_file, pc_1_name, pc_1_components, pc_2_name, pc_2_components, remove_test_dir):
    store = load_store(source_dir=test_dir_path)
    assert len(store.pcs) == 2
    pc_1, pc_2 = store.pcs
    assert pc_1.name == pc_1_name
    assert pc_1.components == pc_1_components
    assert pc_2.name == pc_2_name
    assert pc_2.components == pc_2_components


def __assert_json_file_contains(content, file_path):
    assert file_path.is_file()

    with open(file_path, 'r') as json_file:
        assert load(json_file) == content
