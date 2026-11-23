from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from core.database import VaultDatabase
from screens.setup import SetupScreen
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.editor import EditorScreen
from screens.settings import SettingsScreen
from ui.theme import Theme


class SecureVaultApp(App):
    title = "SecureVaultX"

    def build(self):
        Window.clearcolor = Theme.get("BG_OBSIDIAN")
        self.dek = None
        self.db = VaultDatabase(self.user_data_dir)

        self.sm = ScreenManager(transition=FadeTransition(duration=0.2))
        self.sm.add_widget(SetupScreen(name="setup"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(EditorScreen(name="editor"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        self.sm.current = "setup" if self.db.get_auth() is None else "login"
        return self.sm

    def go_to_login(self):
        self.dek = None
        if self.sm:
            self.sm.current = "login"

    def go_home(self):
        if self.dek is not None:
            self.sm.current = "home"

    def go_editor(self):
        if self.dek is not None:
            self.sm.current = "editor"

    def go_settings(self):
        if self.dek is not None:
            self.sm.current = "settings"

    def on_pause(self):
        # Lock whenever Android backgrounds the app.
        self.go_to_login()
        return True

    def on_resume(self):
        if self.sm and self.sm.current not in ("setup", "login"):
            self.go_to_login()

    def on_stop(self):
        self.dek = None


if __name__ == "__main__":
    SecureVaultApp().run()
