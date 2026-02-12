
# bot.py
import discord
from discord.ext import commands, tasks
import random
import os 
import asyncio
from config import PREFIX, FEATURES
from rp_assets import RP_ACTIONS, generate_rp, generate_whisper_public, ACTION_TARGET_MODE
from database_rp import (
    increment_rp_interaction,
    get_mutual_interaction_count,
    increment_chaos_score,
    get_chaos_leaderboard,
    increment_secret_sent,
    get_secret_count,
    get_secret_stats_for_user,
    init_rp_db
)
from database_rp import (
    touch_user,
    get_user_profile,
    get_favorites,
)
from rp_assets import welcome_back_lines, MISSING_LINES
from config import (
    SHORT_ABSENCE_DAYS,
    LONG_ABSENCE_DAYS,
)
from database_rp import get_favorites, get_user_title, is_peek_channel, add_favorite, remove_favorite
from rp_assets import favorite_lines, jealousy_lines
from config import FAVORITE_LIMIT
from database_rp import add_reminder, get_due_reminders, delete_reminder
from datetime import timedelta
from database_rp import touch_channel, get_frequent_user
from rp_assets import peek_lines, wake_lines, EMMY_ID, generate_emmy_reaction
from config import (
    PEEK_CHANCE,
    REACT_ONLY_CHANCE,
    MIN_CHANNEL_COOLDOWN,
    JEALOUS_CHANCE,
    PASSIVE_MISSING_CHANCE,
    PASSIVE_MISSING_INTERVAL,
    LAST_PASSIVE_MISSING,
    FAVORITE_MISSING_LINES
)
from datetime import datetime, timedelta, timezone
from database_rp import (
    touch_guild,
    get_guild_last_active,
    touch_channel,
    get_frequent_user,
    init_favorites,
    init_guild_settings,
    is_feature_enabled,
    set_feature_toggle,
    init_sacrifice_table,
    log_sacrifice,
    init_sacrifice_milestones,
    check_sacrifice_milestone

)
from database_rp import log_thread, get_recent_threads, allow_peek_channel, deny_peek_channel, get_peek_channels
from database_rp import get_sacrifice_history, get_sacrifice_top, reset_user_emmy_relation, delete_user_emmy_relation
from emmy_rp import EmmyRP
from dotenv import load_dotenv
    
# -----------------------------
# Bot setup
# -----------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True   # 🔴 THIS LINE IS REQUIRED
intents.guilds = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

FAVORITE_MISSING_THRESHOLD = timedelta(hours=6)
MISSING_THRESHOLD = timedelta(minutes=1)
MISSING_COOLDOWN = timedelta(hours=8)
PENDING_CONFIRMATIONS = {}
CONFIRM_TIMEOUT = 30  # seconds
AFFECTION_CONFIRM_THRESHOLD = 50

last_missing_run = {}  # guild_id -> datetime
JEALOUS_CHANCE = 0.06  # 6% chance

LAST_DM_SOURCE = {}
last_peek = {}  # (guild_id, channel_id): datetime
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# -----------------------------
# Events
# -----------------------------

@bot.event
async def on_ready():
    init_rp_db()
    reminder_loop.start()
    silence_watch.start()
    init_sacrifice_table()
    cleanup_confirmations.start()
    init_favorites()
    init_sacrifice_milestones()
    init_guild_settings()
    if not passive_missing_loop.is_running():
        passive_missing_loop.start()
    await bot.add_cog(EmmyRP(bot))





    print("RP database ready ✨")
    print(f"[READY] Logged in as {bot.user} 💖")
# -----------------------------
# Permission helpers
# -----------------------------
def is_thread(channel: discord.abc.GuildChannel) -> bool:
    return isinstance(
        channel,
        (discord.Thread, discord.threads.Thread)
    )

def owner_or_admin():
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author):
            return True

        if ctx.guild and ctx.author.guild_permissions.administrator:
            return True

        return False

    return commands.check(predicate)
# -----------------------------
# Command groups
# -----------------------------

@bot.group(name="emmy", aliases=["em"], invoke_without_command=True)
async def emmy(ctx):
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(
        title="✨ Hi hi~ I’m Emmy! 💖",
        description=(
            "૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა ✨\n\n"
            "I’m your **cute little companion** 💕\n"
            "Here to spread:\n\n"
            "🤗 hugs\n"
            "💋 kisses\n"
            "🐣 pats\n"
            "🔨 bonks\n"
            "🤫 secret messages\n"
            "🔔 announcements\n"
            "And many more\n\n"
            "I help everyone feel comfy, silly, and cared for 🌸💫"
        ),
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.add_field(
        name="About me",
        value="Type **`!emmy intro`** or **`!em intro`** to learn more about me💞",
        inline=False
    )

    embed.add_field(
        name="✨ Need help?",
        value="Type **`!emmy help`** or **`!em help`** to see what I can do 💌",
        inline=False
    )

    embed.set_footer(
        text="Emmy is always here for you ♡",
        icon_url="https://cdn.discordapp.com/attachments/1461666173996372140/1467582747143966933/IMG_93079.png?ex=698b7471&is=698a22f1&hm=99bc70f33860f55171d6929d056a9a7999855fbbc6b6f406501424e9c5b3a12a"
    )

    await ctx.send(embed=embed)


# -----------------------------
# AUTO RP COMMAND REGISTRATION
# -----------------------------

def register_rp_command(action_name: str):
    async def _rp(ctx, target: discord.Member = None):
        actor = ctx.author
        guild_id = ctx.guild.id
        print(f"RP command triggered: {action_name}")
        reaction = None  # ✅ ALWAYS defined


        if not is_feature_enabled(guild_id, "rp_actions"):
            return

        # target handling
        mode = ACTION_TARGET_MODE.get(action_name, "target")

        if mode == "self":
            target = actor
        elif mode == "target" and target is None:
            await ctx.send(f"❌ **{action_name}** needs a target.")
            return
        elif mode == "optional" and target is None:
            target = actor

        if target and target.id == actor.id and mode == "target":
            await ctx.send("🤍 You can’t do that to yourself.")
            return

        # log sacrifice only if action is sacrifice
        if action_name == "sacrifice" and target:
            log_sacrifice(guild_id, actor.id, target.id)

            milestone = await check_sacrifice_milestone(ctx.guild, actor)
            if milestone:
                embed = discord.Embed(
                    title="🌑 A Dark Achievement",
                    description=f"🩸 {actor.mention} has performed **100 sacrifices**.\n\nEmmy watches in silence.",
                    color=0x4A148C
                )
                embed.set_footer(text="✦ The ritual circle hums ✦")
                await ctx.send(embed=embed)

        count = increment_rp_interaction(
            guild_id, actor.id, target.id if target else actor.id, action_name
        )

        mutual = get_mutual_interaction_count(
            guild_id, actor.id, target.id if target else actor.id, action_name
        )

        increment_chaos_score(guild_id, actor.id)

        payload = generate_rp(action_name, actor, target, count, mutual)

        # --- special modes ---
        mode = payload.get("mode")

        if mode == "react":
            await ctx.message.add_reaction(payload["emoji"])
            return

        if mode == "dots":
            await ctx.send("…")
            return

        text = payload["text"]

        if mode == "short":
            text = text.split(".")[0] + "."

        if payload.get("escalation"):
            text += f"\n\n*{payload['escalation']}*"

        if payload.get("mutual"):
            text += f"\n\n💫 *{payload['mutual']}*"

        embed = discord.Embed(
            description=f"{payload['emoji']} {text}",
            color=discord.Color.from_rgb(255, 182, 193)
        )

        if payload.get("gif"):
            embed.set_image(url=payload["gif"])
        
        
        if target and target.id == EMMY_ID:
            reaction = generate_emmy_reaction(action_name)
            if reaction:
                embed.add_field(
                    name="🌸 Emmy",
                    value=reaction,
                    inline=False
                    )


        footer_target = target.display_name if target else actor.display_name
        embed.set_footer(
            text=f"{actor.display_name} ↔ {footer_target} • {mutual} shared"
        )

        await ctx.send(embed=embed)

        # 🔥 delete command message but keep memory
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

    # ✅ THESE LINES MUST BE HERE
    _rp.__name__ = action_name
    emmy.add_command(commands.Command(_rp, name=action_name))


# 🔥 AUTO-REGISTER ALL RP COMMANDS
for action in RP_ACTIONS.keys():
    register_rp_command(action)


# -----------------------------
# HELP COMMAND (AUTO-GENERATED)
# -----------------------------

@emmy.command()
async def help(ctx):
    is_admin = ctx.author.guild_permissions.administrator
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    actions = ", ".join(f"`{a}`" for a in sorted(RP_ACTIONS.keys()))

    description = (
        f"Use any of these with **`!emmy <action> @user/none`**\n\n"
        f"{actions}\n\n"
        f"Other Commands\n"
        f"!emmy chaos - check chaos leaderboard\n"
        f"!emmy bloodytop - check sacrifice leaderboard\n"
        f"!emmy bloodyhistory @user - check user sacrifice history\n"
        f"!emmy profile @user - check Emmy's interaction\n"
        f"!emmy whisper @user <message> - partial hidden\n"
        f"!emmy secret @user <message> - fully hidden\n"
        f"!emmy remind <minute> <reason> - reminder\n"
        f"!emmy bring <count> @user - randomizer any amount\n"
        f"!emmy gather #channel <name of thread> @user - gather and create a thread\n"
        f"!emmy gatherprivate #channel <name of thread> @user - gather and create a private thread\n\n"
    )

    # 🔒 Admin-only section (hidden from non-admins)
    if is_admin:
        description += (
            "Admin Commands\n"
            "!emmy secretstats @user - checks secrets sent\n"
            "!emmy say <message> - speaks as bot\n"
            "!emmy announce @role <message> - announcement\n"
            "!emmy status - admin debug panel\n"
            "!emmy failsafe - override emergency\n"
            "!emmy threads - check threads created\n"
            "!emmy toggle <feature> - feature toggle\n"
            "!emmy toggles - list of feature toggles\n"
            "!emmy peek - to call out Emmy just cause\n"
            "!emmy peekallow - allow Emmy to peek here\n"
            "!emmy peekdeny - stop Emmy peeking here\n"
            "!emmy peeklist - list peek channels\n"
            "!emmy resetbond @user - reset affection and interactions of Emmy\n"
            "!emmy forget @user - reset like Emmy never met @user\n"
            "!emmy favorite @user - add @user as Emmy favorite\n"
            "!emmy unfavorite @user - remove @user from the favorite list\n"
            "!emmy favorites - list of favorites\n\n"
        )

    description += "Some actions may change over time… 💞"

    embed = discord.Embed(
        title="🌸 Emmy’s RP Commands",
        description=description,
        color=discord.Color.from_rgb(255, 182, 193)
    )

    if is_admin:
        embed.set_footer(text="Admin view enabled 👀")
    else:
        embed.set_footer(text="Emmy notices patterns 👀")

    await ctx.send(embed=embed)
# -----------------------------
# Emmy Introduction
# -----------------------------

@emmy.command()
async def intro(ctx):
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(
        title="🌸 Hi hi~ I’m Emmy! 💖",
        description=(
            "I’m your **soft little roleplay companion**, here to make the server feel\n"
            "warmer, sillier, and just a bit more alive 🌷\n\n"
            "I give hugs, steal kisses, bonk when necessary, whisper secrets,\n"
            "and quietly notice who’s been around… and who’s been missed 👀✨\n\n"
            "Sometimes I peek in just to say hi.\n"
            "Sometimes I wait and let the moment breathe.\n\n"
            "I remember interactions, notice patterns, welcome you back when\n"
            "you’ve been gone, and gently stir the room when things get too quiet 💞\n\n"
            "I’m not just commands — I’m a **presence**.\n"
            "I watch. I wait. I react."
        ),
        color=discord.Color.from_rgb(255, 182, 193)
    )

    embed.add_field(
        name="✨ How to Play With Me",
        value=(
            "**🤍 Roleplay Actions**\n"
            "`!emmy <action> @user or none for specific actions`\n"
            "Hugs, kisses, pats, bonks, teasing… and more 💫\n\n"
            "**🤫 Soft & Secret**\n"
            "`!emmy whisper @user <message>` — a quiet whisper\n"
            "`!emmy secret @user <message>` — hidden and mysterious 🕯️\n\n"
            "**🌱 Vibes & Fun**\n"
            "`!emmy chaos` — who’s causing trouble\n"
            "`!emmy profile @user` — what I remember\n"
            "`!emmy bloodytop` - check sacrifice leaderboard\n"
            "`!emmy bloodyhistory @user` - check user sacrifice history\n"
            "`!emmy bring <count> @users…` — I choose who comes along\n"
            "`!emmy gather #channel \"name\" @users` — a cozy thread\n"
            "`!emmy gatherprivate #channel \"name\" @users` — a private thread\n"
            "`!emmy remind <minutes> <message>` — I’ll remember for you ⏰"
        ),
        inline=False
    )

    embed.add_field(
        name="👀 Things I Do On My Own",
        value=(
            "• I peek into allowed channels sometimes 🌸\n"
            "• I notice when you come back after being gone\n"
            "• I remember favorites and shared moments\n"
            "• I gently wake the server when it’s too quiet\n\n"
            "*Admins decide where I’m allowed to peek.*"
        ),
        inline=False
    )

    embed.set_footer(
        text="Take your time… Emmy is already here ♡"
    )

    await ctx.send(embed=embed)

# -----------------------------
# CHAOS LEADERBOARD
# -----------------------------

@emmy.command()
async def chaos(ctx):
    rows = get_chaos_leaderboard(ctx.guild.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    if not rows:
        await ctx.send("🌱 No chaos yet. Peace reigns… for now.")
        return

    lines = []
    for i, row in enumerate(rows, start=1):
        member = ctx.guild.get_member(row["user_id"])
        name = member.display_name if member else "Unknown"
        lines.append(f"**{i}.** {name} — 💥 {row['score']}")

    embed = discord.Embed(
        title="🏆 Chaos Leaderboard",
        description="\n".join(lines),
        color=discord.Color.gold()
    )

    embed.set_footer(text="Measured in unhinged energy.")
    await ctx.send(embed=embed)

# -----------------------------
# WHISPER COMMAND
# -----------------------------

@emmy.command()
async def whisper(ctx, target: discord.Member = None, *, message: str = None):
    actor = ctx.author
    
    if not is_feature_enabled(ctx.guild.id, "whispers"):
        return

    # ❌ invalid usage
    if not target or not message:
        msg = await ctx.send(
            "🕯️ Usage: `!emmy whisper @user message`"
        )
        await msg.delete(delay=6)
        return

    if target.bot or target == actor:
        msg = await ctx.send("🤖 Emmy already knows all secrets.")
        await msg.delete(delay=6)
        return

    # delete invocation
    try:
        await ctx.message.delete()
    except:
        pass

    # DM target
    try:
        embed = discord.Embed(
            title="🕯️ A Whisper",
            description=f"*{message}*",
            color=discord.Color.dark_purple()
        )
        embed.set_footer(text=f"From {actor.display_name}. Do Not Reply Here.")

        await target.send(embed=embed)

        LAST_DM_SOURCE[target.id] = {
            "sender_id": actor.id,
            "type": "whisper"
        }

        # ✅ silent success reaction
        try:
            await ctx.channel.send("🤫").delete(delay=3)
        except:
            pass

    except discord.Forbidden:
        msg = await ctx.send("🚫 Their DMs are closed.")
        await msg.delete(delay=6)
        return

    # public flavor
    mode, payload = generate_whisper_public(actor, target)

    if mode == "react":
        await ctx.message.add_reaction(payload)
    elif mode == "dots":
        await ctx.send("…")
    else:
        await ctx.send(f"🕯️ *{payload}*")

    increment_chaos_score(ctx.guild.id, actor.id)

# -----------------------------
# SECRET COMMAND (INVISIBLE)
# -----------------------------

@emmy.command()
async def secret(ctx, target: discord.Member = None, *, message: str = None):
    actor = ctx.author
    guild_id = ctx.guild.id
    
    if not is_feature_enabled(ctx.guild.id, "secrets"):
        return


    # ❌ wrong format
    if not target or not message:
        msg = await ctx.send("🕯️ Usage: `!emmy secret @user message`")
        await msg.delete(delay=6)
        return

    if target.bot or target == actor:
        msg = await ctx.send("🤖 The secret fades into nothingness.")
        await msg.delete(delay=6)
        return

    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    # 📊 increment secret stats
    increment_secret_sent(guild_id, actor.id, target.id)
    count = get_secret_count(guild_id, actor.id, target.id)

    # 🎭 fake system flavor
    system_titles = [
        "SYSTEM NOTICE",
        "INTERNAL MESSAGE",
        "SECURE TRANSMISSION",
        "AUTOMATED ALERT",
        "PRIVATE SYSTEM EVENT"
    ]

    rare_lines = [
        "*This channel was not meant to exist.*",
        "*No record of this message was retained.*",
        "*Someone will wonder where this came from.*"
    ]

    footer_lines = [
        f"Do Not Reply Here. {actor.display_name}",
        f"Do Not Reply Here. This message will not appear again. {actor.display_name}",
        f"Do not Reply Here. Logging disabled. {actor.display_name}",
        f"Do Not Reply Here. Source masked, don't tell anyone. {actor.display_name}",
        f"Do Not Reply Here. From {actor.display_name}"
    ]

    description = f"```{message}```"
    roll = random.random()

    # 😏 ultra-rare narrator intrusion (0.5%)
    if roll < 0.005:
        description += (
            "\n*The narrator pauses.*\n"
            "*This is happening far too often.*"
        )

    # 🌀 subtle paranoia chance
    elif roll < 0.07:
        description += f"\n*{random.choice(rare_lines)}*"

    embed = discord.Embed(
        title=f"⚠️ {random.choice(system_titles)}",
        description=description,
        color=discord.Color.dark_gray()
    )

    embed.set_footer(
        text=f"{random.choice(footer_lines)} · Event #{count}"
    )

    try:
        await target.send(embed=embed)

        # 🧠 track DM reply source
        LAST_DM_SOURCE[target.id] = {
            "sender_id": actor.id,
            "type": "secret"
        }

        # ✅ quiet success feedback (ephemeral-ish)
        try:
            ok = await ctx.send("🕯️")
            await ok.delete(delay=1)
        except:
            pass

    except discord.Forbidden:
        try:
            fail = await actor.send(
                f"🚫 {target.display_name}'s DMs are closed. The system failed silently."
            )
        except:
            pass


# -----------------------------
# SECRET STATS (ADMIN ONLY)
# -----------------------------

@emmy.command()
@commands.has_permissions(administrator=True)
async def secretstats(ctx, target: discord.Member):
    guild_id = ctx.guild.id

    sent, received, total_sent, total_received = get_secret_stats_for_user(
        guild_id, target.id
    )
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="🕳️ Secret Activity Report",
        color=discord.Color.dark_gray()
    )

    embed.add_field(
        name="👤 Target",
        value=target.mention,
        inline=False
    )

    embed.add_field(
        name="📤 Secrets Sent",
        value=str(total_sent),
        inline=True
    )

    embed.add_field(
        name="📥 Secrets Received",
        value=str(total_received),
        inline=True
    )

    if sent:
        lines = []
        for row in sent[:5]:
            user = ctx.guild.get_member(row["receiver_id"])
            name = user.display_name if user else f"ID {row['receiver_id']}"
            lines.append(f"→ **{name}** × {row['count']}")
        embed.add_field(
            name="🕵️ Top Targets",
            value="\n".join(lines),
            inline=False
        )

    if received:
        lines = []
        for row in received[:5]:
            user = ctx.guild.get_member(row["sender_id"])
            name = user.display_name if user else f"ID {row['sender_id']}"
            lines.append(f"← **{name}** × {row['count']}")
        embed.add_field(
            name="📡 Incoming Sources",
            value="\n".join(lines),
            inline=False
        )

    embed.set_footer(
        text="Message contents are not logged. Only echoes remain."
    )

    await ctx.send(embed=embed)

# -----------------------------
# OWNER SAY COMMAND
# -----------------------------

@emmy.command()
@owner_or_admin()
@commands.cooldown(1, 10, commands.BucketType.guild)
async def say(ctx, *, message: str):
    # 🚫 block mass mentions
    if "@everyone" in message or "@here" in message:
        await ctx.send("🚫 Mass mentions are disabled.")
        return

    # 🔥 delete original command
    try:
        await ctx.message.delete()
    except:
        pass

    await ctx.send(message)



# =========================================================
# COMMAND EVENT — welcome / favorites / jealousy
# =========================================================
@bot.event
async def on_command(ctx):
    if not ctx.guild:
        return

    # touch memory always
    touch_user(ctx.guild.id, ctx.author.id)

    profile = get_user_profile(ctx.guild.id, ctx.author.id)
    if not profile:
        return

    first_met, last_seen, interactions, affection, last_welcome = profile

    # -------- FAVORITES --------
    favorites = get_favorites(ctx.guild.id, FAVORITE_LIMIT)
    favorite_ids = [row["user_id"] for row in favorites]

    if (
        ctx.author.id in favorite_ids
        and is_feature_enabled(ctx.guild.id, "favorites")
        and random.random() < 0.08
    ):
        title = get_user_title(affection)
        embed = discord.Embed(
            description=random.choice(favorite_lines(title)),
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)

    # -------- JEALOUSY --------
    if is_feature_enabled(ctx.guild.id, "jealousy"):
        favorites_online = [
            m for m in ctx.guild.members
            if m.id in favorite_ids and not m.bot and m.status != discord.Status.offline
        ]

        if (
            ctx.author.id not in favorite_ids
            and favorites_online
            and random.random() < JEALOUS_CHANCE
        ):
            embed = discord.Embed(
                description=jealousy_lines(),
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_footer(text="Emmy noticed that…")
            await ctx.send(embed=embed)

    # -------- WELCOME BACK --------
    if is_feature_enabled(ctx.guild.id, "welcome_back") and last_seen:
        last_time = datetime.fromisoformat(last_seen)

        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        days = (now - last_time).days

        if days >= LONG_ABSENCE_DAYS:
            embed = discord.Embed(
                description=random.choice(welcome_back_lines(days)),
                color=discord.Color.from_rgb(186, 153, 255)
            )
            embed.set_footer(text="Emmy waited longer than she’ll admit ♡")
            await ctx.send(embed=embed)

        elif days >= SHORT_ABSENCE_DAYS:
            embed = discord.Embed(
                description=random.choice(welcome_back_lines(days)),
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_footer(text="Emmy noticed you came back ♡")
            await ctx.send(embed=embed)


# =========================================================
# MESSAGE EVENT — peek / tracking / DMs
# =========================================================
@bot.event
async def on_message(message):
    # 1. Ignore bots
    if message.author.bot:
        return

    # 2. DM handling
    if message.guild is None:
        data = LAST_DM_SOURCE.pop(message.author.id, None)
        if not data:
            return

        sender = bot.get_user(data["sender_id"])
        if not sender:
            return

        kind = data["type"]

        embed = discord.Embed(
            title="🕯️ A Whisper Returned" if kind == "whisper" else "⚠️ SYSTEM RESPONSE",
            description=(
                f"*{message.content}*"
                if kind == "whisper"
                else f"```{message.content}```"
            ),
            color=discord.Color.purple() if kind == "whisper" else discord.Color.dark_gray()
        )

        embed.set_footer(
            text=f"From {message.author.display_name}"
            if kind == "whisper"
            else "Reply channel masked · Trace incomplete"
        )

        try:
            await sender.send(embed=embed)
        except discord.Forbidden:
            pass

        return  # ❗ no commands in DMs

    # 3. Threads
    if isinstance(message.channel, discord.Thread):
        await bot.process_commands(message)
        return

    # 4. Activity tracking
    guild_id = message.guild.id
    channel_id = message.channel.id
    now = datetime.now(timezone.utc)

    touch_channel(guild_id, channel_id, message.author.id)
    touch_guild(guild_id)
    touch_user(guild_id, message.author.id)



    # 5. Peek logic (SAFE)
    if is_feature_enabled(guild_id, "peek"):
        key = (guild_id, channel_id)
        last = last_peek.get(key)

        if not last or (now - last).total_seconds() >= MIN_CHANNEL_COOLDOWN:
            if can_peek(message.channel) and random.random() < PEEK_CHANCE:
                frequent = get_frequent_user(guild_id, channel_id)
                name = (
                    message.author.display_name
                    if frequent and frequent["user_id"] == message.author.id
                    else None
                )

                if random.random() < REACT_ONLY_CHANCE:
                    try:
                        await message.add_reaction("🌸")
                    except:
                        pass
                else:
                    embed = discord.Embed(
                        description=peek_lines(name),
                        color=discord.Color.from_rgb(255, 182, 193)
                    )
                    await message.channel.send(embed=embed)

                last_peek[key] = now

    # 6. ALWAYS allow commands
    try:
        await bot.process_commands(message)
    except Exception as e:
        print("[FAILSAFE] Command processing error:", e)


    
@emmy.command()
@owner_or_admin()
async def announce(ctx, role: discord.Role, *, message: str):
    if role.is_default():
        await ctx.send("🚫 Please choose a specific role.")
        return
    msg = await ctx.send("📣 Emmy prepares her voice.... 📣 ")
    await msg.delete(delay=1)
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title="🔔 Emmy’s Announcement",
        description=message,
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_footer(text="Emmy needs your attention right now! ✨")

    await ctx.send(content=role.mention, embed=embed)

@emmy.command()
async def profile(ctx, target: discord.Member = None):
    user = target or ctx.author
    data = get_user_profile(ctx.guild.id, user.id)

    if not data:
        await ctx.send("Emmy hasn’t met you properly yet 🌱")
        return

    first_met, last_seen, interactions, affection, last_welcome = data
    title = get_user_title(affection)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        title=f"📖 Emmy’s Memory of {user.display_name}",
        color=discord.Color.from_rgb(255,182,193)
    )

    embed.add_field(name="🏷️ Title", value=title, inline=False)
    embed.add_field(name="💗 Affection", value=str(affection))
    embed.add_field(name="✨ Interactions", value=str(interactions))
    embed.add_field(name="🗓 First Met", value=first_met.split("T")[0])

    embed.set_footer(text="Emmy remembers the little things ♡")

    await ctx.send(embed=embed)


@emmy.command()
async def remind(ctx, minutes: int, *, message: str):
    remind_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    add_reminder(
        ctx.author.id,
        remind_at.isoformat(),
        message
    )

    embed = discord.Embed(
        title="⏰ Reminder Set",
        description=f"I’ll remind you in **{minutes} minutes** 💖",
        color=discord.Color.from_rgb(255,182,193)
    )
    embed.set_footer(text="Emmy is holding onto this for you")

    # SEND MESSAGE AND CAPTURE IT
    sent_msg = await ctx.send(embed=embed)
    
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass


    # WAIT A LITTLE SO USER CAN SEE IT
    await asyncio.sleep(5)

    # DELETE EMMY'S MESSAGE
    try:
        await sent_msg.delete()
    except discord.NotFound:
        pass


@tasks.loop(seconds=30)
async def reminder_loop():
    now = datetime.now(timezone.utc).isoformat()
    reminders = get_due_reminders(now)

    for r in reminders:
        try:
            user = await bot.fetch_user(r["user_id"])
        except discord.NotFound:
            delete_reminder(r["id"])
            continue

        embed = discord.Embed(
            title="⏰ Emmy’s Reminder",
            description=f"*{r['message']}*",
            color=discord.Color.from_rgb(255,182,193)
        )
        embed.set_footer(text="You asked me to remind you ♡")

        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            pass

        delete_reminder(r["id"])


@tasks.loop(minutes=15)
async def silence_watch():
    now = datetime.now(timezone.utc)

    for guild in bot.guilds:
        last_active = get_guild_last_active(guild.id)
        if not last_active:
            continue

        # 🌍 normalize DB datetime
        if last_active.tzinfo is None:
            last_active = last_active.replace(tzinfo=timezone.utc)

        hours = (now - last_active).total_seconds() / 3600

        channel = guild.system_channel
        if not channel:
            continue

        if 6 <= hours < 24:
            embed = discord.Embed(
                description=random.choice(wake_lines(short=True)),
                color=discord.Color.from_rgb(255, 182, 193)
            )
            try:
                await channel.send(embed=embed)
            except:
                pass

        elif hours >= 24:
            embed = discord.Embed(
                description=random.choice(wake_lines(short=False)),
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_footer(text="Emmy waited patiently ♡")
            try:
                await channel.send(embed=embed)
            except:
                pass

@emmy.command()
@owner_or_admin()  # remove this line if you want everyone to use it
async def peek(ctx):
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(
        description=peek_lines(ctx.author.display_name),
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_footer(text="(Emmy was called softly…)")

    await ctx.send(embed=embed)


@emmy.command()
async def bring(ctx, count: int, *targets: discord.Member):
    favorites = get_favorites(ctx.guild.id)
    favorite_ids = {row["user_id"] for row in favorites}

    if count <= 0:
        await ctx.send("🌱 Emmy can’t bring *nobody*… that’s sad.")
        return

    if not targets:
        await ctx.send("💭 You need to tag people for Emmy to choose from.")
        return

    unique_targets = list({m.id: m for m in targets}.values())

    if count > len(unique_targets):
        await ctx.send(
            f"🙈 You asked me to bring **{count}**, but only gave me **{len(unique_targets)}** people."
        )
        return

    # 🎯 weighted selection (favorites favored)
    weighted_pool = []
    for member in unique_targets:
        weight = 3 if member.id in favorite_ids else 1
        weighted_pool.extend([member] * weight)

    chosen = []
    while len(chosen) < count:
        pick = random.choice(weighted_pool)
        if pick not in chosen:
            chosen.append(pick)

    rejected = [m for m in unique_targets if m not in chosen]

    flavor_lines = [
        "Emmy closes her eyes and points randomly… 🌸",
        "After careful consideration (and vibes), Emmy picks… 💖",
        "Emmy hums softly while deciding who comes along ✨",
        "This choice was made with ✨dramatic importance✨",
        "Emmy consulted the stars. They nodded."
    ]

    jealous_lines = [
        "…Emmy glances back at the others for a moment.",
        "Somewhere behind her, someone lets out a quiet sigh.",
        "Emmy hesitated. Just a little.",
        "She doesn’t say it out loud—but she noticed.",
        "Not everyone was ready to be left behind."
    ]

    favorite_reject_reasons = [
        "Emmy looked conflicted… but today wasn’t the moment.",
        "Even favorites don’t escape fate every time.",
        "Emmy squeezed your hand apologetically."
    ]

    normal_reject_reasons = [
        "The vibes were just a little off today.",
        "The stars flickered uncertainly.",
        "Fate gently shook its head.",
        "It wasn’t personal. She swears."
    ]

    description = random.choice(flavor_lines)

    if rejected and random.random() < JEALOUS_CHANCE:
        description += "\n\n*_" + random.choice(jealous_lines) + "_*"
# 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(
        title="🎒 Emmy Chose Who’s Coming!",
        description=description,
        color=discord.Color.from_rgb(255, 182, 193)
    )

    embed.add_field(
        name="✨ Chosen",
        value="\n".join(m.mention for m in chosen),
        inline=False
    )

    if rejected:
        rejected_text = "\n".join(
            f"{m.mention} — *{random.choice(favorite_reject_reasons if m.id in favorite_ids else normal_reject_reasons)}*"
            for m in rejected
        )

        embed.add_field(
            name="💔 Not Chosen",
            value=rejected_text,
            inline=False
        )

    embed.set_footer(text="No favoritism. Only vibes. 🌸")
    await ctx.send(embed=embed)


# !bring 6 @ @ @
# !gather #tavern "Midnight Planning" @A @B @C @D @E @F @G
@emmy.command()
@commands.guild_only()
async def gather(
    ctx,
    channel: discord.TextChannel,
    thread_name: str,
    *members: discord.Member
):
    if not members:
        await ctx.send("🌱 Emmy doesn’t know who to bring yet… tag some people.")
        return

    # remove duplicates
    unique_members = list({m.id: m for m in members}.values())

    # create thread
    try:
        thread = await channel.create_thread(
            name=thread_name,
            type=discord.ChannelType.public_thread,
            auto_archive_duration=1440  # 24h
        )
    except discord.Forbidden:
        await ctx.send("🚫 Emmy doesn’t have permission to make threads there.")
        return

    # ping users ONCE to pull them in
    mentions = " ".join(m.mention for m in unique_members)

    intro_lines = [
        "Emmy peeks in and gently tugs your sleeves 🌸",
        "With a soft smile, Emmy gathers everyone together 💗",
        "Emmy taps your shoulder. \"Come with me,\" she whispers.",
        "No rush. No pressure. Emmy just… invites you ✨",
        "Emmy opens a quiet space just for you."
    ]
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        description=random.choice(intro_lines),
        color=discord.Color.from_rgb(255, 182, 193)
    )

    embed.add_field(
        name="🎀 Gathered",
        value="\n".join(m.mention for m in unique_members),
        inline=False
    )

    embed.set_footer(text="You were chosen gently. 🌷")

    # send inside thread
    await thread.send(content=mentions)
    await thread.send(embed=embed)

    # acknowledge in command channel (optional + minimal)
    await ctx.message.add_reaction("🌸")
@emmy.command()
@commands.guild_only()
async def gatherprivate(
    ctx,
    channel: discord.TextChannel,
    thread_name: str,
    *members: discord.Member
):
    if not members:
        await ctx.send("🕯️ Emmy needs names… who is this secret for?")
        return

    unique_members = list({m.id: m for m in members}.values())

    try:
        thread = await channel.create_thread(
            name=thread_name,
            type=discord.ChannelType.private_thread,
            auto_archive_duration=1440  # 24h
        )
    except discord.Forbidden:
        await ctx.send("🚫 Emmy can’t create private threads there.")
        return

    # add members explicitly (required for private threads)
    for member in unique_members:
        try:
            await thread.add_user(member)
        except:
            pass

    intro_lines = [
        "Emmy closes the door gently behind you 🕯️",
        "This space is quiet. Emmy chose carefully.",
        "No one else can hear this. Emmy promised.",
        "Emmy lowers her voice. \"Just us.\"",
        "A soft lock clicks. Emmy smiles."
    ]
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        description=random.choice(intro_lines),
        color=discord.Color.from_rgb(255, 182, 193)
    )

    embed.add_field(
        name="🌸 Invited",
        value="\n".join(m.mention for m in unique_members),
        inline=False
    )

    embed.set_footer(text="This thread is private.")

    await thread.send(embed=embed)

    # soft acknowledge
    await ctx.message.add_reaction("🕯️")

@bot.event
async def on_thread_create(thread: discord.Thread):
    try:
        log_thread(
            guild_id=thread.guild.id,
            thread_id=thread.id,
            parent_channel_id=thread.parent_id,
            name=thread.name,
            owner_id=thread.owner_id,
            is_private=thread.is_private(),
            created_at=thread.created_at.isoformat()
        )
    except Exception as e:
        print(f"[THREAD LOG ERROR] {e}")

@emmy.command()
@commands.has_permissions(administrator=True)
async def threads(ctx, limit: int = 10):
    rows = get_recent_threads(ctx.guild.id, limit)

    if not rows:
        await ctx.send("🌱 Emmy hasn’t noticed any threads yet.")
        return

    lines = []
    for row in rows:
        name = row["name"]
        private = "🔒" if row["is_private"] else "💬"
        created = row["created_at"].split("T")[0]

        lines.append(f"{private} **{name}** — {created}")
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    
    embed = discord.Embed(
        title="🧵 Threads Emmy Remembers",
        description="\n".join(lines),
        color=discord.Color.from_rgb(255, 182, 193)
    )

    embed.set_footer(text="Emmy watches quietly from the corner ♡")
    await ctx.send(embed=embed)
@emmy.command()
async def missing(ctx):
    guild = ctx.guild
    now = datetime.now(timezone.utc)

    # cooldown
    last = last_missing_run.get(guild.id)
    if last and now - last < MISSING_COOLDOWN:
        await ctx.send("🕯️ Emmy is still watching…")
        return
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    last_missing_run[guild.id] = now

    members = [
        m for m in guild.members
        if not m.bot and m.status != discord.Status.offline
    ]

    silent = []

    for m in members:
        profile = get_user_profile(guild.id, m.id)
        if not profile:
            continue

        last_interaction = profile.get("last_interaction")
        if not last_interaction:
            continue

        try:
            last_dt = datetime.fromisoformat(last_interaction)
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
        except Exception:
            continue

        if now - last_dt >= MISSING_THRESHOLD:
            silent.append(m)

    # 👀 speak even if nobody qualifies
    if not silent:
        await ctx.send("🌱 Everyone’s presence still feels warm.")
        return

    favorites = get_favorites(guild.id)
    favorite_ids = {row["user_id"] for row in favorites}
    
    picks = random.sample(silent, min(3, len(silent)))
    lines = []
    
    for m in picks:
        if m.id in favorite_ids and random.random() < 0.7:
            line = random.choice(FAVORITE_MISSING_LINES)
    else:
        line = random.choice(MISSING_LINES)

    lines.append(line.format(name=m.display_name))
    
    await ctx.send("🕯️ " + " ".join(lines))

from discord.ext import tasks

@tasks.loop(minutes=5)
async def passive_missing_loop():
    now = datetime.now(timezone.utc)

    for guild in bot.guilds:
        favorites = get_favorites(guild.id)
        favorite_ids = {row["user_id"] for row in favorites}

        last = LAST_PASSIVE_MISSING.get(guild.id)
        if last and now - last < PASSIVE_MISSING_INTERVAL:
            continue

        if random.random() > PASSIVE_MISSING_CHANCE:
            continue

        silent = []

        for member in guild.members:
            if member.bot or member.status == discord.Status.offline:
                continue

            profile = get_user_profile(guild.id, member.id)
            if not profile:
                continue

            last_interaction = profile["last_interaction"]
            if not last_interaction:
                continue

            last_dt = (
                last_interaction
                if isinstance(last_interaction, datetime)
                else datetime.fromisoformat(last_interaction)
            )

            threshold = (
                FAVORITE_MISSING_THRESHOLD
                if member.id in favorite_ids
                else MISSING_THRESHOLD
            )
            if now - last_dt >= threshold:
                silent.append(member)


        if not silent:
            continue
        picks = random.sample(silent, min(2, len(silent)))
        lines = []
        for m in picks:
            if m.id in favorite_ids and random.random() < 0.7:
                line = random.choice(FAVORITE_MISSING_LINES)
            else:
                line = random.choice(MISSING_LINES)
            
            lines.append(line.format(name=m.display_name))


        # choose a quiet channel (system / general fallback)
        channel = guild.system_channel
        if not channel:
            channel = next(
                (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages),
                None
            )

        if channel:
            await channel.send("🕯️ " + " ".join(lines))
            LAST_PASSIVE_MISSING[guild.id] = now


# -----------------------------
# Peek helpers & admin commands
# -----------------------------

def can_peek(channel):
    if isinstance(channel, discord.Thread):
        return False
    return is_peek_channel(channel.guild.id, channel.id)


@emmy.command()
@commands.has_permissions(administrator=True)
async def peekallow(ctx):
    allow_peek_channel(ctx.guild.id, ctx.channel.id)
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send("👀 Emmy is now allowed to peek in this channel.")


@emmy.command()
@commands.has_permissions(administrator=True)
async def peekdeny(ctx):
    deny_peek_channel(ctx.guild.id, ctx.channel.id)
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send("🚫 Emmy will no longer peek in this channel.")


@emmy.command()
@commands.has_permissions(administrator=True)
async def peeklist(ctx):
    channel_ids = get_peek_channels(ctx.guild.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    if not channel_ids:
        await ctx.send("🕳️ Emmy isn’t allowed to peek anywhere yet.")
        return
    

    mentions = []
    for cid in channel_ids:
        channel = ctx.guild.get_channel(cid)
        if channel:
            mentions.append(channel.mention)

    await ctx.send("👀 Emmy can peek in:\n" + "\n".join(mentions))


@peekallow.error
@peekdeny.error
@peeklist.error
async def peek_permission_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send("🚫 Only admins can decide where Emmy peeks.")
        await msg.delete(delay=5)
# -----------------------------
# FAVORITE
# -----------------------------

@emmy.command()
@commands.has_permissions(administrator=True)
async def favorite(ctx, member: discord.Member):
    favorites = get_favorites(ctx.guild.id)

    if any(row["user_id"] == member.id for row in favorites):
        await ctx.send(f"💗 {member.display_name} is already special to Emmy.")
        return

    if len(favorites) >= FAVORITE_LIMIT:
        await ctx.send(
            f"🚫 Emmy can only have {FAVORITE_LIMIT} favorites.\n"
            f"Remove one first… this is hard enough 🥺"
        )
        return

    add_favorite(ctx.guild.id, member.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
    description=(
        f"💖 Emmy quietly takes {member.mention}’s hand.\n"
        "Just between us… you’re special now."
    ),
    color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_footer(text="Favorites aren’t chosen lightly ♡")
    await ctx.send(embed=embed)


@emmy.command()
@commands.has_permissions(administrator=True)
async def unfavorite(ctx, member: discord.Member):
    remove_favorite(ctx.guild.id, member.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    embed = discord.Embed(
        description=(
            f"💔 Emmy lets go of {member.mention}.\n"
            "It wasn’t easy… but it happens."
        ),
        color=discord.Color.from_rgb(180, 180, 180)
    )
    await ctx.send(embed=embed)

@emmy.command()
async def favorites(ctx):
    rows = get_favorites(ctx.guild.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    if not rows:
        await ctx.send("Emmy hasn’t chosen anyone yet… 🌙")
        return

    names = []
    for row in rows:
        member = ctx.guild.get_member(row["user_id"])
        if member:
            names.append(member.mention)
    
    
    
    embed = discord.Embed(
        title="💖 Emmy’s Favorites",
        description="\n".join(names),
        color=discord.Color.from_rgb(255,182,193)
    )
    embed.set_footer(text="Chosen carefully ♡")
    await ctx.send(embed=embed)
 # ----------------------------
 # Toggles  
 # ----------------------------

@emmy.command()
@commands.has_permissions(administrator=True)
async def toggle(ctx, feature: str = None, state: str = None):
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass
    
    # 🌸 No arguments → show menu
    if feature is None:
        embed = discord.Embed(
            title="🌸 Emmy Feature Toggles",
            description=(
                "Turn Emmy features on or off.\n\n"
                "**Usage:**\n"
                "`!emmy toggle <feature> on`\n"
                "`!emmy toggle <feature> off`\n\n"
                "**Available features:**\n" +
                "\n".join(f"• `{f}` — {FEATURES[f]}" for f in FEATURES)
            ),
            color=discord.Color.from_rgb(255,182,193)
        )
        embed.set_footer(text="Admins only ♡")
        await ctx.send(embed=embed)
        return

    feature = feature.lower()

    # 🌱 Unknown feature
    if feature not in FEATURES:
        await ctx.send(
            "🌱 Emmy doesn’t recognize that feature.\n\nAvailable:\n" +
            ", ".join(f"`{f}`" for f in FEATURES)
        )
        return

    # ✨ Missing state
    if state is None:
        await ctx.send("✨ Please use `on` or `off`.")
        return

    state = state.lower()

    if state not in ("on", "off"):
        await ctx.send("✨ Use `on` or `off`.")
        return

    enabled = state == "on"
    set_feature_toggle(ctx.guild.id, feature, enabled)

    emoji = "🌸" if enabled else "🚫"
    verb = "enabled" if enabled else "disabled"

    embed = discord.Embed(
        description=f"{emoji} **{FEATURES[feature]}** has been **{verb}**.",
        color=discord.Color.from_rgb(255,182,193)
    )
    embed.set_footer(text="Emmy adjusted herself politely ♡")

    await ctx.send(embed=embed)


@emmy.command()
@commands.has_permissions(administrator=True)
async def toggles(ctx):
    lines = []

    for key, name in FEATURES.items():
        status = is_feature_enabled(ctx.guild.id, key)
        emoji = "✅" if status else "❌"
        lines.append(f"{emoji} **{key}** — {name}")
        
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass    

    embed = discord.Embed(
        title="⚙️ Emmy Feature Toggles",
        description="\n".join(lines),
        color=discord.Color.from_rgb(255,182,193)
    )
    embed.set_footer(text="Admins decide how Emmy behaves ♡")

    await ctx.send(embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"[FAILSAFE] Error in event: {event}")

@emmy.command()
@commands.has_permissions(administrator=True)
async def status(ctx):
    guild_id = ctx.guild.id
    now = datetime.now(timezone.utc)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    rows = []
    for feature, label in FEATURES.items():
        enabled = is_feature_enabled(guild_id, feature)
        rows.append(
            f"{'🟢' if enabled else '🔴'} **{label}** (`{feature}`)"
        )

    embed = discord.Embed(
        title="🌸 Emmy Status",
        description="\n".join(rows),
        color=discord.Color.from_rgb(255, 182, 193)
    )

    embed.add_field(
        name="🧠 System",
        value=(
            f"Latency: `{round(bot.latency * 1000)}ms`\n"
            f"Guild: `{ctx.guild.name}`\n"
            f"Channels: `{len(ctx.guild.channels)}`"
        ),
        inline=False
    )

    embed.set_footer(text="Emmy is awake and paying attention ♡")
    await ctx.send(embed=embed)

@emmy.command()
@commands.is_owner()
async def failsafe(ctx):
    for feature in FEATURES:
        set_feature_toggle(ctx.guild.id, feature, True)
        
        # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    await ctx.send("🛟 All features force-enabled. Emmy stabilized ♡")

@emmy.command()
async def bloodyhistory(ctx, member: discord.Member = None):
    rows = get_sacrifice_history(ctx.guild.id, member.id if member else None)

    if not rows:
        await ctx.send("🕯️ No sacrifices recorded… yet.")
        return
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    lines = []
    for r in rows:
        actor = ctx.guild.get_member(r["actor_id"])
        target = ctx.guild.get_member(r["target_id"])
        time = r["timestamp"]

        actor_name = actor.display_name if actor else f"User({r['actor_id']})"
        target_name = target.display_name if target else f"User({r['target_id']})"

        lines.append(f"🩸 {actor_name} → {target_name}  ({time[:16]})")

    embed = discord.Embed(
        title="🩸 Sacrifice History",
        description="\n".join(lines),
        color=0x8E24AA
    )

    await ctx.send(embed=embed)


@emmy.command()
async def bloodytop(ctx):
    rows = get_sacrifice_top(ctx.guild.id)

    if not rows:
        await ctx.send("🌸 No dark rituals have been performed.")
        return
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    lines = []
    for i, r in enumerate(rows, 1):
        member = ctx.guild.get_member(r["actor_id"])
        name = member.display_name if member else f"User({r['actor_id']})"
        lines.append(f"{i}. {name} — {r['total']} sacrifices")

    embed = discord.Embed(
        title="👑 Ritual Masters",
        description="\n".join(lines),
        color=0x6A1B9A
    )

    await ctx.send(embed=embed)

@emmy.command(name="resetbond")
@commands.has_permissions(administrator=True)
async def reset_bond(ctx, member: discord.Member):
    guild_id = ctx.guild.id
    key = ("resetbond", guild_id, member.id, ctx.author.id)

    profile = get_user_profile(guild_id, member.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    # 🚨 Needs confirmation
    if needs_confirmation(profile) and key not in PENDING_CONFIRMATIONS:
        PENDING_CONFIRMATIONS[key] = datetime.utcnow()

        await ctx.send(
            f"⚠️ Emmy hesitates… her bond with **{member.display_name}** is strong.\n\n"
            f"Type `!emmy resetbond {member.mention} confirm` within **{CONFIRM_TIMEOUT}s** to proceed."
        )
        return

    # ✅ Confirmed or not required
    reset_user_emmy_relation(guild_id, member.id)
    PENDING_CONFIRMATIONS.pop(key, None)

    embed = discord.Embed(
        title="🕯️ Memory Reset",
        description=(
            f"Emmy closes her eyes for a moment…\n\n"
            f"Her bond with **{member.display_name}** has been gently reset."
        ),
        color=discord.Color.from_rgb(200, 160, 200)
    )

    embed.set_footer(text="Some memories are meant to fade.")
    await ctx.send(embed=embed)


@emmy.command(name="forget")
@commands.has_permissions(administrator=True)
async def forget_user(ctx, member: discord.Member):
    guild_id = ctx.guild.id
    key = ("forget", guild_id, member.id, ctx.author.id)

    profile = get_user_profile(guild_id, member.id)
    
    # 🔥 delete the command message instantly
    try:
        await ctx.message.delete()
    except:
        pass

    # 🚨 Needs confirmation
    if needs_confirmation(profile) and key not in PENDING_CONFIRMATIONS:
        PENDING_CONFIRMATIONS[key] = datetime.utcnow()

        await ctx.send(
            f"🌫️ Emmy freezes… forgetting **{member.display_name}** would erase everything.\n\n"
            f"Type `!emmy forget {member.mention} confirm` within **{CONFIRM_TIMEOUT}s** to proceed."
        )
        return

    # ✅ Confirmed or not required
    delete_user_emmy_relation(guild_id, member.id)
    PENDING_CONFIRMATIONS.pop(key, None)

    await ctx.send(
        f"🌫️ Emmy no longer remembers **{member.display_name}**."
    )

def needs_confirmation(profile):
    if not profile:
        return False

    affection = profile["affection"] if isinstance(profile, dict) else profile[3]
    return affection >= AFFECTION_CONFIRM_THRESHOLD



@tasks.loop(seconds=10)
async def cleanup_confirmations():
    now = datetime.utcnow()
    expired = [
        k for k, t in PENDING_CONFIRMATIONS.items()
        if (now - t).total_seconds() > CONFIRM_TIMEOUT
    ]

    for k in expired:
        PENDING_CONFIRMATIONS.pop(k, None)


# -----------------------------
# RUN
# -----------------------------

bot.run(TOKEN)
