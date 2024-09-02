import discord
from redbot.core import commands, checks
from redbot.core.bot import Red

class TransferOwnership(commands.Cog):
    """
    Transfers server ownership from the bot to a specified member.
    """

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command()
    @checks.is_owner()  # Only the bot owner can use this command
    @commands.guild_only()  # This command can only be used in a server
    async def transferownership(self, ctx: commands.Context, new_owner: discord.Member):
        """
        Transfers server ownership from the bot to the specified member.

        This command is highly sensitive and should only be used when absolutely necessary.

        Arguments:
            new_owner: The member to transfer ownership to.
        """

        if not ctx.guild.owner == self.bot.user:
            await ctx.send("I am not the owner of this server.")
            return

        await ctx.send(f"Are you absolutely sure you want to transfer ownership of this server to {new_owner.mention}? This action is irreversible. Type `yes` to confirm.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            confirmation = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("Ownership transfer timed out. No action was taken.")
            return

        if confirmation.content.lower() != 'yes':
            await ctx.send("Ownership transfer cancelled.")
            return

        try:
            await ctx.guild.edit(owner=new_owner)
            await ctx.send(f"Server ownership has been transferred to {new_owner.mention}.")
        except discord.Forbidden:
            await ctx.send("I don't have the necessary permissions to transfer ownership.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while transferring ownership: {e}")