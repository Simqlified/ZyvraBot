import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="~", intents=discord.Intents.all())
from typing import Optional

@bot.event
async def on_ready():
    print("The bot is now working!")

@bot.command()
async def hello(ctx):
    username = ctx.message.author.name
    await ctx.reply(f"Whats Up?")


#Moderation Commands!
    #Kick
@bot.command()
async def kick(ctx, member: discord.Member=None):
    if not member:
        await ctx.reply("You need to mention a member to kick, dumbass.")
        return

    if ctx.message.author.guild_permissions.kick_members:
        if member.id == ctx.guild.owner_id:
            await ctx.reply("You can't kick the server owner, dumbass.")
        elif member.top_role >= ctx.author.top_role:
            await ctx.reply("You can't kick someone with a higher role than you, dumbass.")
        else:
            await member.kick(reason="::middle_finger_tone5:")
            await ctx.reply(f"{member.mention} has been kicked! :middle_finger_tone5:")
    else:
        await ctx.reply("You don't have the permission to kick members, dumbass.")
    #Ban
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        # Check if the user is missing the "Ban Members" permission
        if 'ban_members' in [p[0] for p in ctx.author.guild_permissions]:
            # User is missing the "Ban Members" permission
            await ctx.reply("You do not have permission to ban members.")
        else:
            # User is missing a different permission
            await ctx.reply("You do not have permission to run this command.")
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member is None:
        await ctx.reply("Please mention a member to ban.")
        return

    if member == ctx.guild.owner:
        await ctx.reply("You cannot ban the owner of the server.")
        return

    try:
        await member.ban(reason="Banned by {}".format(ctx.author.name))
        await ctx.reply("{} has been banned.".format(member.display_name))
    except discord.Forbidden:
        await ctx.reply("I do not have permissions to ban {}.".format(member.display_name))
    except discord.HTTPException:
        await ctx.reply("An error occurred while attempting to ban {}.".format(member.display_name))
    except commands.MissingPermissions as e:
        print(f"Missing permissions: {e}")
        await ctx.reply("You don't have permission to do that.")


    #Unban
@bot.command()
async def unban(ctx, user=None):
    if user is None:
        return await ctx.reply("Please provide a user to unban.")
    try:
        if not ctx.author.guild_permissions.ban_members:
            raise commands.MissingPermissions(["ban_members"])
        user_obj = await commands.UserConverter().convert(ctx, user)
    except commands.errors.MissingPermissions as e:
        perms = ", ".join(e.missing_perms)
        return await ctx.reply(f"You are missing {perms} permission(s) to run this command.")
    except commands.errors.UserNotFound:
        return await ctx.reply("The user does not exist.")
    async for ban in ctx.guild.bans():
        if ban.user.id == user_obj.id:
            await ctx.guild.unban(user_obj)
            await ctx.reply(f"{user_obj} has been unbanned.")
            return

    await ctx.reply("This user is not banned.")

@bot.command()
async def dicksize(ctx, name):
    if name.lower() == "ray" or name.lower() == "rayhn":
        response = "25 centimeter"
        await ctx.reply(f"The size of {name} is {response}", mention_author=False)
    else:
        await ctx.reply(f"No dick size found for {name}")
    
    #Utility
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    embed = discord.Embed(title=f"{member.name}'s avatar", color=member.color)
    embed.set_author(name=member, icon_url=member.avatar.url)
    embed.set_image(url=member.avatar.url)

    await ctx.send(embed=embed)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I couldn't find that user. Please specify a valid user.")
    else:
        raise error

@bot.command()
async def av(ctx):
    await avatar(ctx)


avatar.hidden = True

@bot.command()
async def poll(ctx, poll_type, question, *options):
    if poll_type.lower() == "choice":
        if len(options) > 10:
            await ctx.send("Error: Too many options. Please limit to 10.")
            return
        if len(options) < 2:
            await ctx.send("Error: Not enough options. Please provide at least 2.")
            return
        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        for i, option in enumerate(options):
            embed.add_field(name=f"{reactions[i]} {option}", value="", inline=False)
        poll_msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_msg.add_reaction(reactions[i])
    elif poll_type.lower() == "yesno":
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        embed.add_field(name="✅ Yes", value="", inline=False)
        embed.add_field(name="❌ No", value="", inline=False)
        poll_msg = await ctx.send(embed=embed)
        await poll_msg.add_reaction('✅')
        await poll_msg.add_reaction('❌')
    else:
        await ctx.send("Error: Invalid poll type. Please choose either 'choice' or 'yesno'.")

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    members = guild.members
    humans = len([member for member in members if not member.bot])
    bots = len([member for member in members if member.bot])
    total_members = guild.member_count
    creation_date = guild.created_at.strftime("%B %d, %Y")
    icon_url = guild.icon.url
    owner = guild.owner
    roles = guild.roles
    num_roles = len(roles)
    channels = guild.channels
    num_channels = len(channels)
    voice_channels = guild.voice_channels
    num_voice_channels = len(voice_channels)
    embed = discord.Embed(title=f"{guild.name} Server Information", color=discord.Color.blue())
    embed.set_thumbnail(url=icon_url)
    embed.add_field(name="・Created On", value=creation_date, inline=False)
    embed.add_field(name="・Owner", value=owner, inline=False)
    embed.add_field(name="・Members", value=f"👤 {humans}  |  🤖 {bots}  |  👥 {total_members}", inline=True) 
    embed.add_field(name="・Roles", value=f"🔺{num_roles}", inline=True)
    embed.add_field(name="・Channels", value=f"⌨️ {num_channels}  |  🎙️ {num_voice_channels}", inline=True)
    await ctx.send(embed=embed)

@serverinfo.error
async def serverinfo_handler(ctx, error):
    print(error)

bot.run("MTA5NTEwOTAwNjI5NDUyODE1MA.G9bcN4.IQDbIoyOHTQNv43a-t10zVPow_ZF82Hr4qKbYo")