# config.py

PREFIX = "!"

EMMY_ID = 1467562178956623984  # Emmy's user ID

JEALOUS_CHANCE = 0.2  # or whatever value you want

# -----------------------------
# Emmy Memory Config
# -----------------------------

MIN_AFFECTION = 5
AFFECTION_GAIN = 1
AFFECTION_DECAY_PER_DAY = 1

SHORT_ABSENCE_DAYS = 1
LONG_ABSENCE_DAYS = 7

FAVORITE_COUNT = 5

# -----------------------------
# Emmy Favorites & Titles
# -----------------------------

FAVORITE_LIMIT = 5

AFFECTION_TITLES = [
    (120, "💞 Pookie"),
    (90,  "🌸 Bestie"),
    (60,  "💫 Crush"),
    (30,  "🐣 Soft Spot"),
    (0,   "✨ Familiar"),
]
PEEK_CHANCE = 0.04        # 4% per message
REACT_ONLY_CHANCE = 0.35
MIN_CHANNEL_COOLDOWN = 30 * 60  # 1 hour



from datetime import datetime, timedelta

GUILD_ACTIVITY = {}  # guild_id -> last_activity_iso

def touch_guild(guild_id: int):
    GUILD_ACTIVITY[guild_id] = datetime.utcnow().isoformat()

def get_guild_last_activity(guild_id: int):
    return GUILD_ACTIVITY.get(guild_id)

FEATURES = {
    "rp_actions": "Roleplay actions",
    "whispers": "Whispers",
    "secrets": "Secrets",
    "chaos": "Chaos system",
    "favorites": "Favorites & jealousy",
    "peek": "Channel peeking",
    "welcome_back": "Welcome-back messages",
    "silence_wake": "Silence wake messages",
    "threads": "Thread creation & logging",
    "reminders": "Reminders",
}

# PASSIVE MISSING

LAST_PASSIVE_MISSING = {}  # guild_id -> datetime
PASSIVE_MISSING_INTERVAL = timedelta(minutes=30)
PASSIVE_MISSING_CHANCE = 0.35  # not every time

FAVORITE_MISSING_LINES = [
    "I keep listening for {name}.",
    "{name} feels closer than silence usually allows.",
    "I noticed {name} wasn’t here.",
    "Some absences echo louder. {name}’s does.",
    "I’ve been waiting for {name}.",
    "{name} usually lingers longer than this.",
    "Something feels off without {name}.",
    "I keep expecting {name} to return.",
]
