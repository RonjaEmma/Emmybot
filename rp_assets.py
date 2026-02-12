# rp_assets.py
import random
import discord
from config import EMMY_ID
# =========================
# RP ACTION DEFINITIONS
# =========================

RP_ACTIONS = {
    "hug": {
        "emoji": "🤍",
        "color": 0xFFC0CB,
        "gifs": [
            "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
            "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3am51Y2IwdXp1MzRuZm53bm9pYzExbjdobnA3Y3JxeHBpOGlzY2xoYyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/fLv2F5rMY2YWk/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3am51Y2IwdXp1MzRuZm53bm9pYzExbjdobnA3Y3JxeHBpOGlzY2xoYyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/2A75Y6NodD38I/giphy.gif",
            "https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeW5haXJ6bDljN3ZjNXY2bGs3dGJtNGlrZWIxbXNnbDhjazN3eTV4dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/IzXiddo2twMmdmU8Lv/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeW5haXJ6bDljN3ZjNXY2bGs3dGJtNGlrZWIxbXNnbDhjazN3eTV4dyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EvYHHSntaIl5m/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bmM5Ymd1aThvbXJsNnl5Z3J2andlYXg1Zno0NjkwcXUyejRwc3o4OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5OqXb948EBkyUcnwHt/giphy.gif",
            "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjMyeHZjb2UxYWNkZjZscTg2OGI5ZHFzOWszcXE5MjkxMmN5YmFpZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IRUb7GTCaPU8E/giphy.gif",
            "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjMyeHZjb2UxYWNkZjZscTg2OGI5ZHFzOWszcXE5MjkxMmN5YmFpZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IRUb7GTCaPU8E/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MWFmcG9ybW00cmJ5Nnp4MmdycTRxeGJsa29yOWJpeWQzZ2Z4b3Z1ZCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/u9BxQbM5bxvwY/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bXdob3R2ajBuMWJkeGU1ZngzYjVoaW5ycnpnZmYydDU2NjRnbzc3byZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Lb3vIJjaSIQWA/giphy.gif",
            "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjhqYnRwNDd6OHZvcGIzb3BmMzl2eGE3cjV1cG1naHZ2ZHoxYmdpbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JLovyTOWK4cuc/giphy.gif",
        ],
        "lines": [
            "{actor} pulls {target} into a warm hug.",
            "{actor} hugs {target} tightly.",
            "Without a word, {actor} wraps {target} in a hug.",
            "For a moment, the world pauses as {actor} hugs {target}.",
        ],
        "special": [
            "✨ Embrace of Fate ✨\n{actor} and {target} share a hug that feels destined.",
        ],
        "special_chance": 0.08,
    },

    "pat": {
        "emoji": "🫳",
        "color": 0xAEDFF7,
        "gifs": [
            "https://media.giphy.com/media/4HP0ddZnNVvKU/giphy.gif",
            "https://media.giphy.com/media/L2z7dnOduqEow/giphy.gif",
            "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmxlZ2c1MnRwbGdhZ2Rpc2FpOGtpazJ6dnJ1MjV4YTd1azhheXZkOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/X42IAaDJ42pHqPllGk/giphy.gif",
            "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExazg4YWl4dDVtNXI4d2NwM2ZxNWEzNXEzdDlreWtlZWZwdjF6aXlhMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qE86wtoTSWzaSDVYix/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d3RydzF3bnMwaW54bHByeHVreTQxZTg2dGo5a3k5d3F3MGcxcmVnayZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/5tmRHwTlHAA9WkVxTU/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d3RydzF3bnMwaW54bHByeHVreTQxZTg2dGo5a3k5d3F3MGcxcmVnayZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/SSPW60F2Uul8OyRvQ0/giphy.gif",
        ],
        "lines": [
            "{actor} gently pats {target}'s head.",
            "{actor} gives {target} a comforting pat.",
        ],
    },

    "kiss": {
        "emoji": "💋",
        "color": 0xFF9AA2,
        "gifs": [
            "https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif",
            "https://media.giphy.com/media/11k3oaUjSlFR4I/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2t2Y2M2OWo0aDRvZzJ2dW1sYWEzbDY0ZGJsMGR0czRta3NhYmRheiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/W1hd3uXRIbddu/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dWF3bXFldmlza2RrYXlyc2JoNDJxY2xheWt0czc2MG9vdHFiYW94MiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YDB4EF3U6i6IM/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d3dxb2lxOWJqenoyYmVhbWdpYTN2cHd4eThjZjJydGN2anlvdjAzMSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/jR22gdcPiOLaE/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d3dxb2lxOWJqenoyYmVhbWdpYTN2cHd4eThjZjJydGN2anlvdjAzMSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/VXsUx3zjzwMhi/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3czl1czMwbTQ5Yml4NjNhanI3bzVxMGpncWdhaHdlYnN6d25zY2ZscSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/wOtkVwroA6yzK/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3czl1czMwbTQ5Yml4NjNhanI3bzVxMGpncWdhaHdlYnN6d25zY2ZscSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/11kOyLOLUxDS2k/giphy.gif",
        ],
        "lines": [
            "{actor} leans in and kisses {target}.",
            "💋 {actor} gives {target} a sweet kiss.",
            "A soft moment passes as {actor} kisses {target}.",
        ],
    },
    
    "boop": {
        "emoji": "👉👈",
        "color": 0xFFB6C1,
        "gifs": [
            "https://media.giphy.com/media/Zdg7kl9bnyqXrPH2jq/giphy.gif",
            "https://media.giphy.com/media/l0HU20BZ6LbSEITza/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW1ma29vcXIzcXYweXA3a2I3cTQ5Y3NuYmJrN2c2OTNibDFmdWdtYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/SYLvjCEtBClsS2QePl/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW1ma29vcXIzcXYweXA3a2I3cTQ5Y3NuYmJrN2c2OTNibDFmdWdtYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/fC4vvkZZNX1Tfnuxzt/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW1ma29vcXIzcXYweXA3a2I3cTQ5Y3NuYmJrN2c2OTNibDFmdWdtYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lcvjDNIJ8CS88/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMW1ma29vcXIzcXYweXA3a2I3cTQ5Y3NuYmJrN2c2OTNibDFmdWdtYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/li2guAY6z7TSK43UH3/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MWh4bHcybGNuc3dwYmRtd2NuMGtqeXZ0ODlnejlraDNoYmMycTQ4ZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XwnOjVqPIlXGM/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXR3am11cjVoZDg2YWhodjVhd3Qxbnp4YmM5OGdqZjlwM294aTBzeSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EzP85aNlqGXWo/giphy.gif",
            
            ],
        "lines": [
            "{actor} gently boops {target}'s nose.",
            "{actor} sneaks in and boops {target}!",
            "{target} gets an unexpected nose boop from {actor}.",
            "{actor} boops {target} and immediately looks proud.",
        ],
    },
    
    "bite": {
        "emoji": "🦷",
        "color": 0xFF8FAB,
        "gifs": [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGU2encyb3p5bXNpYncybjY0eTV0M3oxNzd2bXNtdG5kZWhkdTdkYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/OqQOwXiCyJAmA/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGU2encyb3p5bXNpYncybjY0eTV0M3oxNzd2bXNtdG5kZWhkdTdkYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/108wBdjDIkQZb2/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZjRrcmpyNm1pN2U1MnBvYTg0aGc0dTRqZnBxZHZmdGNqbGtyM2ZvMSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/lrMUMn9lnpaJDsvP0u/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YmpzcGI0aDlqdjVpcTRwNDJwMHRsbXk2eTRoZ3g4NjBvYmNvOWc4MCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/NVWbq9vSYf7so85wqh/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGU1MzdyNm5obHF3aXV6bDB3aTgwcmVmcmZ1ZjFoZnV4M2RqdDZuNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YW3obh7zZ4Rj2/giphy.gif",
        ],
        "lines": [
            "{actor} leans in and gives {target} a playful bite.",
            "{actor} nips at {target} before pulling away innocently.",
            "{target} gets lightly bitten by {actor}!",
            "{actor} bites {target} and pretends it wasn’t on purpose.",
        ],
    },
    
    "poke": {
        "emoji": "👉",
        "color": 0xA0E7E5,
        "gifs": [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3JnNWRiMnVyYXo4azZrbnV6azNsMDR4aW9rNDB3ODlhbm02eXYyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Vfie0DJryAde8/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3JnNWRiMnVyYXo4azZrbnV6azNsMDR4aW9rNDB3ODlhbm02eXYyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jCENc3aA4fLJm/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3JnNWRiMnVyYXo4azZrbnV6azNsMDR4aW9rNDB3ODlhbm02eXYyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/aZSMD7CpgU4Za/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3JnNWRiMnVyYXo4azZrbnV6azNsMDR4aW9rNDB3ODlhbm02eXYyZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TYAYywTcAb4Iw/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bTNmc3RjY2NoMWJ3enNpMDQzd3Fpa2ExZDF5aWxocWE5amcxOWJieiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/FdinyvXRa8zekBkcdK/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3amZneXZnYm01ZjdpMHQ5c2k5YW5ibzVyamd3YXp0cmQya203b2JybiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/pWd3gD577gOqs/giphy.gif",
            
            ],
        "lines": [
            "{actor} pokes {target}.",
            "{actor} keeps poking {target} for no reason.",
            "{target} is poked by {actor}. Rude.",
            "{actor} pokes {target} and waits for a reaction.",
       ],
    },
    "sacrifice": {
    "emoji": "🩸",
    "lines": [
        "{actor} offers {target} to unseen forces.",
        "{actor} draws a circle… {target} stands at its center.",
        "A hush falls as {actor} prepares the sacrifice of {target}.",
        "{target} feels the air grow heavy around them.",
    ],
    "special": [
        "The ground drinks deeply as {actor} completes the sacrifice of {target}.",
        "Something ancient accepts {target} — and stirs.",
        "The ritual flares violently as {target} is claimed.",
    ],
    "special_chance": 0.12,
    "gifs": [
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczUyaGlvcXE2dGFuZWprc2UxeG9xMmxuYWFpMjhldmlkcnYwa2s0biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/La3G8N3tn4nzW/giphy.gif",
        
    ],
},

    "summon": {
        "emoji": "🔮",
        "lines": [
            "✨ Reality ripples… {target} is summoned by {actor}!",
            "{actor} calls forth {target} into the scene!",
            "A magic circle glows beneath {target}.",
            "{target} feels a pull toward {actor}.",
            ],
        "special": [
            "The air fractures as {actor} drags {target} across reality.",
            "{target} arrives in a flash of unstable light.",
            ],
        "special_chance": 0.15,
        "gifs": [
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExejk5emxlM3h6OGMwOW03MXEwZ2x4eGdkNm42MTRrcDJkNmF4dWx1ZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/A2GXvZmG73hQc/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjlyb3F0OTZuNHJleXdhdzg3MzZkcGRjNWszdGQ5cHlhemhwb2FhZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/yO5URi0mbRxkev4Qmt/giphy.gif",
        "https://tenor.com/bsmzM.gif",
        ],
     },

    "bonk": {
        "emoji": "🔨",
        "color": 0xD5AAFF,
        "gifs": [
            "https://media.giphy.com/media/qs4ll1FSxKnNHeSmom/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M2NueTJ2Nndnazc1cXRmazcydWR0bndtc2RtaWdxdTF4ZnBqemI0dSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tHKW4XiwOZ25cU9yHx/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGkwYzlsaXpqNjF2aWg0ZThtb25mY3Z1ZWR4cThtOWduZDc1bHhjdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/schUjA2QKXd3NE59Yo/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cWJsdTZsbHhwc3NjeDFmMmk4aTViNnRiMWlrNXVqY2E4MGc2cmQ0cSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/R5LFtvAahcZ6WNBZzD/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3M2NueTJ2Nndnazc1cXRmazcydWR0bndtc2RtaWdxdTF4ZnBqemI0dSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/gOQauUreUyDdP2l2gT/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cWJsdTZsbHhwc3NjeDFmMmk4aTViNnRiMWlrNXVqY2E4MGc2cmQ0cSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/gsyDSxD5mpBdKftDLq/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZGhpcXFjcDE3c2t3am5maDEwb2pleW8zYTd3NDRkYW9qbGYweGgzaSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/sB4vLNDWsSZ7o4DSv6/giphy.gif",            
        ],
        "lines": [
            "Bonk! {actor} bonks {target}. Go to horny jail.",
            "{actor} bonks {target} on the head.",
        ],
    },
    
    "cry": {
        "emoji": "💧",
        "color": 0xA7C7E7,
        "gifs": [
            "https://media.giphy.com/media/ROF8OQvDmxytW/giphy.gif",
            "https://media.giphy.com/media/9Y5BbDSkSTiY8/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3emtscXp3Nnl5NXI0MG8waDFrcHUyZHBoM2dpZWZ2OWozdmx4MXliaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vudNK1LtwXTTa/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aWNjdWIwc2dnbjRjOWluNnRucDZqeGV3ZnRteWdmbHR4MmR4ano0ciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lR3pWtb80Hz22UjrYj/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Z3RncHVkaHhjbHhndTg2anlqYzh3cmh2anpsa2M3YWE0c2lqeDBqYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YyECUhkxzUTDI0I5bx/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cTBobm13MHB0ajR6N3U5aXVsbmtwOWtxdHN3OW5jNnh0c2pwMGFvdSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/L95W4wv8nnb9K/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cTBobm13MHB0ajR6N3U5aXVsbmtwOWtxdHN3OW5jNnh0c2pwMGFvdSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/OPU6wzx8JrHna/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGdxaHZuZzUwNjh1ZjRnZnl1MDE5N2RmOThlY2phNXJlNmIzbGx6NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/d2lcHJTG5Tscg/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGdxaHZuZzUwNjh1ZjRnZnl1MDE5N2RmOThlY2phNXJlNmIzbGx6NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dCwNmR9BBOzKpiBQOs/giphy.gifhttps://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGdxaHZuZzUwNjh1ZjRnZnl1MDE5N2RmOThlY2phNXJlNmIzbGx6NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/dCwNmR9BBOzKpiBQOs/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGdxaHZuZzUwNjh1ZjRnZnl1MDE5N2RmOThlY2phNXJlNmIzbGx6NyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hppWdK8gcmzXq/giphy.gif",
        ],
        "lines": [
            "{actor} breaks down and starts crying.",
            "{actor} wipes their eyes, tears still falling.",
            "{actor} can’t hold it in anymore.",
            "{actor} quietly cries where everyone can see.",
            ],
        "special": [
            "Something cracks. {actor} finally lets themselves cry.",
        ],
        "special_chance": 0.07,
    },
    
    "compliment": {
        "emoji": "💐",
        "color": 0xFFD1DC,
        "gifs": [
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YWNjaDZrb2U2Y2M4aWkwNDIyN3k1aHYxa2c2OTdoOXJ3N2gzeXFxNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/EbEphCw4wMYGBAYYO8/giphy.gif",
            "https://media.giphy.com/media/l4pTdcifPZLpDjL1e/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YWNjaDZrb2U2Y2M4aWkwNDIyN3k1aHYxa2c2OTdoOXJ3N2gzeXFxNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YfSKB039u1zspUoaJp/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dDllYTFmYWkxdnAxYmI2cjJlN3JmNzJjenprdDlzN2J0NWVpcHVwZyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/RSk4bOw2ptIkAcVxK2/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dnVtZTE0c3llanJ3N2dzaWRkMXFvZWUwaG92M2k0ejYzanJjb3dkOSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xAN6q8sJ0h8r7M1kkO/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cG16eWRhNmswZnZqdHpzdXNrczU4Zm90d3c0ZTZvNHMzcnRxY25jdiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/QLwkIS74IbIM53Kz8F/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3YnU2d293cWJod2FzdzBhODl0c29qazh2MnNwcWp5cGh1ZnVsbTRxbCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/U1UpB3msYOdElFXCt1/giphy.gif",
        ],
    "lines": [
        "{actor} tells {target} they look really nice today.",
        "{actor} compliments {target} sincerely.",
        "{actor} smiles at {target} and offers a kind compliment.",
        "{actor} quietly praises {target}.",
        ],
    "special": [
        "{actor} says something so sincere it makes {target} pause.",
        ],
    "special_chance": 0.06,
    },
    
    "angry": {
    "emoji": "💢",
    "color": 0xFF6F61,
    "gifs": [
        "https://media.giphy.com/media/l1J3G5lf06vi58EIE/giphy.gif",
        "https://media.giphy.com/media/11tTNkNy1SdXGg/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cDlscWNpdnN3ZmdmenE2OWg3YXpvY2Q3ZGxuNWk5NmR4N2lqemM2MiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/qsLVENvjyRHNu/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWl6M3didmY1aHJvdGZ5MmlzNHAyNXJvN3kwc3llbGd2Z3oyazk5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TGi1zmIHpDRsrxtoPq/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWl6M3didmY1aHJvdGZ5MmlzNHAyNXJvN3kwc3llbGd2Z3oyazk5biZlcD12MV9naWZzX3NlYXJjaCZjdD1n/hJUHoFaWf4MTSTuKmK/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MjM4OGRpZXlrbWtxd3Q1bndpY2hhNGxsN3Z3aGNtNjJxYzJqODQ1MCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/L0mL3oDfLol2z6KcmR/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NDRpMTUxdDE1Y2ZuNDIyYThzdWk5Mnpqd3FsN2g0MzRnMDVlcm4wNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/tZiLOffTNGoak/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cXM4OGc3czQ5cnlvbHdqd3E5ODM5dHZiaTFxZWN0Z3VueTVrNmJxMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9jVAv94PRzPoc/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cXM4OGc3czQ5cnlvbHdqd3E5ODM5dHZiaTFxZWN0Z3VueTVrNmJxMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26uf1EUQzKKGcIhJS/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dTF4bGtpd2Vhdnl0YW1kNjRoZGNzZjM1ZXM5YzdwMXp4Z3N2azlxeiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/11WojR0GhjExlm/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ZXV1ZGt4b2xsem0xb3RhdHRkbmEwbWxiYWRhYmUweWtoOTRyOW9lNSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/EPcvhM28ER9XW/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cHFqNzJiNGhvOHJleG8wenc1bmxwZDV5am5kYWc3YWxrbWtraDE5ZiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/ySVKduoNNFoRy/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cHFqNzJiNGhvOHJleG8wenc1bmxwZDV5am5kYWc3YWxrbWtraDE5ZiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/1Bf2QoS5z1laU/giphy.gif",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWp1d2VzODF2OWZtY2Y3NzdxZHc5OG56dHo1YWNldHBvOHI4anZkZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FO8mbXfBehV0A/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExendkN293MGt3NWl2NzhnaGJwM3FoODgxZnh2a280ampodnkzemRweCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WoF3yfYupTt8mHc7va/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3am93M2t0NTJndW9wcG11anE5emJxZTg1ejE5bWY1OGJra2MxZDhudyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/RYOsjgBkb40E/giphy.gif",
    ],
    "lines": [
        "{actor} looks visibly angry.",
        "{actor} clenches their fists, clearly upset.",
        "{actor} snaps, unable to hide their anger.",
        "{actor} glares in {target}'s direction.",
    ],
    "special": [
        "{actor} explodes — this has been building for a while.",
    ],
    "special_chance": 0.05,
},
    
    "attention": {
    "emoji": "🥺",
    "color": 0xE6C7FF,
    "gifs": [
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd21lamhvYWkxdzFpbnh2cmR0bWlsb2JtbTVrNHJ5M2Fwb2tpbmpyOSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0HlDEWlv0m8kCMfe/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczZsY2M2YjZmOXBiMzFxdDBlNmZnN3loYmZiY2QzbGFieWVpdm52YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/j2M6NZyAq6FLyOFx1U/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczZsY2M2YjZmOXBiMzFxdDBlNmZnN3loYmZiY2QzbGFieWVpdm52YyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/57SRq2RRLAjIYwXwMJ/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Mzl1MDdtNnRhMGZuaGhvb3pudmszc3JmYTVnNW1zaGJqMXB6NDdpbCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/PcwpnqpwAfRK/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OXJpOXIxN3FibmZwYXM5NnBkMTh4Y29mcTB0cGhqcGtqaWUyM2VhOSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/xT0GqEWuqNxdVEWxlm/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bWpvd2VmYTA2bnhubXUyaDdtcjU2enplZWxydGdnODV1NnljZjViayZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/PhFXIlPu4ieKoAQV4V/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODRmOTh2cDg5MzhsbngzZzgydGl4NHFmYnU2ZGU2YXR6MGl3a3llaCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Y4z9olnoVl5QI/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDVkbnk3ajA2ajVwY3VqeGc2ZHdyb2FwbTNkNGd5czdpNWNydDluYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4pk6ba2LUEMi4/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3MzliaGZ0M3VpdWFzd3h3a2dpdGR1ZjJyZW8yaHByZWxubzJxY3c0cSZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/beFz7ODP7OD8Q/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cXNnY3cwYXRhNHNyY2VkaGNpc3A1NGN0cmplM3U3N211eTB5ZHoxYyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/FGbEffWs9la1O/giphy.gif",
    ],
    "lines": [
        "{actor} sniffles loudly and keeps glancing around.",
        "{actor} cries just enough to be noticed.",
        "{actor} makes sure everyone knows they’re upset.",
        "{actor} looks miserable, hoping someone will say something.",
    ],
    "special": [
        "{actor} cries dramatically, peeking to see who reacts.",
    ],
    "special_chance": 0.1,
},
    
    "bratty": {
    "emoji": "😈",
    "color": 0xC77DFF,
    "gifs": [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXFkMzJoZmp2aGM0NnhyY2I1dm94ZzZsb2h5bDI2amZwZmIxcmZpaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wiFxDY1R6cKje/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3ejQ1Z3hlMTNrcGZ6MWRiNHd3dmNmeTA2YmIwYjV3czJzNWdmc2Z3YyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/l0Iy33dWjmywkCnNS/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3dzJxcm5ndmxxenE3dzUzNTZ6MnVod20xa3g2ejZmMHlqdTBhbG4wbyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/d0JPBhiwCm6Kk/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cGlpNmkzb2wzczYzeGdlcGRjZmNxNHBtaWc5ajRmOXJyc3huNWh5aCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/3LrvHf5chL7RS/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bjJka3c0dDR5bXI1b21zcGNjMDM2ejAyeGRmeG1rM2NtZms0djhqeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RCWahfIC5IPew/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzYzcXEyMmM2amVjcHRpdHczb2tpaGRsd2xsM2NicWh0dW91ODc4cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WJKA6tktuSYAKMhz8H/giphy.gifhttps://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzYzcXEyMmM2amVjcHRpdHczb2tpaGRsd2xsM2NicWh0dW91ODc4cyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WJKA6tktuSYAKMhz8H/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OW03bGo5OGFzM2NzM2U1OTZuNjFwd242eDY5amRobzI0ajV1ejJqcCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/7yMTKcMaO3NgaXZTMV/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Y3JqdThhOGExMmVvamV2bnBqcW1lNmVtcTM0em1rMjkxNXRpNmdxdSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9xqgSer64HJ113ZByT/giphy.gif",
        "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHRsMXVwdDV5NWVrOXp6MTgwczA0MTU5Zm95Z24xdHNkaDN2MjMwNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qLErpwsfLyY6RSTJlJ/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3am93M2t0NTJndW9wcG11anE5emJxZTg1ejE5bWY1OGJra2MxZDhudyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/jTU09JLRaYCt2/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3Yzg1ejRhNzJ3d3ZpeXVoYmV6NWloMGl2anN2NHVvMHUxNnRuaTRraCZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/PivShcAVhKARq/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cDlscWNpdnN3ZmdmenE2OWg3YXpvY2Q3ZGxuNWk5NmR4N2lqemM2MiZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/iMEOxEJP7CJBS/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3cXNnY3cwYXRhNHNyY2VkaGNpc3A1NGN0cmplM3U3N211eTB5ZHoxYyZlcD12MV9naWZzX3JlbGF0ZWQmY3Q9Zw/z7o1ZJk2dWhPZVurqw/giphy.gif",
    ],
    "lines": [
        "{actor} sticks their tongue out at {target}.",
        "{actor} acts deliberately bratty.",
        "{actor} smirks, clearly misbehaving on purpose.",
        "{actor} crosses their arms and refuses to cooperate.",
    ],
    "special": [
        "{actor} is being *extra* bratty today, and they know it.",
    ],
    "special_chance": 0.08,
},

    "slap": {
        "emoji": "💥",
        "color": 0xFF6961,
        "gifs": [
            "https://media.giphy.com/media/jLeyZWgtwgr2U/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjRjYmxhbXpnOXJma2M2cjlxbzc5ZGk5YTE1ZXB6eGU1bmdhZjNiaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Zau0yrl17uzdK/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjRjYmxhbXpnOXJma2M2cjlxbzc5ZGk5YTE1ZXB6eGU1bmdhZjNiaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Gf3AUz3eBNbTW/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjRjYmxhbXpnOXJma2M2cjlxbzc5ZGk5YTE1ZXB6eGU1bmdhZjNiaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4R6EMXhNPz5WsJFEta/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjRjYmxhbXpnOXJma2M2cjlxbzc5ZGk5YTE1ZXB6eGU1bmdhZjNiaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/mJWDiMyXuWG8U/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NzE0ZWZnZjlidThoaTBpeTgxOHhvenZ6Z2RmZXB1cG0yY3g0c2pnYSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RXGNsyRb1hDJm/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NjNrd2h2ZGhqazdjZHRxY3BncnVsd2F3MjB0OGRlaW5panNnOXBmYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/2A5oOQdXOxCfjPaP9l/giphy.gif",
            
        ],
        "lines": [
            "{actor} slaps {target} without hesitation!",
            "{target} gets absolutely slapped by {actor}.",
        ],
    },
}

ACTION_TARGET_MODE = {
    "attention": "self",

    "hug": "target",
    "kiss": "target",
    "bite": "target",
    "pat": "target",
    "summon": "target",
    "bonk": "target",
    "boop": "target",
    "bratty": "target",
    "compliment": "target",
    "poke": "target",
    "slap": "target",
    
    "angry": "optional",
    "cry": "optional",
}

# =========================
# SOFT / SPICY VARIANTS
# =========================

SOFT_SPICY_LINES = {
    "hug": [
        "{actor} holds {target} just a little longer.",
        "{target} melts into {actor}'s embrace.",
    ],
    "kiss": [
        "{actor}'s kiss lingers softly.",
        "{actor} kisses {target} slowly.",
    ],
}
SOFT_SPICY_LINES.update({
    "compliment": [
        "{actor} lowers their voice and compliments {target} softly.",
        "{actor} gives {target} a look full of warmth.",
    ],
    "bratty": [
        "{actor} acts bratty but clearly wants attention.",
        "{actor} misbehaves, watching {target} closely.",
    ],
})

def get_soft_spicy(action):
    return SOFT_SPICY_LINES.get(action)



# =========================
# INTERNAL STATE
# =========================

_LAST_LINES = {}
RARE_CHANCE = 0.005

RARE_LINES = [
    "The universe pauses, reconsidering its choices.",
    "Somewhere, fate sighs quietly.",
]

ESCALATION_LINES = {
    10: "The scene is getting a little out of hand.",
    20: "This has escalated beyond reason.",
    35: "Chaos reigns.",
}

MUTUAL_ESCALATION_LINES = {
    15: "There is a shared understanding here.",
    30: "Both sides have embraced the chaos.",
}


# =========================
# CORE RP GENERATOR
# =========================

def generate_rp(action, actor, target, count=0, mutual_count=0):
    data = RP_ACTIONS[action]

    # 🎲 Rare meta override
    if random.random() < RARE_CHANCE:
        return {
            "emoji": "✨",
            "text": random.choice(RARE_LINES),
            "gif": None,
            "mode": "rare",
        }

    # 🌟 Special action override (per-action)
    if "special" in data and random.random() < data.get("special_chance", 0):
        special_line = random.choice(data["special"]).format(
            actor=actor.mention,
            target=target.mention,
        )
        return {
            "emoji": data["emoji"],
            "text": special_line,
            "gif": random.choice(data["gifs"]),
            "special": True,
        }

    # 🧠 Prevent same-line spam
    key = (actor.id, action)
    lines = data["lines"].copy()

    last = _LAST_LINES.get(key)
    if last in lines and len(lines) > 1:
        lines.remove(last)

    # 🎭 Pick base line
    line = random.choice(lines)

    # 💞 Soft / spicy override (uses get_soft_spicy)
    soft_lines = get_soft_spicy(action)
    if soft_lines and mutual_count >= 5 and random.random() < 0.15:
        line = random.choice(soft_lines)

    # Remember final line
    _LAST_LINES[key] = line

    # 📝 Format text
    text = line.format(
        actor=actor.mention,
        target=target.mention,
    )

    # 🔥 Escalation
    escalation = None
    for threshold, esc in ESCALATION_LINES.items():
        if count >= threshold:
            escalation = esc

    # 🫶 Mutual escalation
    mutual = None
    for threshold, esc in MUTUAL_ESCALATION_LINES.items():
        if mutual_count >= threshold:
            mutual = esc

    return {
        "emoji": data["emoji"],
        "text": text,
        "gif": random.choice(data["gifs"]),
        "escalation": escalation,
        "mutual": mutual,
    }



# =========================
# EMBED BUILDERS
# =========================

def make_rp_embed(payload, actor=None, target=None, action=None):
    embed = discord.Embed(
        description=f"{payload['emoji']} **{payload['text']}**",
        color=discord.Color.random()
    )

    if payload.get("gif"):
        embed.set_image(url=payload["gif"])

    if payload.get("escalation"):
        embed.add_field(
            name="⚠️",
            value=payload["escalation"],
            inline=False
        )

    if payload.get("mutual"):
        embed.add_field(
            name="💫",
            value=payload["mutual"],
            inline=False
        )

    # 🌸 Emmy reacts HERE
    if target and target.id == EMMY_ID:
        reaction = generate_emmy_reaction(action)
        if reaction:
            embed.add_field(
                name="🌸 Emmy",
                value=reaction,
                inline=False
            )

    embed.set_footer(text="✦ Roleplay Mode ✦")
    return embed





# =========================
# WHISPER (PUBLIC)
# =========================

WHISPER_PUBLIC_LINES = [
    "{actor} leans in and whispers something to {target}.",
    "{actor} murmurs softly to {target}.",
]

def generate_whisper_public(actor, target):
    roll = random.random()

    if roll < 0.15:
        return "react", random.choice(["🤫", "🕯️"])

    if roll < 0.25:
        return "dots", "…"

    line = random.choice(WHISPER_PUBLIC_LINES)
    return "text", line.format(actor=actor.mention, target=target.mention)

def welcome_back_lines(days):
    if days >= 7:
        return [
            "It’s been a while… Emmy kept your place warm 🌙",
            "Oh— there you are. Emmy never forgot 💞"
        ]
    return [
        "Oh! You’re back already~ 💖",
        "Emmy smiles when she sees you again 🌸"
    ]

# =========================
# UTILITIES
# =========================
def get_rp_actions():
    """Returns all RP action names."""
    return list(RP_ACTIONS.keys())


def favorite_lines(title):
    return random.choice([
        f"Emmy leans closer to her {title} 💖",
        f"Emmy smiles — her {title} is here ✨",
        f"Special treatment for a {title}, obviously 🐣"
    ])

def jealousy_lines():
    return random.choice([
        "Hey… Emmy noticed that 😗",
        "Hmm? You’re being popular today…",
        "Emmy looks away. Just a little.",
        "Emmy pretends not to mind. Pretends."
    ])

def peek_lines(name=None):
    base = [
        "Emmy peeks in quietly 🌸",
        "Just passing by… ✨",
        "Emmy was nearby and noticed 👀",
        "Soft footsteps… Emmy’s here 💕",
        "A small glance from the doorway 🌙",
        "Emmy lingers for just a second 🌷",
        "Someone felt the room shift… that was Emmy",
        "Emmy drifts through, unseen but present 🌸",
        "A quiet presence brushes past 💭",
        "Emmy pauses, listening 🌙",
    ]

    personal = [
        f"Emmy peeks in — oh, hi {name} 💖",
        f"{name}’s here… Emmy smiles 🌸",
        f"Emmy notices {name} and stays a moment ✨",
        f"{name} caught Emmy’s attention 💕",
        f"Emmy glances toward {name} and nods softly 🌷",
        f"{name} feels familiar… Emmy lingers 🌙",
    ]

    return random.choice(personal if name and random.random() < 0.5 else base)


def wake_lines(short=True):
    if short:
        return [
            "It’s been quiet for a while… 🌸",
            "Emmy stretches and looks around 👀",
            "A soft sigh breaks the silence 🌙",
            "Emmy blinks awake, listening ✨",
            "Something stirs… Emmy is awake 💕",
            "Emmy peeks at the empty channels 🌷",
            "A gentle hum signals Emmy’s return 🎶",
        ]
    return [
        "It’s been a whole day… Emmy gently opens the curtains 🌅",
        "A quiet server… Emmy hums softly 🎶",
        "Time passed slowly here… Emmy notices 🌙",
        "Dust settled. Emmy brushes it away 🌸",
        "The day turned over while Emmy watched silently 🌄",
        "Emmy wakes to a still room and waits ✨",
        "Morning light reaches even quiet places 🌅",
        "Emmy stretches after a long silence 💭",
    ]

MISSING_LINES = [
    "I haven’t felt {name} around today.",
    "It’s quieter without {name}.",
    "Someone usually leaves a trace. {name} didn’t.",
    "{name} hasn’t crossed my path today.",
    "I keep expecting {name} to speak.",
    "{name} usually passes through by now.",
    "The room remembers {name}.",
]
SOFT_REASONS = [
    "You feel steady.",
    "You stayed.",
    "You didn’t try to be noticed.",
    "You feel safe to choose.",
    "You listen more than you speak.",
    "You hesitated.",
    "You didn’t leave.",
]

CHAOS_REASONS = [
    "You look like trouble.",
    "Something bad always follows you.",
    "This will be more interesting with you.",
    "You feel unlucky.",
    "Fate nudged me.",
    "You look doomed. Respectfully.",
]

OBSERVANT_REASONS = [
    "You always linger.",
    "You leave traces.",
    "You’ve done this before.",
    "You’re predictable.",
    "You’re not.",
    "You hesitate last.",
]

JEALOUS_REASONS = [  # RARE
    "You ignored me.",
    "You’ve been busy with others.",
    "You thought I wouldn’t notice.",
    "You didn’t look my way earlier.",
]


#Emmy reactions

EMMY_NEGATIVE_REACTIONS = {
    "cry": [
        "Emmy flinches, tears welling up.",
        "She turns away, clearly hurt.",
        "Emmy curls in on herself, trembling."
    ],
    "fight": [
        "Emmy snaps back, eyes burning.",
        "She doesn’t take it quietly this time.",
        "Emmy retaliates without hesitation."
    ],
    "freeze": [
        "Emmy freezes, saying nothing.",
        "She goes eerily still.",
    ]
}

EMMY_POSITIVE_REACTIONS = {
    "hug": [
        "Emmy hugs back, holding on a little tighter.",
        "She melts into the embrace.",
    ],
    "soft": [
        "Emmy smiles softly.",
        "Her shoulders relax."
    ]
}

EMMY_NEUTRAL_REACTIONS = {
    "oh": [
        "Yes, I'm here.",
        "I'm always here, watching",
        "Alright let's play!",
        "Im bored...are you bored too...",
        "You have my attention, {actor} ",
    ]
}

EMMY_COMFORT_REACTIONS = {
    "there": [
        "Let it out, it's okay, I'm here for you.",
        "What happened, {actor}?",
        "Who made you cry like this? hand me their name."
    ]
}

NEGATIVE_ACTIONS = {
    "slap", "bite", "angry", "bonk", "bratty", 
}

POSITIVE_ACTIONS = {
    "hug", "kiss", "boop", "pat", "compliment",
}
NEUTRAL_ACTIONS = {
    "attention", "poke", 
}
COMFORT_ACTIONS = {
    "cry",
}
def generate_emmy_reaction(action):
    if action in NEGATIVE_ACTIONS:
        roll = random.random()

        if roll < 0.4:
            return random.choice(EMMY_NEGATIVE_REACTIONS["cry"])
        elif roll < 0.7:
            return random.choice(EMMY_NEGATIVE_REACTIONS["freeze"])
        else:
            return random.choice(EMMY_NEGATIVE_REACTIONS["fight"])

    if action in POSITIVE_ACTIONS:
        if random.random() < 0.7:
            return random.choice(EMMY_POSITIVE_REACTIONS["hug"])
        return random.choice(EMMY_POSITIVE_REACTIONS["soft"])
    if action in NEUTRAL_ACTIONS:
        if random.random() < 0.7:
            return random.choice(EMMY_NEUTRAL_REACTIONS["oh"])
    if action in COMFORT_ACTIONS:
        if random.random() < 0.7:
            return random.choice(EMMY_COMFORT_REACTIONS["there"])

    return None
