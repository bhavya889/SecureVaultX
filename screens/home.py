from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from core.notes_manager import NotesManager
from ui.components import MetalPanel, TactileButton, VaultLabel


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(12))
        self.add_widget(self.layout)

        header = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        header.add_widget(VaultLabel(text="YOUR VAULT", size=24, color="METALLIC_SILVER"))
        settings = TactileButton(
            text="SETTINGS", color="CHARCOAL",
            size_hint=(None, 1), width=dp(105),
        )
        settings.bind(on_release=lambda *_: App.get_running_app().go_settings())
        header.add_widget(settings)
        self.layout.add_widget(header)

        self.btn_new = TactileButton(
            text="+ NEW NOTE", color="ACCENT_GREEN",
            size_hint_y=None, height=dp(54),
        )
        self.btn_new.bind(on_release=lambda *_: App.get_running_app().go_editor())
        self.layout.add_widget(self.btn_new)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=(0, dp(4)))
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.grid.clear_widgets()
        app = App.get_running_app()
        if app.dek is None:
            return
        notes = NotesManager(app.db).read_notes(app.dek)
        if not notes:
            self.grid.add_widget(VaultLabel(
                text="No notes yet. Create your first secure note.",
                size=15, color="TEXT_MUTED", size_hint_y=None, height=dp(55),
            ))
            return

        for note in notes:
            panel = MetalPanel(
                orientation="vertical", size_hint_y=None,
                height=dp(76), padding=dp(10), spacing=dp(4),
            )
            panel.add_widget(VaultLabel(
                text=note["title"], size=17, color="TEXT_LIGHT",
                halign="left", valign="middle",
            ))
            actions = BoxLayout(size_hint_y=None, height=dp(28), spacing=dp(8))
            actions.add_widget(VaultLabel(
                text=note["body"][:70].replace("\n", " "),
                size=11, color="TEXT_MUTED", halign="left",
            ))
            delete = TactileButton(
                text="DEL", color="ACCENT_RED",
                size_hint=(None, 1), width=dp(55),
            )
            delete.bind(on_release=lambda *_args, nid=note["id"]: self.delete(nid))
            actions.add_widget(delete)
            panel.add_widget(actions)
            self.grid.add_widget(panel)

    def delete(self, note_id):
        app = App.get_running_app()
        NotesManager(app.db).delete_note(note_id)
        self.refresh()
