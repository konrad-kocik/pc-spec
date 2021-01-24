from pc_spec.pc import PC


def test_components_management():
    pc = PC()

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
