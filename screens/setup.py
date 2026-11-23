import os
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from core.encryption import CryptoEngine
from ui.components import RecessedInput, TactileButton, VaultLabel


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(18))
        self.add_widget(layout)
        layout.add_widget(VaultLabel(
            text="SECUREVAULTX", size=32, color="METALLIC_SILVER",
            size_hint_y=None, height=dp(60),
        ))
        layout.add_widget(VaultLabel(
            text="Create a master password to secure your private notes.",
            size=14, color="TEXT_MUTED",
        ))
        self.pw_input = RecessedInput(
            hint_text="Master Password", password=True,
            size_hint_y=None, height=dp(52),
        )
        self.pw_confirm = RecessedInput(
            hint_text="Confirm Master Password", password=True,
            size_hint_y=None, height=dp(52),
        )
        layout.add_widget(self.pw_input)
        layout.add_widget(self.pw_confirm)
        self.btn = TactileButton(
            text="INITIALIZE VAULT", size_hint_y=None, height=dp(56),
        )
        self.btn.bind(on_release=self.create_vault)
        layout.add_widget(self.btn)

    def create_vault(self, *_):
        password = self.pw_input.text
        if len(password) < 8 or password != self.pw_confirm.text:
            self._popup("Check your password", "Passwords must match and contain at least 8 characters.")
            return
        self.btn.disabled = True
        self.btn.text = "ENCRYPTING..."
        threading.Thread(target=self._process_setup, args=(password,), daemon=True).start()

    def _process_setup(self, password):
        try:
            dek = CryptoEngine.generate_dek()
            recovery_key = CryptoEngine.generate_recovery_key()
            master_salt = os.urandom(16)
            recovery_salt = os.urandom(16)
            wrapped = CryptoEngine.wrap_dek(dek, password, master_salt)
            recovery_wrapped = CryptoEngine.wrap_dek(dek, recovery_key, recovery_salt)
            App.get_running_app().db.save_auth(
                master_salt, wrapped, recovery_salt, recovery_wrapped,
            )
            Clock.schedule_once(lambda dt: self._finish_setup(recovery_key), 0)
        except Exception as exc:
            Clock.schedule_once(lambda dt: self._setup_failed(str(exc)), 0)

    def _finish_setup(self, recovery_key):
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        content.add_widget(VaultLabel(
            text="SAVE YOUR RECOVERY KEY", size=18, color="ACCENT_RED",
            size_hint_y=None, height=dp(35),
        ))
        content.add_widget(VaultLabel(
            text="This is the only way to recover your notes if you forget the master password. Store it somewhere safe.",
            size=13,
        ))
        key_box = RecessedInput(
            text=recovery_key, readonly=True, multiline=False,
            size_hint_y=None, height=dp(52),
        )
        content.add_widget(key_box)
        confirm = TactileButton(
            text="I HAVE SAVED IT", size_hint_y=None, height=dp(50),
        )
        content.add_widget(confirm)
        popup = Popup(
            title="Vault created", content=content,
            size_hint=(0.92, 0.48), auto_dismiss=False,
        )
        confirm.bind(on_release=lambda *_: (popup.dismiss(), App.get_running_app().go_to_login()))
        popup.open()
        self.pw_input.text = ""
        self.pw_confirm.text = ""
        self.btn.text = "INITIALIZE VAULT"
        self.btn.disabled = False

    def _setup_failed(self, message):
        self.btn.text = "INITIALIZE VAULT"
        self.btn.disabled = False
        self._popup("Setup failed", message)

    def _popup(self, title, message):
        Popup(
            title=title, content=VaultLabel(text=message, size=14),
            size_hint=(0.85, 0.32),
        ).open()
