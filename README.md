# DiscordBot_Anti-ScamLink
Дискорд бот на python для проверки ссылок в сообщения.

## Инструкция:
1. Установите id каналов, в которых будет вестись проверка. (**CHANNEL_IDS**) 
2. Установите ключ [VirusTotal](https://www.virustotal.com/gui/user/). (**VT_TOKEN**)
3. Установите [токен бота](https://discord.com/developers/applications). (**YOUR_BOT_TOKEN**)
4. Установите разрешённые ссылки, точнее домен, так как он проверяет домен, но не что потом. (**EXEMPT_DOMAINS**)
5. Установите канал логирования. (**LOG_CHANNEL_ID**)

## Зависимости:
1. discord - Взаимодействие с дискордом.
2. vt - API VirusTotal.
3. re - обычные выражения.
4. os - для записи в файлы.

## Установка:
- `apt install git python3 -y`
- `pip install discord vt-py`
- `git clone https://github.com/44wrw44/DiscordBot_Anti-ScamLink.git`
- `python3 main.py`