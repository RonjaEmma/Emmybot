from rp_assets import RP_ACTIONS, generate_rp, make_rp_embed
import discord
from discord.ext import commands
class EmmyRP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        for action in RP_ACTIONS.keys():
            self.register_rp_command(action)

    def register_rp_command(self, action_name):
        async def _rp(ctx, target: discord.Member = None):
            print(f"RP command triggered: {action_name}")

            actor = ctx.author
            guild_id = ctx.guild.id

            payload = generate_rp(action_name, actor, target, 0, 0)

            embed = make_rp_embed(
                payload,
                actor=actor,
                target=target,
                action=action_name
            )

            await ctx.send(embed=embed)

        _rp.__name__ = action_name
        self.bot.add_command(commands.Command(_rp))
