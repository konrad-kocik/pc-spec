from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

from pc_spec.data import load_store, save_store


class PCSpecApp(App):
    def __init__(self):
        super(PCSpecApp, self).__init__()

        Config.set('graphics', 'fullscreen', '0')
        Config.write()

        self.title = 'PC Spec'
        self._colors = {'pink': [120, 0, 255, 0.7],
                        'mint': [0, 255, 3, 0.7],
                        'black': [255, 255, 255, 1],
                        'red': [200, 0, 0, 1]}

        self._main_layout = None
        self._menu_layout = None
        self._buttons_layout = None
        self._pcs_layout = None
        self._components_layout = None
        self._spec_layout = None

        self._pcs_buttons = []
        self._add_pc_button = None
        self._components_buttons = []
        self._add_component_button = None
        self._spec_params_buttons = []
        self._add_spec_param_button = None

        self._selected_pc_button = None
        self._selected_component_button = None
        self._selected_spec_param_button = None

        self._store_path = Path(Path.home(), 'AppData', 'Local', 'PCSpec')
        self._store = load_store(source_dir=self._store_path)

        self._pc = None
        self._component_category = None
        self._component = None
        self._spec_param_name = None
        self._spec_param_value = None

    def build(self):
        self._create_layouts()
        # self._create_menu()
        self._create_pcs_buttons()
        return self._main_layout

    def _create_layouts(self):
        border_size = 3

        self._main_layout = BoxLayout(padding=0,
                                      orientation='vertical')

        self._menu_layout = BoxLayout(padding=border_size,
                                      orientation='horizontal',
                                      size_hint=(1, 0.15))
        self._main_layout.add_widget(self._menu_layout)

        self._buttons_layout = BoxLayout(padding=0,
                                         spacing=border_size,
                                         orientation='horizontal')
        self._main_layout.add_widget(self._buttons_layout)

        self._pcs_layout = BoxLayout(padding=0,
                                     spacing=border_size,
                                     orientation='vertical',
                                     size_hint=(0.5, 1))
        self._buttons_layout.add_widget(self._pcs_layout)

        self._components_layout = BoxLayout(padding=0,
                                            spacing=border_size,
                                            orientation='vertical',
                                            size_hint=(0.5, 1))
        self._buttons_layout.add_widget(self._components_layout)

        self._spec_layout = BoxLayout(padding=0,
                                      spacing=border_size,
                                      orientation='vertical')
        self._buttons_layout.add_widget(self._spec_layout)

    def _create_menu(self):
        image = Image(source=str(Path('pc_spec', 'app', 'rsc', 'logo.png')),
                      size_hint=(1, 1))
        self._menu_layout.add_widget(image)

    def _create_pcs_buttons(self):
        for pc in self._store.pcs:
            self._create_pc_button(pc_name=pc.name)

        self._add_pc_button = self._create_add_button(target_layout=self._pcs_layout,
                                                      on_press=self._add_empty_pc)

    def _create_pc_button(self, pc_name):
        pc_button = Button(text=pc_name.upper(),
                           background_color=self._colors['mint'],
                           color=self._colors['black'])
        pc_button.bind(on_press=self._select_pc)
        pc_button.pc_name = pc_name
        self._pcs_buttons.append(pc_button)
        self._pcs_layout.add_widget(pc_button)

    def _add_empty_pc(self, _):
        self._pcs_layout.remove_widget(self._add_pc_button)
        pc_text_input = TextInput(multiline=False)
        pc_text_input.background_color = self._colors['mint']
        pc_text_input.bind(on_text_validate=self._save_pc)
        self._pcs_layout.add_widget(pc_text_input)

    def _save_pc(self, pc_text_input):
        pc_name = pc_text_input.text

        if self._store.has_pc(name=pc_name):
            self._show_error(pc_text_input)
            return

        self._store.add_pc(name=pc_name)
        self._save_store()
        self._pcs_layout.remove_widget(pc_text_input)
        self._create_pc_button(pc_name=pc_name)
        self._pcs_layout.add_widget(self._add_pc_button)

    def _select_pc(self, selected):
        self._pc = self._store.get_pc(selected.pc_name)
        self._color_buttons(buttons=self._pcs_buttons, selected_button=selected)
        self._create_components_buttons()
        self._selected_pc_button = selected
        self._selected_component_button = None
        self._selected_spec_param_button = None
        self._create_remove_buttons()

    def _create_components_buttons(self):
        self._components_buttons.clear()
        self._components_layout.clear_widgets()

        self._spec_params_buttons.clear()
        self._spec_layout.clear_widgets()

        for component_category in self._pc.components:
            self._create_component_button(component_category)

        self._add_component_button = self._create_add_button(target_layout=self._components_layout,
                                                             on_press=self._add_empty_component)

    def _create_component_button(self, component_category):
        component_button = Button(text=component_category.upper(),
                                  background_color=self._colors['mint'],
                                  color=self._colors['black'])
        component_button.bind(on_press=self._select_component)
        component_button.component_category = component_category
        self._components_buttons.append(component_button)
        self._components_layout.add_widget(component_button)

    def _add_empty_component(self, _):
        self._components_layout.remove_widget(self._add_component_button)
        component_text_input = TextInput(multiline=False)
        component_text_input.background_color = self._colors['mint']
        component_text_input.bind(on_text_validate=self._save_component)
        self._components_layout.add_widget(component_text_input)

    def _save_component(self, component_text_input):
        component_category = component_text_input.text

        if self._pc.has_component(category=component_category):
            self._show_error(component_text_input)
            return

        self._pc.add_component(category=component_category)
        self._save_store()
        self._components_layout.remove_widget(component_text_input)
        self._create_component_button(component_category=component_category)
        self._components_layout.add_widget(self._add_component_button)

    def _select_component(self, selected):
        self._component_category = selected.component_category
        self._component = self._pc.components[selected.component_category]
        self._color_buttons(buttons=self._components_buttons, selected_button=selected)
        self._create_spec_params_buttons()
        self._selected_component_button = selected
        self._selected_spec_param_button = None
        self._create_remove_buttons()

    def _create_spec_params_buttons(self):
        self._spec_params_buttons.clear()
        self._spec_layout.clear_widgets()

        for spec_param_name, spec_param_value in self._component.items():
            self._create_spec_param_button(spec_param_name, spec_param_value)

        self._add_spec_param_button = self._create_add_button(target_layout=self._spec_layout,
                                                              on_press=self._add_empty_spec)

    def _create_spec_param_button(self, spec_param_name, spec_param_value):
        button_text = spec_param_value if spec_param_name.lower() == 'name' \
            else f'{spec_param_name.upper()}: {spec_param_value}'
        spec_param_button = Button(text=button_text,
                                   background_color=self._colors['mint'],
                                   color=self._colors['black'])
        spec_param_button.bind(on_press=self._select_spec_param)
        spec_param_button.spec_param_name = spec_param_name
        spec_param_button.spec_param_value = spec_param_value
        self._spec_params_buttons.append(spec_param_button)
        self._spec_layout.add_widget(spec_param_button)

    def _add_empty_spec(self, _):
        self._spec_layout.remove_widget(self._add_spec_param_button)
        spec_param_text_input = TextInput(multiline=False)
        spec_param_text_input.background_color = self._colors['mint']
        spec_param_text_input.bind(on_text_validate=self._save_spec_param)
        self._spec_layout.add_widget(spec_param_text_input)

    def _save_spec_param(self, spec_param_text_input):
        if ':' not in spec_param_text_input.text:
            self._show_error(spec_param_text_input)
            return

        spec_param_name, spec_param_value = spec_param_text_input.text.split(':')
        spec_param_name = spec_param_name.rstrip()
        spec_param_value = spec_param_value.lstrip()

        if self._pc.has_spec_param(category=self._component_category, spec_param_name=spec_param_name):
            self._show_error(spec_param_text_input)
            return

        self._pc.update_component(self._component_category, spec_param_name, spec_param_value)
        self._save_store()
        self._spec_layout.remove_widget(spec_param_text_input)
        self._create_spec_param_button(spec_param_name=spec_param_name, spec_param_value=spec_param_value)
        self._spec_layout.add_widget(self._add_spec_param_button)

    def _select_spec_param(self, selected):
        self._spec_param_name = selected.spec_param_name
        self._spec_param_value = selected.spec_param_value
        self._color_buttons(buttons=self._spec_params_buttons, selected_button=selected)
        self._selected_spec_param_button = selected
        self._create_remove_buttons()

    def _create_add_button(self, target_layout, on_press):
        add_button = Button(text='+',
                            background_color=self._colors['mint'],
                            color=self._colors['black'])
        add_button.bind(on_press=on_press)
        target_layout.add_widget(add_button)
        return add_button

    def _create_remove_buttons(self):
        self._menu_layout.clear_widgets()

        if self._selected_pc_button:
            self._create_remove_button(item_type='PC', on_press=self._remove_pc)

        if self._selected_component_button:
            self._create_remove_button(item_type='component', on_press=self._remove_component)

        if self._selected_spec_param_button:
            self._create_remove_button(item_type='spec param', on_press=self._remove_spec_param)

    def _create_remove_button(self, item_type, on_press):
        remove_button = Button(text=f'Remove {item_type}',
                               background_color=self._colors['mint'],
                               color=self._colors['black'])
        remove_button.bind(on_press=on_press)
        self._menu_layout.add_widget(remove_button)

    def _remove_pc(self, _):
        self._store.remove_pc(self._pc.name)
        self._save_store()

        self._pc = None
        self._component_category = None
        self._component = None
        self._spec_param_name = None
        self._spec_param_value = None

        self._pcs_layout.remove_widget(self._selected_pc_button)
        self._components_layout.clear_widgets()
        self._spec_layout.clear_widgets()

        self._selected_pc_button = None
        self._selected_component_button = None
        self._selected_spec_param_button = None
        self._create_remove_buttons()

    def _remove_component(self, _):
        self._pc.remove_component(self._component_category)
        self._save_store()

        self._component_category = None
        self._component = None
        self._spec_param_name = None
        self._spec_param_value = None

        self._components_layout.remove_widget(self._selected_component_button)
        self._spec_layout.clear_widgets()

        self._selected_component_button = None
        self._selected_spec_param_button = None
        self._create_remove_buttons()

    def _remove_spec_param(self, _):
        self._pc.remove_spec_param(self._component_category, self._spec_param_name)
        self._save_store()

        self._spec_param_name = None
        self._spec_param_value = None

        self._spec_layout.remove_widget(self._selected_spec_param_button)

        self._selected_spec_param_button = None
        self._create_remove_buttons()

    def _save_store(self):
        save_store(self._store, target_dir=self._store_path)

    def _color_buttons(self, buttons, selected_button):
        for button in buttons:
            button.background_color = self._colors['pink'] if button is selected_button else self._colors['mint']

    def _show_error(self, widget):
        widget.foreground_color = self._colors['red']
