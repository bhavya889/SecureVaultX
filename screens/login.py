import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from core.encryption import CryptoEngine, DecryptionError
from ui.components import RecessedInput, TactileButton, VaultLabel


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(18))
        self.add_widget(layout)
        layout.add_widget(VaultLabel(
            text="VAULT LOCKED", size=28, color="ACCENT_RED",
            size_hint_y=None, height=dp(60),
        ))
        self.pw_input = RecessedInput(
            hint_text="Master Password", password=True,
            size_hint_y=None, height=dp(52),
        )
        layout.add_widget(self.pw_input)
        self.btn = TactileButton(text="UNLOCK", size_hint_y=None, height=dp(56))
        self.btn.bind(on_release=self.attempt_unlock)
        layout.add_widget(self.btn)
        recovery = TactileButton(
            text="USE RECOVERY KEY", color="CHARCOAL",
            size_hint_y=None, height=dp(50),
        )
        recovery.bind(on_release=self.show_recovery)
        layout.add_widget(recovery)

    def attempt_unlock(self, *_):
        secret = self.pw_input.text
        if not secret:
            return
        self._start_unlock(secret)

    def show_recovery(self, *_):
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        field = RecessedInput(
            hint_text="Paste recovery key", password=True,
            multiline=False, size_hint_y=None, height=dp(52),
        )
        content.add_widget(field)
        unlock = TactileButton(text="RECOVER VAULT", size_hint_y=None, height=dp(50))
        content.add_widget(unlock)
        popup = Popup(title="Recovery", content=content, size_hint=(0.9, 0.34))
        unlock.bind(on_release=lambda *_: (popup.dismiss(), self._start_unlock(field.text, recovery=True)))
        popup.open()

    def _start_unlock(self, secret, recovery=False):
        self.btn.disabled = True
        self.btn.text = "DECRYPTING..."
        threading.Thread(
            target=self._verify, args=(secret, recovery), daemon=True,
        ).start()

    def _verify(self, secret, recovery):
        try:
            auth = App.get_running_app().db.get_auth()
            if not auth:
                raise DecryptionError("Vault setup is incomplete.")
            salt_name = "recovery_salt" if recovery else "master_salt"
            wrapped_name = "recovery_wrapped_dek" if recovery else "wrapped_dek"
            dek = CryptoEngine.unwrap_dek(auth[wrapped_name], secret, auth[salt_name])
            Clock.schedule_once(lambda dt: self._success(dek), 0)
        except Exception:
            Clock.schedule_once(lambda dt: self._fail(), 0)

    def _success(self, dek):
        self.pw_input.text = ""
        self.btn.text = "UNLOCK"
        self.btn.disabled = False
        App.get_running_app().dek = dek
        App.get_running_app().go_home()

    def _fail(self):
        self.pw_input.text = ""
        self.btn.text = "UNLOCK"
        self.btn.disabled = False
        Popup(
            title="Unlock failed",
            content=VaultLabel(text="Incorrect password/recovery key.", size=14),
            size_hint=(0.82, 0.3),
        ).open()
