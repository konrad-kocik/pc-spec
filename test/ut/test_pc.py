from pytest import fixture

from pc_spec.pc import PC


@fixture
def pc():
    return PC()


@fixture
def pc_with_cpu(pc, cpu, cpu_spec):
    pc.add_component(name=cpu, spec=cpu_spec)
    return pc


@fixture
def cpu():
    return 'cpu'


@fixture
def cpu_spec():
    return {'name': 'Intel i7 9700K'}


def test_new_pc_has_no_components(pc):
    assert pc.components == {}


def test_add_component_when_component_not_there_then_it_is_added(pc, cpu):
    spec = {}
    pc.add_component(name=cpu, spec=spec)
    assert pc.components == {cpu: spec}


def test_add_component_when_component_is_there_then_it_is_not_replaced(pc, cpu, cpu_spec):
    pc.add_component(name=cpu, spec=cpu_spec)
    pc.add_component(name=cpu, spec={'name': 'AMD Ryzen 5 5900X'})
    assert pc.components == {cpu: cpu_spec}


def test_remove_component_when_component_not_there_then_nothing_is_removed(pc_with_cpu, cpu, cpu_spec):
    pc_with_cpu.remove_component(name='ram')
    assert pc_with_cpu.components == {cpu: cpu_spec}


def test_remove_component_when_component_is_there_then_it_is_removed(pc_with_cpu, cpu):
    pc_with_cpu.remove_component(name=cpu)
    assert pc_with_cpu.components == {}
