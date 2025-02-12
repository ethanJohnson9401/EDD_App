from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

# Load the kv file explicitly
Builder.load_file('login.kv')

class LoginScreen(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return LoginScreen()

    def on_login(self, username, password):
        # Placeholder for login functionality
        print(f"Username: {username}, Password: {password}")

if __name__ == '__main__':
    # Set the window size and lock it
    Window.size = (400, 300)  # Width, Height
    Window.resizable = False  # Lock the window size
    MyApp().run()