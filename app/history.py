import sqlite3
import json
from datetime import datetime


class LessonHistory:

    def __init__(self, db_path="lesson_history.db"):
        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                video_url TEXT NOT NULL,
                title TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                video_type TEXT,
                lesson TEXT NOT NULL,
                created_at TEXT NOT NULL,
                chat_messages TEXT NOT NULL DEFAULT '[]',
                chat_summary TEXT NOT NULL DEFAULT ''
            )
        """)

        self.conn.commit()

    def save_lesson(
        self,
        video_id: str,
        video_url: str,
        lesson,
        difficulty: str,
        video_type: str,
        chat_messages=None,
        chat_summary=""
    ):

        if chat_messages is None:
            chat_messages = []

        self.conn.execute(
            """
            INSERT INTO lessons (
                video_id,
                video_url,
                title,
                difficulty,
                video_type,
                lesson,
                chat_messages,
                chat_summary,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                video_id,
                video_url,
                lesson.title,
                difficulty,
                video_type,
                lesson.model_dump_json(),
                json.dumps(chat_messages),
                chat_summary,
                datetime.now().isoformat()
            )
        )

        self.conn.commit()
        
        return self.conn.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]
        
    def get_lessons(self):
        cursor = self.conn.execute(
            """
            SELECT
                id,
                video_id,
                video_url,
                title,
                difficulty,
                video_type,
                created_at
            FROM lessons
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "video_id": row[1],
                "video_url": row[2],
                "title": row[3],
                "difficulty": row[4],
                "video_type": row[5],
                "created_at": row[6],
            }
            for row in rows
        ]
        
    def get_lesson(self, lesson_id: int):

        cursor = self.conn.execute(
            """
            SELECT
                video_id,
                video_url,
                title,
                difficulty,
                video_type,
                lesson,
                chat_messages,
                chat_summary
            FROM lessons
            WHERE id = ?
            """,
            (lesson_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "video_id": row[0],
            "video_url": row[1],
            "title": row[2],
            "difficulty": row[3],
            "video_type": row[4],
            "lesson": row[5],
            "chat_messages": json.loads(row[6]),
            "chat_summary": row[7],
        }
        
    def update_chat(
        self,
        lesson_id: int,
        chat_messages: list,
        chat_summary: str
    ):
        self.conn.execute(
            """
            UPDATE lessons
            SET chat_messages = ?,
                chat_summary = ?
            WHERE id = ?
            """,
            (
                json.dumps(chat_messages),
                chat_summary,
                lesson_id
            )
        )

        self.conn.commit()