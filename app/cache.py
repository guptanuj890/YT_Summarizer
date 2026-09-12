import json
import sqlite3

class TranscriptCache:
    def __init__(self, db_path = "lesson_cache.db"):
        self.conn = sqlite3.connect(db_path)
        
        self.conn.execute(
            """ CREATE TABLE IF NOT EXISTS transcripts(
                video_id TEXT PRIMARY KEY,
                transcript TEXT NOT NULL
            )
            """
        )
        self.conn.commit()
        
    def get(self, video_id: str):
        cursor = self.conn.execute(
            "SELECT transcript From transcripts WHERE video_id = ?",
            (video_id,)
        )
        
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return json.loads(row[0])
    
    def set(self, video_id: str, transcript: list[dict]):
        self.conn.execute(
            """
            INSERT OR REPLACE INTO transcripts
            (video_id, transcript)
            VALUES(?, ?)
            """,
            (
                video_id,
                json.dumps(transcript)
            )
        )
        
        self.conn.commit()