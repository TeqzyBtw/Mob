from ast import parse
import os
from datetime import datetime, timedelta
import datetime
import humanfriendly
from webserver import keep_alive
import nextcord
from nextcord.ext import commands, activities
from nextcord.ui import Button, View
import asyncio
import random
import time
import wavelink
import aiohttp
from io import BytesIO

class MakeLinkBtn(nextcord.ui.View):
  def __init__(self, link:str):
    super().__init__()
    self.add_item(nextcord.ui.Button(label="Join Game!", url=f"{link}"))

class Dropdown(nextcord.ui.Select):
  def __init__(self):
    selectOptions=[
      nextcord.SelectOption(label="UI", description="Sends A List Of UI Commands", emoji="<:emoji_25:934036179404333056>"),
      nextcord.SelectOption(label="Moderation", description="Sends A List Of Moderation Commands", emoji="<:emoji_18:933834042078539817>"),
      nextcord.SelectOption(label="Other", description="Sends A List Of Other Commands", emoji="<:emoji_26:934036203903287356>")
    ]
    super().__init__(placeholder="Please Choose What You Need Help With", min_values=1, max_values=1, options=selectOptions)
  async def callback(self, interaction: nextcord.Interaction):
    if self.values[0] == "Moderation":
      em = nextcord.Embed(title="<:emoji_18:933834042078539817> Moderation Commands List <:emoji_18:933834042078539817>", description="%ban: Bans The Mentioned User\n%kick: Kicks The Mentioned User\n%unban: Unbans The Mentioned Person(Use ID)\n%purge: Purges The Wanted Amount Of Messages\n%timeout: Times The Mentioned Person Out\n%untimeout: Removes The Timeout From The Mentioned Person", color=0xff1100)
      return await interaction.response.send_message(embed=em)
    if self.values[0] == "UI":
      emb = nextcord.Embed(title="<:emoji_25:934036179404333056> UI Commands <:emoji_25:934036179404333056>", description="%whois: Gives The Mentioned User's Information\n%invite: Gives The Link In Order To Invite Mob To Your Server\n%ping: Returns Mob's Current Latency", color=0x07ff03)
      return await interaction.response.send_message(embed=emb)
    if self.values[0] == "Other":
      embe = nextcord.Embed(title="<:emoji_26:934036203903287356> Other Commands <:emoji_26:934036203903287356>", description="%play: Plays The Selected Game In The Specified Voice Channel", color=0xfff203)
      return await interaction.response.send_message(embed=embe)

class DropdownView(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(Dropdown())

client = commands.Bot(command_prefix = "%")

@client.event
async def on_message(message):
  if f"{message.author.display_name}" == f"[AFK] {message.author.name}":
    await message.author.edit(nick=f"{message.author.name}")
    await message.reply("hey buddy, welcome back, i removed your afk")
  if "@[AFK]" in message.content:
    await message.reply.send("User's AFK Please No Bother")
  await client.process_commands(message)

client.remove_command("help")

@client.command()
async def steal(ctx, url:str, *, name):
  guild = ctx.guild
  async with aiohttp.ClientSession() as ses:
    async with ses.get(url) as r:
      try:
        imgOrGif = BytesIO(await r.read())
        bValue = imgOrGif.getvalue()
        if r.status in range(200, 299):
          emoji = await guild.create_custom_emoji(image=bValue, name=name)
          em = nextcord.Embed(title="<a:emoji_2:933815752220377098>: Success!", description=f"Successfully Added The Emoji With The Name: {name}")
          await ctx.send(embed=em)
          await ses.close()
      except nextcord.HTTPException:
        await ctx.send("Emoji's Size Is More Than The Maximum")

@client.command()
async def help(ctx):
  view = DropdownView()
  e = nextcord.Embed(title=f"Hey {ctx.author.name}", description="What Do You Need Help With?", color=0x03ffea)
  await ctx.send(embed=e, view=view)

@client.command()
async def info(ctx):
  e = nextcord.Embed(title="Copyright©")

@client.group(invoke_without_command=True)
async def play(ctx):
  return

@play.command()
async def sketch(ctx, channel: nextcord.VoiceChannel=None):
  if channel == None:
    return await ctx.send("Please Specify A Channel To Join/Create A Game")
  try:
    invite_link = await channel.create_activity_invite(activities.Activity.sketch)
  except nextcord.HTTPExeption:
    return await ctx.send("Please Mention A Voice Channel To Join And Create A Game In")
  em = nextcord.Embed(title="Sketch Game", description=f"{ctx.author.mention} Created A Game In {channel.mention}")
  em.add_field(name="What Is Sketch Game?", value="Its A Game Like Skribble Where A Player Draws Something And Someone Else Has To Guess It.")
  await ctx.send(embed=em, view=MakeLinkBtn(invite_link))

@play.command()
async def chess(ctx, channel: nextcord.VoiceChannel=None):
  if channel == None:
    return await ctx.send("Please Specify A Channel To Join/Create A Game")
  try:
    invite_link = await channel.create_activity_invite(activities.Activity.chess)
  except nextcord.HTTPExeption:
    return await ctx.send("Please Mention A Voice Channel To Join And Create A Game In")
  em = nextcord.Embed(title="Chess", description=f"{ctx.author.mention} Created A Game In {channel.mention}")
  em.add_field(name="What Is Chess?", value="Its A Game Where You Have To Attack/Defend And Try To Get The Oppent's King.")
  await ctx.send(embed=em, view=MakeLinkBtn(invite_link))

@play.command()
async def poker(ctx, channel: nextcord.VoiceChannel=None):
  if channel == None:
    return await ctx.send("Please Specify A Channel To Join/Create A Game")
  try:
    invite_link = await channel.create_activity_invite(activities.Activity.poker)
  except nextcord.HTTPExeption:
    return await ctx.send("Please Mention A Voice Channel To Join And Create A Game In")
  em = nextcord.Embed(title="Poker", description=f"{ctx.author.mention} Created A Game In {channel.mention}")
  em.add_field(name="What Is Poker?", value="Its A Game Where You Have To Get More Points By Winning Hands, Play Smart.")
  await ctx.send(embed=em, view=MakeLinkBtn(invite_link))

@client.event
async def on_ready():
  await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"%help | Watching {len(client.guilds)} Servers"))
  print("Mob Is Online!")
  client.loop.create_task(node_connect())

async def node_connect():
  await client.wait_until_ready()
  await wavelink.NodePool.create_node(bot=client, host='lavalink.devz.cloud', port=443, password='mathiscool', https=True)

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
  print(f"Node {node.identifier} is ready!")

@client.command()
async def mplay(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
  if not ctx.voice_client:
    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
  elif not ctx.author.voice_client:
    return await ctx.send("Please Join A VC First")
  else:
    vc: wavelink.Player = ctx.voice_client
  vc.play(search)

@client.command(description="Shows The Client's Latency")
async def ping(ctx):
  pingy = nextcord.Embed(title=f"☑️ Pong!", description=f"Latency: {round(client.latency * 1000)}ms", color=0xe3ff0f)
  await ctx.channel.send(embed=pingy)

@client.command()
async def invite(ctx, amount=None):
        button = Button(label="Required Permissions", url="https://discord.com/oauth2/authorize?client_id=898879454078726144&scope=bot%20applications.commands&permissions=388102")
        button1 = Button(label="Administrator Permissions", url="https://discord.com/oauth2/authorize?client_id=898879454078726144&scope=bot%20applications.commands&permissions=8")
        view = View()
        view.add_item(button1)
        view.add_item(button)
        embed = nextcord.Embed(title="Add Me To Your Own Server", description="Choose My Permissions", color=0x00ff1e)
        await ctx.send(embed=embed, view=view)

@client.command()
async def gstart(ctx, mins : int, *, prize: str):
  embed = nextcord.Embed(title="New Giveaway!", description=f"Prize: {prize}", color=ctx.author.color)
  end = datetime.datetime.utcnow()+datetime.timedelta(seconds = mins*60)
  embed.add_field(name = "Ends At:", value = f"{end} UTC")
  embed.set_footer(text=f"Host: {ctx.author}, Ends {mins} minutes from now in your time!", url=ctx.author.avatar.url)
  my_msg = await ctx.send(embed=embed)
  await my_msg.add_reaction("🎉")
  await asyncio.sleep(mins)
  new_msg = await ctx.channel.fetch_message(my_msg.id)
  users = await new_msg.reactions[0].users().flatten()
  users.pop(users.index(client.user))
  winner = random.choice(users)
  await ctx.send(f"Congratulations {winner}, You Just Won {prize}!")
  

@client.command(pass_context=True)
async def afk(ctx, reason=None):
  await ctx.send(f"{ctx.author.mention} Is AFK - {reason}")
  await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def timeout(ctx, user: nextcord.Member,time=None, *, reason=None):
        time = humanfriendly.parse_timespan(time)
        await user.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
        ffff = nextcord.Embed(title=f"☑️ Timed {user.name} Out!", description=f"Reason: {reason}\nBy: {ctx.author.mention}\nTime: {time}s", color=0xff0000)
        await ctx.message.delete()
        await ctx.channel.send(embed=ffff)



@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : nextcord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.roles, overwrite=overwrite)
    await ctx.send('Channel locked.')

@client.command()
@commands.has_permissions(manage_messages=True)
async def untimeout(ctx, user: nextcord.Member=None):
        await user.edit(timeout=None)
        await ctx.message.reply(f"Successfully Removed The Timeout From {user}")

@client.command(description="Bans The Mentioned Person")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: nextcord.Member, *, reason="No reason provided"):
        if ctx.message.author.id == user.id:
          em = nextcord.Embed(title="<:Error:965657609677991976> ERROR", description="You Can't Ban Yourself", color=0xff1303)
          await ctx.send(embed=em)
        else:
          ban = nextcord.Embed(title=f"☑️ Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xff0000)
          await ctx.reply(embed=ban)
          ban1 = nextcord.Embed(title=f"❌ {user.name}!", description=f"Reason: You Got Banned For {reason}\nBanned By: {ctx.author.mention}", color=0xff0000)
          await user.send(embed=ban1)
          await user.ban(reason=reason)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.channel.send("Please Enter The Required Arguments")
  if isinstance(error, commands.UnexpectedQuoteError):
    await ctx.send("An Unexpected Error Happened, Please Try Again Or Report It As A Bug.")

@client.command(description="Unbans The Chosen Person")
@commands.has_permissions(ban_members = True)
async def unban(ctx, id: int, *, reason = None):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"☑️ Unbanned {user.name}!")

@commands.has_permissions(kick_members=True)
@client.command(description="Kicks The Mentioned Person")
async def kick(ctx, user: nextcord.Member, *, reason="No reason provided"):
        if ctx.message.author.id == user.id:
          em = nextcord.Embed(title="<:Error:965657609677991976> ERROR", description="You Can't Kick Yourself", color=0xff1303)
          await ctx.reply(embed=em)
        else:
          await user.kick(reason=reason)
          kick = nextcord.Embed(title=f"☑️ Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}", color=0xFF5733)
          await ctx.reply(embed=kick)
          kick1 = nextcord.Embed(title=f"❌ {user.name}!", description=f"Reason: You Got Kicked For {reason}\nBy: {ctx.author.mention}", color=0xFF5733)
          await user.send(embed=kick1)
          await user.kick(reason=reason)

@commands.has_permissions(manage_messages=True)
@client.command(description="Purges The Specfic Amount Of Messages In The Channel")
async def purge(ctx, amount:int):
  hoi = nextcord.Embed(title="**<:emoji_8:933817778496995368> Purging...**", color=0x00FF00)
  await ctx.channel.send(embed=hoi) 
  await ctx.channel.purge(limit=amount+2)

@client.command(description="Gives Some Information About The Chosen Person")
async def whois(ctx, member: nextcord.Member=None):
  if member==None:
    member = ctx.author
  roles = [role for role in member.roles]
  embed = nextcord.Embed(title=member.name, color=0x00FFFF, timestamp=ctx.message.created_at)
  embed.add_field(name="ID", value=member.id, inline=True)
  embed.add_field(name="Account Creation", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
  embed.add_field(name="Joined At", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
  embed.set_thumbnail(url = member.avatar.url)
  embed.add_field(name="Bot", value=member.bot, inline=False)
  embed.add_field(name=f"Roles: ({len(roles)})", value=" ".join([role.mention for role in roles]))
  embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar.url)
  await ctx.channel.send(embed=embed)

@client.command(description="Introduces itself")
async def introduction(ctx):
  hola = nextcord.Embed(title = f"Hey {ctx.author}", description = "I'm Mob", color=0x0febff)
  hola.add_field(name="‌", value="<:emoji_24:933834295053779024> A Moderation Bot Coded In Python By Teqzy", inline=False)
  hola.add_field(name="‌", value="Version 1.00 `BETA`", inline=False)
  hola.add_field(name="‌", value="Type %help To Get Started", inline=False)
  await ctx.channel.send(embed=hola)

Token = ("ODk4ODc5NDU0MDc4NzI2MTQ0.YWqoug.SFTkgia1cmHDzrV3IjzOh5IqMLU")
keep_alive()
client.run(Token, reconnect=True)
