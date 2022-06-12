from pytest import fixture

from pc_spec.pc import PC


@fixture
def pc(pc_name):
    return PC(name=pc_name)


@fixture
def pc_name():
    return 'my gaming pc'


@fixture
def pc_with_cpu(pc, cpu, cpu_intel_spec):
    pc.add_component(category=cpu, spec=cpu_intel_spec)
    return pc


@fixture
def cpu():
    return 'cpu'


@fixture
def cpu_intel_name():
    return 'name', 'Intel i7 9700K'


@fixture
def cpu_intel_spec(cpu_intel_name):
    return {cpu_intel_name[0]: cpu_intel_name[1]}


@fixture
def cpu_intel_spec_with_freq(cpu_intel_name, cpu_freq):
    name_name, name_value = cpu_intel_name
    freq_name, freq_value = cpu_freq
    return {name_name: name_value, freq_name: freq_value}


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


def test_new_pc_has_name(pc, pc_name):
    assert pc.name == pc_name


def test_new_default_pc_has_no_components(pc):
    assert pc.components == {}


def test_new_custom_pc_has_components(pc_name, cpu, cpu_intel_spec):
    components = {cpu: cpu_intel_spec}
    pc = PC(name=pc_name, components=components)
    assert pc.components == components


def test_add_component_when_component_not_there_then_it_is_added(pc, cpu):
    spec = {}
    pc.add_component(category=cpu, spec=spec)
    assert pc.components == {cpu: spec}


def test_add_component_when_component_is_there_then_nothing_is_added(pc_with_cpu, cpu, cpu_intel_spec, cpu_amd_spec):
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
    pc.update_component(category=cpu, spec_param_name=freq_name, spec_param_value=freq_value)
    assert pc.components == {}


def test_update_component_when_param_not_there_then_it_is_added(pc_with_mobo, mobo):
    format_name = 'format'
    format_value = 'ATX'
    pc_with_mobo.update_component(category=mobo, spec_param_name=format_name, spec_param_value=format_value)
    assert pc_with_mobo.components == {mobo: {format_name: format_value}}


def test_update_component_when_param_is_there_then_it_is_updated(pc_with_cpu, cpu, cpu_intel_name, cpu_freq):
    name_name, name_value = cpu_intel_name
    freq_name, _ = cpu_freq
    freq_value = '5.0 GHz'
    pc_with_cpu.update_component(category=cpu, spec_param_name=freq_name, spec_param_value=freq_value)
    assert pc_with_cpu.components == {cpu: {name_name: name_value, freq_name: freq_value}}


def test_remove_spec_param_when_component_not_there_then_nothing_is_removed(pc, cpu, cpu_freq):
    freq_name, _ = cpu_freq
    pc.remove_spec_param(category=cpu, spec_param_name=freq_name)
    assert pc.components == {}


def test_remove_spec_param_when_param_not_there_then_nothing_is_removed(pc_with_cpu, cpu, cpu_intel_spec, cpu_freq):
    freq_name, _ = cpu_freq
    pc_with_cpu.remove_spec_param(category=cpu, spec_param_name=freq_name)
    assert pc_with_cpu.components == {cpu: cpu_intel_spec}


def test_remove_spec_param_when_param_is_there_then_it_is_removed(pc_with_cpu, cpu, cpu_intel_name):
    name_name, _ = cpu_intel_name
    pc_with_cpu.remove_spec_param(category=cpu, spec_param_name=name_name)
    assert pc_with_cpu.components == {cpu: {}}


def test_has_component_when_component_is_there_then_true_is_returned(pc_with_cpu, cpu):
    assert pc_with_cpu.has_component(category=cpu) is True
    assert pc_with_cpu.has_component(category=cpu.upper()) is True


def test_has_component_when_component_is_not_there_then_false_is_returned(pc, cpu):
    assert pc.has_component(category=cpu) is False
    assert pc.has_component(category=cpu.upper()) is False


def test_has_spec_param_when_spec_param_is_there_then_true_is_returned(pc_with_cpu, cpu):
    assert pc_with_cpu.has_spec_param(category=cpu, spec_param_name='name') is True
    assert pc_with_cpu.has_spec_param(category=cpu, spec_param_name='NAME') is True


def test_has_spec_param_when_spec_param_is_not_there_then_false_is_returned(pc_with_cpu, cpu):
    assert pc_with_cpu.has_spec_param(category=cpu, spec_param_name='frequency') is False
    assert pc_with_cpu.has_spec_param(category=cpu, spec_param_name='FREQUENCY') is False


def test_has_spec_param_when_category_is_not_there_then_false_is_returned(pc, cpu):
    assert pc.has_spec_param(category=cpu, spec_param_name='frequency') is False
    assert pc.has_spec_param(category=cpu.upper(), spec_param_name='frequency') is False
