import sqlite3
import os
from typing import Optional

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db")
DB_PROFILES = os.path.join(DB_DIR, "profiles.db")
DB_PROJECTS = os.path.join(DB_DIR, "projects.db")


def init_db():
    """Создание таблиц, если их нет"""
    os.makedirs(DB_DIR, exist_ok=True)

    # --- База профилей ---
    conn = sqlite3.connect(DB_PROFILES)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            tg_username TEXT DEFAULT '',
            name TEXT DEFAULT '',
            skills TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    # --- База проектов ---
    conn = sqlite3.connect(DB_PROJECTS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id INTEGER NOT NULL,
            creator_nick TEXT DEFAULT '',
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            requirements TEXT DEFAULT '',
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# ====================== ПРОФИЛИ ======================

def save_profile(user_id: int, name: str, skills: str, rank: str, tg_username: str = "") -> None:
    """Сохранить или обновить профиль пользователя"""
    conn = sqlite3.connect(DB_PROFILES)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO profiles (user_id, tg_username, name, skills, rank)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            name = excluded.name,
            skills = excluded.skills,
            rank = excluded.rank,
            tg_username = excluded.tg_username
    """, (user_id, tg_username, name, skills, rank))
    conn.commit()
    conn.close()


def get_profile(user_id: int) -> Optional[dict]:
    """Получить профиль пользователя по user_id"""
    conn = sqlite3.connect(DB_PROFILES)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return {
        "user_id": row[0],
        "tg_username": row[1],
        "name": row[2],
        "skills": row[3],
        "rank": row[4],
        "created_at": row[5],
    }


def profile_exists(user_id: int) -> bool:
    """Проверить, есть ли профиль у пользователя"""
    conn = sqlite3.connect(DB_PROFILES)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM profiles WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


# ====================== ПРОЕКТЫ ======================

def save_project(creator_id: int, creator_nick: str, name: str, description: str, requirements: list) -> int:
    """Сохранить проект в БД и вернуть его id"""
    conn = sqlite3.connect(DB_PROJECTS)
    cursor = conn.cursor()
    req_text = ", ".join(requirements) if requirements else ""
    cursor.execute("""
        INSERT INTO projects (creator_id, creator_nick, name, description, requirements)
        VALUES (?, ?, ?, ?, ?)
    """, (creator_id, creator_nick, name, description, req_text))
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return project_id


def get_projects_by_user(user_id: int) -> list:
    """Получить все проекты пользователя"""
    conn = sqlite3.connect(DB_PROJECTS)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE creator_id = ? ORDER BY created_at DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    projects = []
    for row in rows:
        projects.append({
            "id": row[0],
            "creator_id": row[1],
            "creator_nick": row[2],
            "name": row[3],
            "description": row[4],
            "requirements": row[5],
            "status": row[6],
            "created_at": row[7],
        })
    return projects


def get_all_projects() -> list:
    """Получить все активные проекты"""
    conn = sqlite3.connect(DB_PROJECTS)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE status = 'active' ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    projects = []
    for row in rows:
        projects.append({
            "id": row[0],
            "creator_id": row[1],
            "creator_nick": row[2],
            "name": row[3],
            "description": row[4],
            "requirements": row[5],
            "status": row[6],
            "created_at": row[7],
        })
    return projects