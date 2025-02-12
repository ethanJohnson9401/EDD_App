from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Create a GridLayout for the form
        form_layout = GridLayout(cols=2, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        form_layout.add_widget(Label(text='User   Name', size_hint_y=None, height=40))
        self.username = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.username)

        form_layout.add_widget(Label(text='Password', size_hint_y=None, height=40))
        self.password = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.password)

        # Add the form layout to the main layout
        self.add_widget(form_layout)

        # Add a submit button
        self.submit_button = Button(text='Login', size_hint_y=None, height=50)
        self.submit_button.bind(on_press=self.on_login)
        self.add_widget(self.submit_button)

    def on_login(self, instance):
        # Placeholder for login functionality
        username = self.username.text
        password = self.password.text
        print(f"Username: {username}, Password: {password}")


class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    # Set the window size (optional)
    Window.size = (400, 300)  # Width, Height
    Window.borderless = False  # Optional: Set to False to show window borders
    Window.size = (400, 300)  # Set the desired window size
    Window.resizable = False  # Lock the window size
    MyApp().run()