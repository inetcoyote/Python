from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class MergeApp(App):
    def build(self):
        self.title = "Объединение текста"

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Поля ввода
        self.entry1 = TextInput(hint_text="Поле 1", multiline=False, size_hint_y=None, height=50)
        self.entry2 = TextInput(hint_text="Поле 2", multiline=False, size_hint_y=None, height=50)
        self.entry3 = TextInput(hint_text="Результат", readonly=True, multiline=False, size_hint_y=None, height=50)

        # Кнопка
        button = Button(text="Объединить", size_hint_y=None, height=60)
        button.bind(on_press=self.combine_texts)

        # Добавляем в интерфейс
        layout.add_widget(Label(text="Введите текст:", size_hint_y=None, height=30))
        layout.add_widget(self.entry1)
        layout.add_widget(self.entry2)
        layout.add_widget(self.entry3)
        layout.add_widget(button)

        return layout

    def combine_texts(self, instance):
        text1 = self.entry1.text.strip()
        text2 = self.entry2.text.strip()
        combined = f"{text1} {text2}".strip()

        if not combined:
            self.show_popup("Предупреждение", "Оба поля пусты!")
        else:
            self.entry3.text = combined
            self.show_popup("Результат", f"Объединённый текст:\n{combined}")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.6)
        )
        popup.open()


MergeApp().run()