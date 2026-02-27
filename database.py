import sqlite3
import json
import os
import hashlib
import binascii

DB_PATH = os.path.join("data", "quiz.db")


def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            category TEXT,
            question TEXT,
            options TEXT,
            correct INTEGER,
            difficulty TEXT,
            points INTEGER
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            category TEXT,
            score INTEGER,
            total_questions INTEGER,
            correct_answers INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def _hash_password(password: str, salt: bytes) -> str:
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return binascii.hexlify(dk).decode()


def create_user(username: str, password: str) -> bool:
    salt = os.urandom(16)
    password_hash = _hash_password(password, salt)
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
            (username, password_hash, binascii.hexlify(salt).decode()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username: str, password: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, salt FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    user_id, stored_hash, salt_hex = row
    salt = binascii.unhexlify(salt_hex.encode())
    if _hash_password(password, salt) == stored_hash:
        return user_id
    return None


def add_question(category: str, question: str, options: list, correct: int, difficulty: str, points: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO questions (category, question, options, correct, difficulty, points) VALUES (?, ?, ?, ?, ?, ?)",
        (category, question, json.dumps(options), correct, difficulty, points),
    )
    conn.commit()
    conn.close()


def get_questions():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, category, question, options, correct, difficulty, points FROM questions")
    rows = cur.fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "category": r[1],
            "question": r[2],
            "options": json.loads(r[3]) if r[3] else [],
            "correct": r[4],
            "difficulty": r[5],
            "points": r[6],
        })
    return results


def get_question_by_id(qid: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, category, question, options, correct, difficulty, points FROM questions WHERE id=?", (qid,))
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    return {
        "id": r[0],
        "category": r[1],
        "question": r[2],
        "options": json.loads(r[3]) if r[3] else [],
        "correct": r[4],
        "difficulty": r[5],
        "points": r[6],
    }


def update_question(qid: int, category: str, question: str, options: list, correct: int, difficulty: str, points: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE questions SET category=?, question=?, options=?, correct=?, difficulty=?, points=? WHERE id=?
        """,
        (category, question, json.dumps(options), correct, difficulty, points, qid),
    )
    conn.commit()
    conn.close()


def delete_question(qid: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    conn.close()


def add_score(user_id: int, category: str, score: int, total_questions: int, correct_answers: int):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scores (user_id, category, score, total_questions, correct_answers) VALUES (?, ?, ?, ?, ?)",
        (user_id, category, score, total_questions, correct_answers),
    )
    conn.commit()
    conn.close()


def get_highscores(limit=10):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT s.score, s.category, s.total_questions, s.correct_answers, s.timestamp, u.username
        FROM scores s
        LEFT JOIN users u ON s.user_id=u.id
        ORDER BY s.score DESC, s.timestamp ASC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "score": r[0],
            "category": r[1],
            "total_questions": r[2],
            "correct_answers": r[3],
            "timestamp": r[4],
            "username": r[5] or "Anonymous",
        }
        for r in rows
    ]


def clear_scores():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
