from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World from Kivy!',
                     font_size=30,
                     size_hint=(0.5, 0.5),
                     pos_hint={'center_x': 0.5, 'center_y': 0.5})

if __name__ == '__main__':
    TestApp().run()