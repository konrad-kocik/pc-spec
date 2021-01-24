from pytest import fixture

from pc_spec.pc import PC


@fixture
def pc():
    return PC()


@fixture
def pc_with_cpu(pc, cpu, cpu_intel_spec):
    pc.add_component(category=cpu, spec=cpu_intel_spec)
    return pc


@fixture
def cpu():
    return 'cpu'


@fixture
def cpu_intel_spec():
    return {'name': 'Intel i7 9700K'}


@fixture
def cpu_intel_spec_with_freq(cpu_freq):
    freq_name, freq_value = cpu_freq
    return {'name': 'Intel i7 9700K', freq_name: freq_value}


@fixture
def cpu_freq():
    return 'frequency', '4.8 GHz'


@fixture
def cpu_amd_spec():
    return {'name': 'AMD Ryzen 5 5900X'}


@fixture
def pc_with_mobo(pc, mobo):
    pc.add_component(category=mobo, spec={})
    return pc


@fixture
def mobo():
    return 'mobo'


@fixture
def ram():
    return 'ram'


def test_new_pc_has_no_components(pc):
    assert pc.components == {}


def test_add_component_when_component_not_there_then_it_is_added(pc, cpu):
    spec = {}
    pc.add_component(category=cpu, spec=spec)
    assert pc.components == {cpu: spec}


def test_add_component_when_component_is_there_then_it_is_not_replaced(pc_with_cpu, cpu, cpu_intel_spec, cpu_amd_spec):
    pc_with_cpu.add_component(category=cpu, spec=cpu_amd_spec)
    assert pc_with_cpu.components == {cpu: cpu_intel_spec}


def test_add_component_with_default_spec(pc, cpu):
    pc.add_component(category=cpu)
    assert pc.components == {cpu: {}}


def test_remove_component_when_component_not_there_then_nothing_is_removed(pc_with_cpu, cpu, cpu_intel_spec, ram):
    pc_with_cpu.remove_component(category=ram)
    assert pc_with_cpu.components == {cpu: cpu_intel_spec}


def test_remove_component_when_component_is_there_then_it_is_removed(pc_with_cpu, cpu):
    pc_with_cpu.remove_component(category=cpu)
    assert pc_with_cpu.components == {}


def test_swap_component_when_component_not_there_then_nothing_is_swapped(pc_with_cpu, cpu, cpu_intel_spec, ram):
    pc_with_cpu.swap_component(category=ram, spec={})
    assert pc_with_cpu.components == {cpu: cpu_intel_spec}


def test_swap_component_when_component_is_there_then_it_is_swapped(pc_with_cpu, cpu, cpu_amd_spec):
    pc_with_cpu.swap_component(category=cpu, spec=cpu_amd_spec)
    assert pc_with_cpu.components == {cpu: cpu_amd_spec}


def test_swap_component_with_default_spec(pc_with_cpu, cpu):
    pc_with_cpu.swap_component(category=cpu)
    assert pc_with_cpu.components == {cpu: {}}


def test_update_component_when_component_not_there_then_nothing_is_updated(pc, cpu, cpu_freq):
    freq_name, freq_value = cpu_freq
    pc.update_component(category=cpu, param_name=freq_name, param_value=freq_value)
    assert pc.components == {}


def test_update_component_when_param_not_there_then_it_is_added(pc_with_mobo, mobo):
    format_name = 'format'
    format_value = 'ATX'
    pc_with_mobo.update_component(category=mobo, param_name=format_name, param_value=format_value)
    assert pc_with_mobo.components == {mobo: {format_name: format_value}}


def test_update_component_when_param_is_there_then_it_is_updated(pc_with_cpu, cpu, cpu_intel_spec_with_freq, cpu_freq):
    freq_name, _ = cpu_freq
    freq_value = '5.0 GHz'
    pc_with_cpu.update_component(category=cpu, param_name=freq_name, param_value=freq_value)
    assert pc_with_cpu.components == {cpu: {'name': 'Intel i7 9700K', freq_name: freq_value}}
