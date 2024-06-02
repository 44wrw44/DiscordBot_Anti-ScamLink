import discord
from discord.ext import commands
import vt
import re
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_IDS = [1234567890123345679, 1234567890123345670]

EXEMPT_DOMAINS = ["youtube.com", "discord.gg", "sovagroup.one", "tenor.com"]

VT_TOKEN = "YOUR_VIRUSTOTAL_API_KEY"

LOG_CHANNEL_ID = 1234567890123345678

SCAM_LINKS_FILE = "scam_links.txt"
SAFE_LINKS_FILE = "safe_links.txt"

client = vt.Client(VT_TOKEN)


if os.path.exists(SCAM_LINKS_FILE):
    with open(SCAM_LINKS_FILE, "r") as f:
        known_scam_links = set(f.read().splitlines())
else:
    known_scam_links = set()

if os.path.exists(SAFE_LINKS_FILE):
    with open(SAFE_LINKS_FILE, "r") as f:
        known_safe_links = set(f.read().splitlines())
else:
    known_safe_links = set()


async def is_scam_link(url):
    domain_pattern = r"https?://(?:www\.)?([^/]+)"
    domain_match = re.match(domain_pattern, url)

    if domain_match:
        domain = domain_match.group(1)
        if domain in EXEMPT_DOMAINS:
            return False

    if url in known_scam_links:
        return True
    if url in known_safe_links:
        return False

    try:
        async with vt.Client(VT_TOKEN) as client:
            url_id = vt.url_id(url)
            report = await client.get_object_async(f"/urls/{url_id}")
            if report.last_analysis_stats['malicious'] > 0:
                known_scam_links.add(url)
                with open(SCAM_LINKS_FILE, "a") as f:
                    f.write(f"{url}\n")
                return True
            else:
                known_safe_links.add(url)
                with open(SAFE_LINKS_FILE, "a") as f:
                    f.write(f"{url}\n")
                return False
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
        urls = re.findall(r'(https?://[^\s]+)', message.content)
        for url in urls:
            print(f"Проверка ссылок от {message.author}: {urls}")
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if await is_scam_link(url):
                await message.delete()
                try:
                    await message.author.send(
                        f"Ваше сообщение на канале <#{message.channel.id}> было удалено, так как оно содержит "
                        f"подозрительную ссылку. Содержание:"
                        f"```{message.content}```")
                except discord.Forbidden:
                    print(f"Не удалось отправить личное сообщение пользователю {message.author}")
                await log_channel.send(f"Удалено сообщение от {message.author.mention} в канале <#{message.channel.id}> с подозрительной ссылкой: {url}")
                return
            else:
                await log_channel.send(f"Проверено сообщение от {message.author.mention} в канале <#{message.channel.id}> с ссылкой: {url} - без подозрений")

    await bot.process_commands(message)


@bot.command()
async def check_link(ctx, link: str):
    if await is_scam_link(link):
        await ctx.send(f'Ссылка {link} является скам.')
    else:
        await ctx.send(f'Ссылка {link} не является скам.')


@bot.event
async def on_close():
    await client.close_async()


bot.run('YOUR_BOT_TOKEN')
