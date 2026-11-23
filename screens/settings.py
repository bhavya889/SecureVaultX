from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from ui.components import TactileButton, VaultLabel


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(18))
        self.add_widget(layout)
        layout.add_widget(VaultLabel(
            text="SETTINGS", size=28, color="METALLIC_SILVER",
            size_hint_y=None, height=dp(55),
        ))
        layout.add_widget(VaultLabel(
            text="Your vault is encrypted locally. Lock it whenever you leave the app.",
            size=14, color="TEXT_MUTED",
        ))
        lock = TactileButton(
            text="LOCK VAULT NOW", color="ACCENT_RED",
            size_hint_y=None, height=dp(56),
        )
        lock.bind(on_release=lambda *_: App.get_running_app().go_to_login())
        layout.add_widget(lock)
        back = TactileButton(
            text="BACK TO NOTES", color="CHARCOAL",
            size_hint_y=None, height=dp(50),
        )
        back.bind(on_release=lambda *_: App.get_running_app().go_home())
        layout.add_widget(back)
