from unittest.mock import Mock

from pytest import fixture

from pc_spec.store import Store


@fixture
def store():
    return Store()


@fixture
def pc():
    pc = Mock()
    pc.name = 'workstation'
    return pc


@fixture
def store_with_pc(store, pc):
    store.add_pc(pc=pc)
    return store


@fixture
def not_existing_pc_name():
    return 'not existing pc'


def test_new_store_has_no_pcs(store):
    assert store.pcs == []


def test_add_pc_when_pc_with_same_name_not_there_then_pc_is_added(store, pc):
    store.add_pc(pc=pc)
    assert len(store.pcs) == 1
    assert pc in store.pcs


def test_add_pc_when_pc_with_same_name_is_there_then_nothing_is_added(store_with_pc, pc):
    new_pc = Mock()
    new_pc.name = pc.name
    store_with_pc.add_pc(pc=new_pc)
    assert len(store_with_pc.pcs) == 1
    assert new_pc not in store_with_pc.pcs


def test_get_pc_when_pc_with_same_name_not_there_then_nothing_is_returned(store, not_existing_pc_name):
    assert store.get_pc(name=not_existing_pc_name) is None


def test_get_pc_when_pc_with_same_name_is_there_then_it_is_returned(store_with_pc, pc):
    assert store_with_pc.get_pc(name=pc.name) == pc


def test_remove_pc_when_pc_with_same_name_not_there_then_nothing_is_removed(store_with_pc, pc, not_existing_pc_name):
    store_with_pc.remove_pc(name=not_existing_pc_name)
    assert len(store_with_pc.pcs) == 1
    assert pc in store_with_pc.pcs


def test_remove_pc_when_pc_with_same_name_is_there_then_it_is_removed(store_with_pc, pc):
    store_with_pc.remove_pc(name=pc.name)
    assert len(store_with_pc.pcs) == 0
    assert pc not in store_with_pc.pcs
