from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.config import Config

from pc_spec.data import load_store


class PCSpecApp(App):
    def __init__(self):
        super(PCSpecApp, self).__init__()

        Config.set('graphics', 'fullscreen', '0')
        Config.write()

        self.title = 'PC Spec'
        self._colors = {'pink': [120, 0, 255, 0.7],
                        'mint': [0, 255, 3, 0.7],
                        'black': [255, 255, 255, 1]}

        self._main_layout = None
        self._buttons_layout = None
        self._pcs_layout = None
        self._components_layout = None
        self._specs_layout = None

        self._pcs_buttons = []
        self._components_buttons = []
        self._specs_buttons = []

        self._store = load_store(source_dir=Path('/home/bajit/repos/pc-spec/pc_spec/app/data'))
        self._pc = None
        self._component = None
        self._spec_name = None
        self._spec_value = None

    def build(self):
        self._create_layouts()
        self._create_menu()
        self._create_pcs_buttons()
        return self._main_layout

    def _create_layouts(self):
        border_size = 3

        self._main_layout = BoxLayout(padding=0,
                                      orientation='vertical')

        self._menu_layout = BoxLayout(padding=border_size,
                                      orientation='horizontal',
                                      size_hint=(0.04, 0.15))
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

        self._specs_layout = BoxLayout(padding=0,
                                       spacing=border_size,
                                       orientation='vertical')
        self._buttons_layout.add_widget(self._specs_layout)

    def _create_menu(self):
        image = Image(source='/home/bajit/repos/pc-spec/pc_spec/app/logo.png',
                      size_hint=(1, 1))
        self._menu_layout.add_widget(image)

    def _create_pcs_buttons(self):
        for pc in self._store.pcs:
            pc_button = Button(text=pc.name.upper(),
                               background_color=self._colors['mint'],
                               color=self._colors['black'])
            pc_button.bind(on_press=self._on_press_pc_button)
            pc_button.pc_name = pc.name
            self._pcs_buttons.append(pc_button)
            self._pcs_layout.add_widget(pc_button)

    def _on_press_pc_button(self, instance):
        self._pc = self._store.get_pc(instance.pc_name)
        self._color_buttons(buttons=self._pcs_buttons, pressed_button=instance)
        self._create_components_buttons()

    def _create_components_buttons(self):
        self._components_buttons.clear()
        self._components_layout.clear_widgets()

        self._specs_buttons.clear()
        self._specs_layout.clear_widgets()

        for component_name in self._pc.components:
            component_button = Button(text=component_name.upper(),
                                      background_color=self._colors['mint'],
                                      color=self._colors['black'])
            component_button.bind(on_press=self._on_press_component_button)
            component_button.component_name = component_name
            self._components_buttons.append(component_button)
            self._components_layout.add_widget(component_button)

    def _on_press_component_button(self, instance):
        self._component = self._pc.components[instance.component_name]
        self._color_buttons(buttons=self._components_buttons, pressed_button=instance)
        self._create_specs_buttons()

    def _create_specs_buttons(self):
        self._specs_buttons.clear()
        self._specs_layout.clear_widgets()

        for spec_name, spec_value in self._component.items():
            button_text = spec_value if spec_name.lower() == 'name' else f'{spec_name.upper()}: {spec_value}'
            spec_button = Button(text=button_text,
                                 background_color=self._colors['mint'],
                                 color=self._colors['black'])
            spec_button.bind(on_press=self._on_press_spec_button)
            spec_button.spec_name = spec_name
            spec_button.spec_value = spec_value
            self._specs_buttons.append(spec_button)
            self._specs_layout.add_widget(spec_button)

    def _on_press_spec_button(self, instance):
        self._spec_name = instance.spec_name
        self._spec_value = instance.spec_value
        self._color_buttons(buttons=self._specs_buttons, pressed_button=instance)

    def _color_buttons(self, buttons, pressed_button):
        for button in buttons:
            button.background_color = self._colors['pink'] if button is pressed_button else self._colors['mint']
