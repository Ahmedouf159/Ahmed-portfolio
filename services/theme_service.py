from models.user_model import update_theme

def normalize_theme(theme: str):
    theme = (theme or "").strip().lower()
    if theme not in ("dark", "light", "system"):
        return None
    return theme

def save_theme(user_id: int, theme: str):
    theme = normalize_theme(theme)
    if not theme:
        return False, "Invalid theme."
    update_theme(user_id, theme)
    return True, theme
