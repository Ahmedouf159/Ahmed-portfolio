from models.db import get_db

def create_user(username: str, email: str, password_hash: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users(username, email, password_hash, theme) VALUES(?,?,?,?)",
        (username, email, password_hash, "system")
    )
    conn.commit()
    conn.close()

def find_user_by_login(login_id: str):
    login_id = (login_id or "").strip().lower()
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE lower(email)=? OR lower(username)=?",
        (login_id, login_id)
    ).fetchone()
    conn.close()
    return user

def find_user_by_id(user_id: int):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return user

def update_username(user_id: int, new_username: str):
    conn = get_db()
    conn.execute("UPDATE users SET username=? WHERE id=?", (new_username, user_id))
    conn.commit()
    conn.close()

def update_password_hash(user_id: int, new_hash: str):
    conn = get_db()
    conn.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, user_id))
    conn.commit()
    conn.close()

def update_theme(user_id: int, theme: str):
    conn = get_db()
    conn.execute("UPDATE users SET theme=? WHERE id=?", (theme, user_id))
    conn.commit()
    conn.close()
