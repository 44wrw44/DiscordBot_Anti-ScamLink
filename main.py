import discord
from discord.ext import commands
import vt
import re

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_IDS = [123456789012345678, 234567890123456789]

EXEMPT_DOMAINS = ["example.com", "trustedsite.org"]

client = vt.Client('YOUR_VIRUSTOTAL_API_KEY')


def is_scam_link(url):
    domain_pattern = r"https?://(?:www\.)?([^/]+)"
    domain_match = re.match(domain_pattern, url)

    if domain_match:
        domain = domain_match.group(1)
        if domain in EXEMPT_DOMAINS:
            return False

    try:
        analysis = client.scan_url(url)
        report = client.get_object(f"/urls/{analysis.scan_id}")
        if report.last_analysis_stats['malicious'] > 0:
            return True
    except Exception as e:
        print(f"Ошибка при проверке ссылки: {e}")
    return False


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in CHANNEL_IDS:
        urls = re.findall(r'(https?://\S+)', message.content)
        for url in urls:
            if is_scam_link(url):
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, ваше сообщение удалено, так как оно содержит подозрительную ссылку.")
                return

    await bot.process_commands(message)


@bot.command()
async def check_link(ctx, link: str):
    if is_scam_link(link):
        await ctx.send(f'Ссылка {link} - скам.')
    else:
        await ctx.send(f'Ссылка {link} - не скам.')


bot.run('YOUR_BOT_TOKEN')


@bot.event
async def on_close():
    client.close()