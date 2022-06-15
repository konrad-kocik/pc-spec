from unittest.mock import Mock

from pytest import fixture

from pc_spec.store import Store


@fixture
def store():
    return Store()


@fixture
def pc_name():
    return 'workstation'


@fixture
def empty_pc_name():
    return 'gaming rig'


@fixture
def components():
    return Mock()


@fixture
def store_with_pc(store, pc_name, components):
    store.add_pc(name=pc_name, components=components)
    return store


@fixture
def store_with_pcs(store_with_pc, empty_pc_name):
    store_with_pc.add_pc(name=empty_pc_name)
    return store_with_pc


@fixture
def not_existing_pc_name():
    return 'not existing pc'


def test_new_default_store_has_no_pcs(store):
    assert store.pcs == []


def test_new_custom_store_has_pcs():
    pcs = [Mock(), Mock()]
    store = Store(pcs=pcs)
    assert store.pcs == pcs


def test_add_pc_when_pc_with_same_name_not_there_then_pc_is_added(store):
    pc_name = 'gaming rig'
    components = Mock()

    store.add_pc(name=pc_name, components=components)

    assert len(store.pcs) == 1
    assert store.pcs[0].name == pc_name
    assert store.pcs[0].components is components


def test_add_pc_when_pc_with_same_name_is_there_then_nothing_is_added(store_with_pc, pc_name):
    assert len(store_with_pc.pcs) == 1
    new_components = Mock()

    store_with_pc.add_pc(name=pc_name, components=new_components)

    assert len(store_with_pc.pcs) == 1
    assert store_with_pc.pcs[0].components is not new_components


def test_get_pc_when_pc_with_same_name_not_there_then_nothing_is_returned(store, not_existing_pc_name):
    assert store.get_pc(name=not_existing_pc_name) is None


def test_get_pc_when_pc_with_same_name_is_there_then_it_is_returned(store_with_pc, pc_name, components):
    pc = store_with_pc.get_pc(name=pc_name)

    assert pc.name == pc_name
    assert pc.components is components


def test_remove_pc_when_pc_with_same_name_not_there_then_nothing_is_removed(
        store_with_pc, pc_name, components, not_existing_pc_name):
    assert len(store_with_pc.pcs) == 1

    store_with_pc.remove_pc(name=not_existing_pc_name)

    assert len(store_with_pc.pcs) == 1
    assert store_with_pc.pcs[0].name == pc_name
    assert store_with_pc.pcs[0].components is components


def test_remove_pc_when_pc_with_same_name_is_there_then_it_is_removed(store_with_pc, pc_name):
    assert len(store_with_pc.pcs) == 1
    store_with_pc.remove_pc(name=pc_name)
    assert store_with_pc.pcs == []


def test_has_pc_when_pc_with_given_name_is_there_then_true_is_returned(store_with_pc, pc_name):
    assert store_with_pc.has_pc(name=pc_name) is True
    assert store_with_pc.has_pc(name=pc_name.upper()) is True


def test_has_pc_when_pc_with_given_name_is_not_there_then_false_is_returned(store_with_pc, not_existing_pc_name):
    assert store_with_pc.has_pc(name=not_existing_pc_name) is False
    assert store_with_pc.has_pc(name=not_existing_pc_name.upper()) is False


def test_move_pc_up_when_pc_with_same_name_not_there_then_nothing_is_moved(
        store_with_pcs, pc_name, empty_pc_name, not_existing_pc_name):
    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name

    store_with_pcs.move_pc_up(name=not_existing_pc_name)

    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name


def test_move_pc_up_when_pc_with_same_name_is_there_then_it_is_moved(store_with_pcs, pc_name, empty_pc_name):
    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name

    store_with_pcs.move_pc_up(name=empty_pc_name)

    assert store_with_pcs.pcs[0].name == empty_pc_name
    assert store_with_pcs.pcs[1].name == pc_name


def test_move_pc_up_when_pc_with_same_name_is_on_top_then_nothing_is_moved(store_with_pcs, pc_name, empty_pc_name):
    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name

    store_with_pcs.move_pc_up(name=pc_name)

    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name


def test_move_pc_down_when_pc_with_same_name_not_there_then_nothing_is_moved(
        store_with_pcs, pc_name, empty_pc_name, not_existing_pc_name):
    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name

    store_with_pcs.move_pc_down(name=not_existing_pc_name)

    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name


def test_move_pc_down_when_pc_with_same_name_is_there_then_it_is_moved(store_with_pcs, pc_name, empty_pc_name):
    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name

    store_with_pcs.move_pc_down(name=pc_name)

    assert store_with_pcs.pcs[0].name == empty_pc_name
    assert store_with_pcs.pcs[1].name == pc_name


def test_move_pc_down_when_pc_with_same_name_is_on_bottom_then_nothing_is_moved(store_with_pcs, pc_name, empty_pc_name):
    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name

    store_with_pcs.move_pc_down(name=empty_pc_name)

    assert store_with_pcs.pcs[0].name == pc_name
    assert store_with_pcs.pcs[1].name == empty_pc_name
