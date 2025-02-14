import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock

import asyncio
import platform

kivy.require("2.3.1")

if platform.system() == 'Linux' and 'microsoft' in platform.release():
    # Running on WSL
    from bleak import BleakScanner
elif platform.system() == 'Android':
    # Running on Android
    from jnius import autoclass
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
else:
    # Default to Bleak for other platforms
    from bleak import BleakScanner

class Theme:
    @staticmethod
    def hex_to_rgba(hex_color, alpha=1.0):
        """Converts a hex color code to an RGBA tuple."""
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255.0  # Normalize to [0, 1]
        g = int(hex_color[2:4], 16) / 255.0  # Normalize to [0, 1]
        b = int(hex_color[4:6], 16) / 255.0  # Normalize to [0, 1]
        return (r, g, b, alpha)

    PrimaryColor = hex_to_rgba("#FFFFFF")
    SecondaryColor = hex_to_rgba("#3B3B3B")
    TertiaryColor = hex_to_rgba("#009063")
    QuaternaryColor = hex_to_rgba("#E3E0F3")

# Load the KV file explicitly
Builder.load_file('connection.kv')

class ConnectionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device_list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.device_list_layout.bind(minimum_height=self.device_list_layout.setter('height'))
        self.add_widget(self.device_list_layout)

    def scan_for_devices(self):
        Clock.schedule_once(lambda dt: asyncio.run(self._scan_for_devices()))

    async def _scan_for_devices(self):
        """Scan for Bluetooth devices and update the layout."""
        try:
            print("Scanning for devices...")  # Debugging line
            if platform.system() == 'Android':
                adapter = BluetoothAdapter.getDefaultAdapter()
                if not adapter.isEnabled():
                    print("Bluetooth is not enabled.")
                    return
                paired_devices = adapter.getBondedDevices().toArray()
                devices = [(device.getName(), device.getAddress()) for device in paired_devices]
            else:
                scanner = BleakScanner()
                devices = await scanner.discover(5.0, return_adv=True)
                devices = [(d.name, d.address) for d in devices if d.name]

            self.device_list_layout.clear_widgets()  # Clear previous devices
            for name, address in devices:
                device_button = Button(text=f"{name} ({address})", size_hint_y=None, height='30dp')
                device_button.bind(on_press=lambda btn, device_name=name: self.show_popup(f"Selected device: {device_name}"))
                self.device_list_layout.add_widget(device_button)
        except Exception as e:
            print(f"Error scanning for devices: {e}")

    def show_popup(self, message):
        popup = Popup(title='Device Selected', content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class MyApp(App):
    def build(self):
        self.theme = Theme()  # Create an instance of the Theme class
        return ConnectionScreen()

if __name__ == '__main__':
    MyApp().run()