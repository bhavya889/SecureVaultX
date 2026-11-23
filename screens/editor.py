from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from core.notes_manager import NotesManager
from ui.components import RecessedInput, TactileButton, VaultLabel


class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(12))
        self.add_widget(layout)
        layout.add_widget(VaultLabel(
            text="NEW SECURE NOTE", size=24, color="METALLIC_SILVER",
            size_hint_y=None, height=dp(45),
        ))
        self.title_input = RecessedInput(
            hint_text="Note Title", multiline=False,
            size_hint_y=None, height=dp(52),
        )
        self.body_input = RecessedInput(
            hint_text="Write your private note...", multiline=True,
        )
        layout.add_widget(self.title_input)
        layout.add_widget(self.body_input)

        save = TactileButton(
            text="SAVE SECURELY", color="ACCENT_BLUE",
            size_hint_y=None, height=dp(54),
        )
        save.bind(on_release=self.save_note)
        layout.add_widget(save)
        cancel = TactileButton(
            text="CANCEL", color="CHARCOAL",
            size_hint_y=None, height=dp(48),
        )
        cancel.bind(on_release=lambda *_: App.get_running_app().go_home())
        layout.add_widget(cancel)

    def save_note(self, *_):
        title = self.title_input.text.strip()
        body = self.body_input.text.strip()
        if not title or not body:
            Popup(
                title="Missing content",
                content=VaultLabel(text="Enter both a title and note body.", size=14),
                size_hint=(0.82, 0.3),
            ).open()
            return
        app = App.get_running_app()
        NotesManager(app.db).create_note(app.dek, title, body)
        self.title_input.text = ""
        self.body_input.text = ""
        app.go_home()
