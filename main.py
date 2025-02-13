import asyncio
from bleak import BleakScanner
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock

# Load the KV file explicitly
Builder.load_file('connection.kv')

class DeviceButton(RecycleDataViewBehavior, Button):
    """ Custom button for each device in the RecycleView. """
    text = StringProperty()

    def on_press(self):
        # Handle device selection and connection logic here
        App.get_running_app().root.get_screen('connection').show_popup(f"Selected device: {self.text}")

class ConnectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def scan_for_devices(self):
        devices = await BleakScanner.discover(5.0, return_adv=True)
        device_names = [f"{d.name} ({d.address})" for d in devices if d.name]
        self.ids.device_list.data = [{'text': name} for name in device_names]  # Update the RecycleView data

    def show_popup(self, message):
        popup = Popup(title='Device Selected', content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ConnectionScreen(name='connection'))
        return sm

    def on_start(self):
        # Start scanning for devices when the app starts
        Clock.schedule_once(lambda dt: asyncio.run(self.scan_for_devices()), 1)

    async def scan_for_devices(self):
        devices = await BleakScanner.discover(5.0, return_adv=True)
        device_names = [f"{d.name} ({d.address})" for d in devices if d.name]
        self.root.get_screen('connection').ids.device_list.data = [{'text': name} for name in device_names]

if __name__ == '__main__':
    MyApp().run()