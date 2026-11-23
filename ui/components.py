from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line

from ui.theme import Theme


class MetalPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 0.5)
            self.shadow = RoundedRectangle(
                pos=(self.x + dp(2), self.y - dp(4)),
                size=self.size, radius=Theme.RADIUS,
            )
            Color(*Theme.get("BG_GRAPHITE"))
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=Theme.RADIUS)
            Color(*Theme.get("METALLIC_SILVER"))
            self.border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)),
                width=1.0,
            )
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *_):
        self.shadow.pos = (self.x + dp(2), self.y - dp(4))
        self.shadow.size = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rounded_rectangle = (
            self.x, self.y, self.width, self.height, dp(12),
        )


class TactileButton(Button):
    def __init__(self, text, color="ACCENT_BLUE", **kwargs):
        super().__init__(text=text, **kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = Theme.get("TEXT_LIGHT")
        self.bold = True
        self.font_size = dp(15)
        self._btn_color = Theme.get(color)
        self._state = "normal"

        with self.canvas.before:
            Color(0, 0, 0, 0.4)
            self.shadow = RoundedRectangle(
                pos=(self.x, self.y - dp(4)), size=self.size, radius=Theme.RADIUS,
            )
            Color(*self._btn_color)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=Theme.RADIUS)
            Color(1, 1, 1, 0.3)
            self.highlight = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)),
                width=1,
            )
        self.bind(pos=self.update_graphics, size=self.update_graphics, state=self.on_state_change)

    def update_graphics(self, *_):
        offset = dp(2) if self._state == "down" else 0
        self.shadow.pos = (self.x, self.y - dp(4) + offset)
        self.bg.pos = (self.x, self.y - offset)
        self.bg.size = self.size
        self.highlight.rounded_rectangle = (
            self.x, self.y - offset, self.width, self.height, dp(12),
        )

    def on_state_change(self, _instance, value):
        self._state = value
        self.update_graphics()


class RecessedInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = Theme.get("TEXT_LIGHT")
        self.cursor_color = Theme.get("ACCENT_BLUE")
        self.hint_text_color = Theme.get("TEXT_MUTED")
        self.padding = [dp(14), dp(14)]
        with self.canvas.before:
            Color(0, 0, 0, 0.75)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=Theme.RADIUS)
            Color(0.35, 0.38, 0.43, 0.7)
            self.inner_border = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)),
                width=1,
            )
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.inner_border.rounded_rectangle = (
            self.x, self.y, self.width, self.height, dp(12),
        )


class VaultLabel(Label):
    def __init__(self, text, size=16, color="TEXT_LIGHT", **kwargs):
        super().__init__(
            text=text, font_size=dp(size), color=Theme.get(color),
            **kwargs,
        )
