from kivy.utils import get_color_from_hex


class Theme:
    BG_OBSIDIAN = "#050505"
    BG_GRAPHITE = "#121418"
    METALLIC_SILVER = "#C0C5CE"
    CHARCOAL = "#1E2025"
    ACCENT_BLUE = "#007AFF"
    ACCENT_GREEN = "#34C759"
    ACCENT_RED = "#FF3B30"
    TEXT_LIGHT = "#E5E9F0"
    TEXT_MUTED = "#8A95A5"
    RADIUS = [12]

    @classmethod
    def get(cls, color_name):
        return get_color_from_hex(getattr(cls, color_name))
