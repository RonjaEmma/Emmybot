
# database_rp.py
import sqlite3
import os
from config import AFFECTION_TITLES
from datetime import datetime, timezone
DB_PATH = "emmy.db"

# =====================================================
# Internal helper
# =====================================================

def _connect():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# Database init
# =====================================================

def init_rp_db():
    with _connect() as db:
        tables = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        print("TABLES:", tables)
        # RP interactions
        db.execute("""
        CREATE TABLE IF NOT EXISTS rp_interactions (
            guild_id INTEGER NOT NULL,
            actor_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (guild_id, actor_id, target_id, action)
        )
        """)
                # Reminders
        db.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            remind_at TEXT,
            message TEXT
        )
        """)
        def log_thread(
    guild_id: int,
    thread_id: int,
    parent_channel_id: int,
    name: str,
    owner_id: int | None,
    is_private: bool,
    created_at: str
):
            with db:
                db.execute("""
            INSERT OR IGNORE INTO threads (
                thread_id,
                guild_id,
                parent_channel_id,
                name,
                owner_id,
                is_private,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            thread_id,
            guild_id,
            parent_channel_id,
            name,
            owner_id,
            int(is_private),
            created_at
        ))
         
                # User memory / affection
        db.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            guild_id INTEGER,
            user_id INTEGER,
            first_met TEXT,
            last_interaction TEXT,
            interaction_count INTEGER DEFAULT 0,
            affection INTEGER DEFAULT 10,
            last_welcome TEXT,
            PRIMARY KEY (guild_id, user_id)
        )
        """)

                # Channel activity
        db.execute("""
        CREATE TABLE IF NOT EXISTS channel_activity (
            guild_id INTEGER,
            channel_id INTEGER,
            last_message TEXT,
            message_count INTEGER DEFAULT 0,
            PRIMARY KEY (guild_id, channel_id)
        )
        """)

        # Channel user activity
        db.execute("""
        CREATE TABLE IF NOT EXISTS channel_users (
            guild_id INTEGER,
            channel_id INTEGER,
            user_id INTEGER,
            messages INTEGER DEFAULT 0,
            PRIMARY KEY (guild_id, channel_id, user_id)
        )
        """)
        
        db.execute("""
        CREATE TABLE IF NOT EXISTS guild_activity (
             guild_id INTEGER PRIMARY KEY,
             last_active TIMESTAMP
        )
        """)
    
        db.execute("""
                   CREATE TABLE IF NOT EXISTS threads (
                       thread_id INTEGER PRIMARY KEY,
                       guild_id INTEGER NOT NULL,
                       parent_channel_id INTEGER NOT NULL,
                       name TEXT NOT NULL,
                       owner_id INTEGER,
                       is_private INTEGER NOT NULL,
                       created_at TEXT NOT NULL
                       )
                       """)

                
        db.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, user_id)
        )
        """)


        # Chaos scores
        db.execute("""
        CREATE TABLE IF NOT EXISTS chaos_scores (
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (guild_id, user_id)
        )
        """)

        # Secret stats
        db.execute("""
        CREATE TABLE IF NOT EXISTS secret_stats (
            guild_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            count INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (guild_id, sender_id, receiver_id)
        )
        """)
        

        db.execute("""
        CREATE TABLE IF NOT EXISTS guild_activity (
            guild_id INTEGER PRIMARY KEY,
            last_active TIMESTAMP
            )
            """)
        
        db.execute("""
        CREATE TABLE IF NOT EXISTS peek_channels (
            guild_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            PRIMARY KEY (guild_id, channel_id)
            )
            """)

def init_sacrifice_table():
    with _connect() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS sacrifice_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            actor_id INTEGER,
            target_id INTEGER,
            timestamp TEXT
        )
        """)


def init_favorites():
    with _connect() as db:
        # Create table if missing
        db.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            added_at TEXT,
            chooser_id INTEGER,
            PRIMARY KEY (guild_id, user_id)
        )
        """)

        # Backward compatibility: add chooser_id if table already existed
        try:
            db.execute("ALTER TABLE favorites ADD COLUMN chooser_id INTEGER")
        except sqlite3.OperationalError:
            # Column already exists
            pass




# =====================================================
# RP interaction tracking
# =====================================================

def increment_rp_interaction(guild_id, actor_id, target_id, action):
    with _connect() as db:
        db.execute("""
        INSERT INTO rp_interactions (guild_id, actor_id, target_id, action, count)
        VALUES (?, ?, ?, ?, 1)
        ON CONFLICT(guild_id, actor_id, target_id, action)
        DO UPDATE SET count = count + 1
        """, (guild_id, actor_id, target_id, action))

        row = db.execute("""
        SELECT count FROM rp_interactions
        WHERE guild_id=? AND actor_id=? AND target_id=? AND action=?
        """, (guild_id, actor_id, target_id, action)).fetchone()

        return row["count"] if row else 0


def get_mutual_interaction_count(guild_id, user_a, user_b, action):
    with _connect() as db:
        row = db.execute("""
        SELECT
            IFNULL(a.count, 0) + IFNULL(b.count, 0) AS total
        FROM
            (SELECT count FROM rp_interactions
             WHERE guild_id=? AND actor_id=? AND target_id=? AND action=?) a
        LEFT JOIN
            (SELECT count FROM rp_interactions
             WHERE guild_id=? AND actor_id=? AND target_id=? AND action=?) b
        """, (
            guild_id, user_a, user_b, action,
            guild_id, user_b, user_a, action
        )).fetchone()

        return row["total"] if row else 0


# =====================================================
# Chaos tracking
# =====================================================

def increment_chaos_score(guild_id, user_id):
    with _connect() as db:
        db.execute("""
        INSERT INTO chaos_scores (guild_id, user_id, score)
        VALUES (?, ?, 1)
        ON CONFLICT(guild_id, user_id)
        DO UPDATE SET score = score + 1
        """, (guild_id, user_id))


def get_chaos_leaderboard(guild_id, limit=10):
    with _connect() as db:
        rows = db.execute("""
        SELECT user_id, score
        FROM chaos_scores
        WHERE guild_id=?
        ORDER BY score DESC
        LIMIT ?
        """, (guild_id, limit)).fetchall()

        return rows


# =====================================================
# Secret tracking
# =====================================================

def increment_secret_sent(guild_id, sender_id, receiver_id):
    with _connect() as db:
        db.execute("""
        INSERT INTO secret_stats (guild_id, sender_id, receiver_id, count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(guild_id, sender_id, receiver_id)
        DO UPDATE SET count = count + 1
        """, (guild_id, sender_id, receiver_id))


def get_secret_count(guild_id, sender_id, receiver_id):
    with _connect() as db:
        row = db.execute("""
        SELECT count FROM secret_stats
        WHERE guild_id=? AND sender_id=? AND receiver_id=?
        """, (guild_id, sender_id, receiver_id)).fetchone()

        return row["count"] if row else 0


def get_secret_stats_for_user(guild_id, user_id):
    with _connect() as db:
        sent = db.execute("""
        SELECT receiver_id, count
        FROM secret_stats
        WHERE guild_id=? AND sender_id=?
        ORDER BY count DESC
        """, (guild_id, user_id)).fetchall()

        received = db.execute("""
        SELECT sender_id, count
        FROM secret_stats
        WHERE guild_id=? AND receiver_id=?
        ORDER BY count DESC
        """, (guild_id, user_id)).fetchall()

        total_sent = sum(row["count"] for row in sent)
        total_received = sum(row["count"] for row in received)

        return sent, received, total_sent, total_received

def touch_user(guild_id, user_id):
    now = datetime.now(timezone.utc).isoformat()

    with _connect() as db:
        db.execute("""
        INSERT INTO user_memory (
            guild_id,
            user_id,
            first_met,
            last_interaction,
            interaction_count,
            affection
        )
        VALUES (?, ?, ?, ?, 1, 10)
        ON CONFLICT(guild_id, user_id)
        DO UPDATE SET
            last_interaction = ?,
            interaction_count = interaction_count + 1,
            affection = affection + 1
        """, (
            guild_id,
            user_id,
            now,
            now,
            now
        ))

def get_user_profile(guild_id, user_id):
    with _connect() as db:
        row = db.execute("""
        SELECT
            first_met,
            last_interaction,
            interaction_count,
            affection,
            last_welcome
        FROM user_memory
        WHERE guild_id = ? AND user_id = ?
        """, (guild_id, user_id)).fetchone()

        return row


def update_last_welcome(guild_id, user_id):
    with _connect() as db:
        db.execute("""
        UPDATE user_memory
        SET last_welcome = ?
        WHERE guild_id = ? AND user_id = ?
        """, (datetime.utcnow(), guild_id, user_id))


def add_favorite(guild_id, user_id):
    with _connect() as db:
        db.execute("""
        INSERT OR IGNORE INTO favorites (guild_id, user_id)
        VALUES (?, ?)
        """, (guild_id, user_id))


def remove_favorite(guild_id, user_id):
    with _connect() as db:
        db.execute("""
        DELETE FROM favorites
        WHERE guild_id=? AND user_id=?
        """, (guild_id, user_id))


def get_favorites(guild_id, limit=None):
    with _connect() as db:
        q = """
        SELECT user_id
        FROM favorites
        WHERE guild_id=?
        """
        if limit:
            q += " LIMIT ?"
            return db.execute(q, (guild_id, limit)).fetchall()
        return db.execute(q, (guild_id,)).fetchall()

        return rows
def get_user_title(affection: int):
    

    for threshold, title in AFFECTION_TITLES:
        if affection >= threshold:
            return title
    return "✨ Familiar"

def add_reminder(user_id, remind_at, message):
    with _connect() as db:
        db.execute("""
        INSERT INTO reminders (user_id, remind_at, message)
        VALUES (?, ?, ?)
        """, (user_id, remind_at, message))


def get_due_reminders(now):
    with _connect() as db:
        rows = db.execute("""
        SELECT id, user_id, message
        FROM reminders
        WHERE remind_at <= ?
        """, (now,)).fetchall()
        return rows


def delete_reminder(reminder_id):
    with _connect() as db:
        db.execute("""
        DELETE FROM reminders WHERE id=?
        """, (reminder_id,))


def touch_channel(guild_id, channel_id, user_id):
    now = datetime.utcnow().isoformat()

    with _connect() as db:
        # channel
        db.execute("""
        INSERT INTO channel_activity (guild_id, channel_id, last_message, message_count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(guild_id, channel_id)
        DO UPDATE SET
            last_message=?,
            message_count=message_count+1
        """, (guild_id, channel_id, now, now))

        # channel user
        db.execute("""
        INSERT INTO channel_users (guild_id, channel_id, user_id, messages)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(guild_id, channel_id, user_id)
        DO UPDATE SET messages=messages+1
        """, (guild_id, channel_id, user_id))


def get_active_channels(guild_id, since_iso):
    with _connect() as db:
        return db.execute("""
        SELECT channel_id, last_message
        FROM channel_activity
        WHERE guild_id=? AND last_message >= ?
        """, (guild_id, since_iso)).fetchall()


def get_frequent_user(guild_id, channel_id):
    with _connect() as db:
        return db.execute("""
        SELECT user_id
        FROM channel_users
        WHERE guild_id=? AND channel_id=?
        ORDER BY messages DESC
        LIMIT 1
        """, (guild_id, channel_id)).fetchone()




def touch_guild(guild_id):
    now = datetime.now(timezone.utc)
    with _connect() as db:
        db.execute("""
        INSERT INTO guild_activity (guild_id, last_active)
        VALUES (?, ?)
        ON CONFLICT(guild_id)
        DO UPDATE SET last_active = ?
        """, (guild_id, now, now))


def get_guild_last_active(guild_id):
    with _connect() as db:
        row = db.execute("""
        SELECT last_active
        FROM guild_activity
        WHERE guild_id = ?
        """, (guild_id,)).fetchone()

        if not row:
            return None

        return datetime.fromisoformat(row["last_active"])


def log_thread(
    guild_id: int,
    thread_id: int,
    parent_channel_id: int,
    name: str,
    owner_id: int | None,
    is_private: bool,
    created_at: str
):
    with _connect() as db:
        return db.execute("""
            INSERT OR IGNORE INTO threads (
                guild_id,
                thread_id,
                parent_channel_id,
                name,
                owner_id,
                is_private,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            guild_id,
            thread_id,
            parent_channel_id,
            name,
            owner_id,
            is_private,
            created_at
        ))

def get_recent_threads(guild_id: int, limit: int = 10):
    with _connect() as db:
        cur = db.execute("""
            SELECT *
            FROM threads
            WHERE guild_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (guild_id, limit))
        return cur.fetchall()

# =====================================================
# Peek channel control
# =====================================================

def allow_peek_channel(guild_id, channel_id):
    with _connect() as db:
        db.execute("""
        INSERT OR IGNORE INTO peek_channels (guild_id, channel_id)
        VALUES (?, ?)
        """, (guild_id, channel_id))


def deny_peek_channel(guild_id, channel_id):
    with _connect() as db:
        db.execute("""
        DELETE FROM peek_channels
        WHERE guild_id = ? AND channel_id = ?
        """, (guild_id, channel_id))


def is_peek_channel(guild_id, channel_id) -> bool:
    with _connect() as db:
        row = db.execute("""
        SELECT 1 FROM peek_channels
        WHERE guild_id = ? AND channel_id = ?
        """, (guild_id, channel_id)).fetchone()

        return row is not None


def get_peek_channels(guild_id):
    with _connect() as db:
        rows = db.execute("""
        SELECT channel_id FROM peek_channels
        WHERE guild_id = ?
        """, (guild_id,)).fetchall()

        return [row["channel_id"] for row in rows]

# =================
# toggles
# =================
def init_guild_settings():
    with _connect() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER NOT NULL,
            feature TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (guild_id, feature)
        )
        """)
def is_feature_enabled(guild_id: int, feature: str) -> bool:
    with _connect() as db:
        row = db.execute("""
            SELECT enabled FROM guild_settings
            WHERE guild_id=? AND feature=?
        """, (guild_id, feature)).fetchone()

        # default = enabled
        return True if row is None else bool(row["enabled"])


def set_feature_toggle(guild_id: int, feature: str, enabled: bool):
    with _connect() as db:
        db.execute("""
            INSERT INTO guild_settings (guild_id, feature, enabled)
            VALUES (?, ?, ?)
            ON CONFLICT(guild_id, feature)
            DO UPDATE SET enabled=excluded.enabled
        """, (guild_id, feature, int(enabled)))
        
        # Sacrifice
def log_sacrifice(guild_id, actor_id, target_id):
    now = datetime.now(timezone.utc).isoformat()

    with _connect() as db:
        db.execute("""
        INSERT INTO sacrifice_log (
            guild_id,
            actor_id,
            target_id,
            timestamp
        )
        VALUES (?, ?, ?, ?)
        """, (guild_id, actor_id, target_id, now))
def init_sacrifice_milestones():
    with _connect() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS sacrifice_milestones (
            guild_id INTEGER,
            user_id INTEGER,
            milestone INTEGER,
            PRIMARY KEY (guild_id, user_id, milestone)
        )
        """)
async def check_sacrifice_milestone(guild, actor):
    guild_id = guild.id
    actor_id = actor.id

    with _connect() as db:
        total = db.execute("""
        SELECT COUNT(*) as count
        FROM sacrifice_log
        WHERE guild_id = ? AND actor_id = ?
        """, (guild_id, actor_id)).fetchone()["count"]

        # Check if milestone already announced
        exists = db.execute("""
        SELECT 1 FROM sacrifice_milestones
        WHERE guild_id = ? AND user_id = ? AND milestone = 100
        """, (guild_id, actor_id)).fetchone()

        if total >= 100 and not exists:
            # Save milestone
            db.execute("""
            INSERT INTO sacrifice_milestones (guild_id, user_id, milestone)
            VALUES (?, ?, 100)
            """, (guild_id, actor_id))

            return True

    return False

def get_sacrifice_history(guild_id, member_id=None):
    with _connect() as db:
        if member_id:
            return db.execute("""
                SELECT actor_id, target_id, timestamp
                FROM sacrifice_log
                WHERE guild_id = ?
                AND (actor_id = ? OR target_id = ?)
                ORDER BY id DESC
                LIMIT 10
            """, (guild_id, member_id, member_id)).fetchall()
        else:
            return db.execute("""
                SELECT actor_id, target_id, timestamp
                FROM sacrifice_log
                WHERE guild_id = ?
                ORDER BY id DESC
                LIMIT 10
            """, (guild_id,)).fetchall()


def get_sacrifice_top(guild_id):
    with _connect() as db:
        return db.execute("""
            SELECT actor_id, COUNT(*) as total
            FROM sacrifice_log
            WHERE guild_id = ?
            GROUP BY actor_id
            ORDER BY total DESC
            LIMIT 5
        """, (guild_id,)).fetchall()


def reset_user_emmy_relation(guild_id: int, user_id: int):
    with _connect() as db:
        db.execute("""
        UPDATE user_memory
        SET
            interaction_count = 0,
            affection = 0,
            last_interaction = NULL,
            last_welcome = NULL
        WHERE guild_id = ? AND user_id = ?
        """, (guild_id, user_id))

def delete_user_emmy_relation(guild_id: int, user_id: int):
    with _connect() as db:
        db.execute("""
        DELETE FROM user_memory
        WHERE guild_id = ? AND user_id = ?
        """, (guild_id, user_id))
