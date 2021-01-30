from pathlib import Path
from shutil import rmtree

from pytest import fixture

from pc_spec.data import save_store, load_store
from pc_spec.pc import PC
from pc_spec.store import Store


@fixture
def test_dir_path():
    return Path('test_data', 'test_files')


@fixture
def remove_test_dir(test_dir_path, request):
    def teardown():
        if test_dir_path.is_dir():
            rmtree(test_dir_path.parent)
    request.addfinalizer(teardown)


def test_pcs_management_in_store():
    store = Store()
    assert store.pcs == []

    new_pc = PC(name='gaming rig')
    assert new_pc.name == 'gaming rig'
    assert new_pc.components == {}

    store.add_pc(pc=new_pc)
    assert store.pcs == [new_pc]

    pc = store.get_pc('gaming rig')
    assert pc == new_pc

    pc.add_component(category='mobo')
    assert pc.components == {'mobo': {}}

    pc.add_component(category='cpu', spec={'name': 'Intel i7 9700K'})
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'Intel i7 9700K'}}

    pc.add_component(category='cpu', spec={'name': 'AMD Ryzen 5 5900X'})
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'Intel i7 9700K'}}

    pc.add_component(category='gpu', spec={'name': 'Nvidia RTX 3070'})
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'Intel i7 9700K'},
                             'gpu': {'name': 'Nvidia RTX 3070'}}

    pc.remove_component(category='gpu')
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'Intel i7 9700K'}}

    pc.remove_component(category='ram')
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'Intel i7 9700K'}}

    pc.swap_component(category='cpu', spec={'name': 'AMD Ryzen 5 5900X'})
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'}}

    pc.swap_component(category='ram')
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'}}

    pc.add_component(category='gpu', spec={'name': 'Nvidia RTX 3070'})
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'},
                             'gpu': {'name': 'Nvidia RTX 3070'}}

    pc.swap_component(category='gpu')
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'},
                             'gpu': {}}

    pc.update_component(category='ram', param_name='frequency', param_value='3200 MHz')
    assert pc.components == {'mobo': {},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'},
                             'gpu': {}}

    pc.update_component(category='mobo', param_name='name', param_value='ASRock Z390 EXTREME4')
    assert pc.components == {'mobo': {'name': 'ASRock Z390 EXTREME4'},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'},
                             'gpu': {}}

    pc.update_component(category='mobo', param_name='format', param_value='ITX')
    assert pc.components == {'mobo': {'name': 'ASRock Z390 EXTREME4', 'format': 'ITX'},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'},
                             'gpu': {}}

    pc.update_component(category='mobo', param_name='format', param_value='ATX')
    assert pc.components == {'mobo': {'name': 'ASRock Z390 EXTREME4', 'format': 'ATX'},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'},
                             'gpu': {}}

    pc.remove_component(category='gpu')
    assert pc.components == {'mobo': {'name': 'ASRock Z390 EXTREME4', 'format': 'ATX'},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'}}

    store.add_pc(PC(name='gaming rig'))
    assert store.pcs == [pc]

    new_pc = PC(name='workstation')
    store.add_pc(pc=new_pc)
    assert store.pcs == [pc, new_pc]

    not_existing_pc = store.get_pc(name='xbox')
    assert not_existing_pc is None

    store.remove_pc(name='xbox')
    assert store.pcs == [pc, new_pc]

    store.remove_pc(name='workstation')
    assert store.pcs == [pc]

    pc = store.get_pc(name='gaming rig')
    assert pc.components == {'mobo': {'name': 'ASRock Z390 EXTREME4', 'format': 'ATX'},
                             'cpu': {'name': 'AMD Ryzen 5 5900X'}}


def test_saving_and_loading_store(test_dir_path, remove_test_dir):
    store = Store(pcs=[PC(name='gaming rig',
                          components={'cpu': {'name': 'i7-9700K'},
                                      'gpu': {'name': 'RTX 3070'}}),
                       PC(name='workstation',
                          components={'mobo': {'name': 'ASRock Z390 EXTREME4',
                                               'format': 'ATX'}})])

    save_store(store=store, target_dir=test_dir_path)
    loaded_store = load_store(source_dir=test_dir_path)

    assert len(loaded_store.pcs) == len(store.pcs)

    for pc_id, loaded_pc in enumerate(loaded_store.pcs):
        assert loaded_pc.name == store.pcs[pc_id].name
        assert loaded_pc.components == store.pcs[pc_id].components
