import asyncio
import random
from telethon import TelegramClient, events
from telethon import Button
from telethon.tl.types import InputReportReasonSpam
import os
from re import compile as compile_link
from os import listdir, path as ospath

# Ваши параметры APIp
api_id = 22075720  # Замените на свой api_id
api_hash = '381b83e04ceaf4a328a99ac789d52f02'  # Замените на свой api_hash
bot_token = '8046436338:AAFZsT2Lme0DgJjO6h7I_UGFePt3wE-V_h4'  # Ваш токен бота

# Список API идентификаторов и хешей для проверки сессий
api_credentials = [
  {'api_id': '28234677', 'api_hash': 'e7c47bee153e7c54524d4086c650027d', 'phone': '+79950652058'},
  {'api_id': '21360694', 'api_hash': 'dacae7f3be65e55128fb85e2e6721c88', 'phone': '+79690173115'},
  {'api_id': '20249962', 'api_hash': '5b4df1012c71f7fc2baa086b726e551d', 'phone': '+447402594195'},
  {'api_id': '27293299', 'api_hash': '2325d766046e3b1637f5b0fa22c562eb', 'phone': '+79102533246'},
  {'api_id': '26158693', 'api_hash': '180fd68a14d5a1422dcf81bf8f4ffe37', 'phone': '+79507915811'},
  {'api_id': '23037915', 'api_hash': '50f06f5b2223586fde0d1379ea91ebc7', 'phone': '+79921870852'},
  {'api_id': '29512095', 'api_hash': '0b29a7d42fff002856b9bed64f7ec919', 'phone': '+79910057650'},
  {'api_id': '25055016', 'api_hash': '25edf5b7becebe91a2d61fe8d9d9931b', 'phone': '+79921802240'},
  {'api_id': '21156147', 'api_hash': '90408de329b27f7dd411dff3e601acc6', 'phone': '+79013929006'},
  {'api_id': '29840977', 'api_hash': 'e20b6a9fd01cc9055de0a88a183a030b', 'phone': '+79528625019'},
  {'api_id': '29412963', 'api_hash': '3e37e1d05422db9426aa85e617b441ea', 'phone': '+79105272669'},
  {'api_id': '23140129', 'api_hash': '431e5e839aecf4abdce22d7663acffa7', 'phone': '+79105275170'},
  {'api_id': '28712009', 'api_hash': '94fde6f4d57e3451649331da114783a1', 'phone': '+79264293540'},
  {'api_id': '20003929', 'api_hash': 'd437fb59350c51fc77277356f70abb1a', 'phone': '+79019703042'},
  {'api_id': '25908772', 'api_hash': 'd7cc217ade2f50ab1ab8d8187a223e89', 'phone': '+79105281438'},
  {'api_id': '23907100', 'api_hash': '225c7759435456bafda67f2729318980', 'phone': '+79921944641'},
  {'api_id': '27757367', 'api_hash': '0c3c400d46b47bcf2c98d182fd3a7fd7', 'phone': '+79382974095'},
  {'api_id': '23474941', 'api_hash': 'd1b527d8924a799e3556f48045975d21', 'phone': '+79999729141'},
  {'api_id': '26055857', 'api_hash': '75bf9ca9dccaabe27f3a391183875e1e', 'phone': '+79266067940'},
  {'api_id': '26462182', 'api_hash': '001b0d73e563bfb912d48eeee38dce61', 'phone': '+79267887980'},
  {'api_id': '25481303', 'api_hash': '7b4496634fc1aa143b254aa7e4c50c09', 'phone': '+79522670786'},
  {'api_id': '26304685', 'api_hash': 'b52e8360adc6904c98ff6ee8b7b7cb08', 'phone': '+79104336003'},
  {'api_id': '27019945', 'api_hash': '3b42e8a707d42a9ac244b99c294f5340', 'phone': '+79850353412'},
  {'api_id': '20097016', 'api_hash': '18962b749f03a5db10264cbb7b13f5af', 'phone': '+79251650129'},
  {'api_id': '25639241', 'api_hash': '4be85e762c4a24167094b5f6e8517eda', 'phone': '+79167741290'}
]


# Идентификаторы администраторов и владельца
admins_id = []
owner_id = 7166220534

# Путь к сессиям
path_to_sessions = ospath.join(ospath.dirname(__file__), "sessions")
if not os.path.exists(path_to_sessions):
    os.makedirs(path_to_sessions)

# Загружаем администраторов из файла
def load_admins():
    global admins_id
    try:
        with open("adm.txt", "r") as file:
            admins_id = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        admins_id = []

# Создаем клиента бота
bot = TelegramClient(f'{path_to_sessions}/bot', api_id, api_hash)

async def main():
    await bot.start(bot_token=bot_token)
    load_admins()
    print("Бот запущен. Ожидание сообщений...")
    await validate_sessions()
    await bot.run_until_disconnected()

# Проверка подписки
async def check_subscription(user_id):
    try:
        with open("sub.txt", "r") as file:
            subscriptions = file.readlines()
            for subscription in subscriptions:
                if subscription.strip():
                    sub_id, _ = subscription.strip().split(", ")
                    if str(user_id) == sub_id:
                        return True
    except FileNotFoundError:
        return False
    return False

# Проверка вайт-листа
async def check_whitelist(user_id):
    try:
        with open("whitelist.txt", "r") as file:
            whitelisted_users = file.readlines()
            for whitelisted_user_id in whitelisted_users:
                if str(user_id) == whitelisted_user_id.strip():
                    return True
    except FileNotFoundError:
        return False
    return False

# Валидация сессий
async def validate_sessions():
    valid_sessions = 0
    invalid_sessions = []

    files = listdir(path_to_sessions)
    sessions = [s for s in files if s.endswith(".session") and s != 'bot.session']

    for session in sessions:
        session_path = ospath.join(path_to_sessions, session)

        api_cred = random.choice(api_credentials)  # Случайный api_id и api_hash для проверки
        api_id = api_cred['api_id']
        api_hash = api_cred['api_hash']

        try:
            async with TelegramClient(session_path, api_id, api_hash) as client:
                await client.start()
                valid_sessions += 1
                print(f"Сессия {session} валидна.")
        except Exception as e:
            invalid_sessions.append(session)
            print(f"Недействительная сессия: {session}. Ошибка: {e}")
            os.remove(session_path)

    if invalid_sessions:
        await bot.send_message(owner_id, f"🛠 Удалены {len(invalid_sessions)} невалидные сессии.\n"
                                           f"Осталось валидных сессий: {valid_sessions}.")
    else:
        await bot.send_message(owner_id, f"✅ Все сессии валидны. Осталось валидных сессий: {valid_sessions}.")

# Получение случайной сессии
def get_random_session():
    files = listdir(path_to_sessions)
    sessions = [s for s in files if s.endswith(".session") and s != 'bot.session']
    return random.choice(sessions) if sessions else None

# Отправка жалобы
async def report_message(link):
    message_link_pattern = compile_link(r'https://t.me/(?P<username_or_chat>.+)/(?P<message_id>\d+)')
    match = message_link_pattern.search(link)

    if not match:
        return 0, 0

    chat = match.group("username_or_chat")
    message_id = int(match.group("message_id"))

    session = get_random_session()
    if session is None:
        print("Нет доступных сессий.")
        return 0, 0

    session_path = ospath.join(path_to_sessions, session)

    api_cred = random.choice(api_credentials)  # Случайный api_id и api_hash для отправки
    api_id = api_cred['api_id']
    api_hash = api_cred['api_hash']

    async with TelegramClient(session_path, api_id, api_hash) as client:
        if not await client.is_user_authorized():
            print(f"Сессия {session} не авторизована.")
            return 0, 0

        if await check_whitelist(chat):
            print(f"Атака невозможна, пользователь {chat} находится в вайт-листе.")
            return 0, 0
        
        try:
            entity = await client.get_entity(chat)
            await client(functions.messages.ReportRequest(
                peer=entity,
                id=[message_id],
                reason=InputReportReasonSpam(),
                message="В этом сообщении наблюдается спам."
            ))
            print("Жалоба отправлена.")
            return 1, 0  # Успешная отправка
        except Exception as e:
            print(f"Ошибка при отправке жалобы через сессию {session}: {e}")
            return 0, 1  # Ошибка при отправке

# Обработка команд
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    first_name = event.sender.first_name or "Пользователь"
    user_id = event.sender.id

    buttons = [
        [Button.url("🎲 Руководство", "https://telegra.ph/Re1xx-snos-12-07")],
        [Button.url("💸 Купить подписку", "https://t.me@O00OO0O0OO0000O")],
        [Button.inline("💎 New snos", b"new_snos")],
        [Button.inline("📋 Профиль", b"profile")]
    ]

    await event.respond(
        f"🌟 • Приветствую {first_name}.\n🌗 • Твое айди: {user_id}.\n\nДля продолжения пользуйся кнопками ниже.",
        buttons=buttons
    )

@bot.on(events.CallbackQuery(data=b'new_snos'))
async def new_snos(event):
    user_id = event.sender.id
    if not await check_subscription(user_id):
        await event.respond("🥌 У вас отсутствует подписка, приобретите ее у!")
        return

    await event.respond("💫 Пришлите ссылку для отправки жалоб!")

@bot.on(events.CallbackQuery(data=b'profile'))
async def profile(event):
    user_id = event.sender.id
    first_name = event.sender.first_name or "Пользователь"
    username = f"@{event.sender.username}" if event.sender.username else "Нет юзернейма"
    subscription_status = "Есть" if await check_subscription(user_id) else "Отсутствует"
    whitelist_status = "Есть" if await check_whitelist(user_id) else "Отсутствует"

    profile_info = (
        f"📱 Ваш профиль\n\n"
        f"🗣 Имя: {first_name}\n"
        f"🗄 Данные: id {user_id} / {username}\n"
        f"💎 Подписка: {subscription_status}\n"
        f"📄 Вайт-лист: {whitelist_status}"
    )
    await event.respond(profile_info)
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def handle_message(event):
    if 'https://t.me/' in event.message.message:
        link = event.message.message
        user_id = event.sender.id

        if not await check_subscription(user_id):
            await event.respond("🥌 У вас отсутствует подписка, пожалуйста, приобретите ее, чтобы отправлять жалобы.")
            return

        await event.respond('❄️ Отправка жалоб началась...')
        
        successful_reports, failed_reports = await report_message(link)

        response_text = f'🫧 Все жалобы отправлены!\n\nУспешно: {successful_reports}\nНеуспешные: {failed_reports}'
        await event.respond(response_text)
    else:
        pass

@bot.on(events.NewMessage(pattern='/give_sub'))
async def give_subscription(event):
    user_id = event.sender.id
    if user_id != owner_id and user_id not in admins_id:
        await event.respond("У вас нет прав для выдачи подписок.")
        return
    
    try:
        parts = event.message.message.split(" ")
        if len(parts) != 3:
            await event.respond("Неправильный формат. Используйте: /give_sub (ID Пользователя) (Количество дней)")
            return
        
        target_user_id = int(parts[1])  
        days = int(parts[2]) 
        
        if days == 0:  
            with open("sub.txt", "r") as file:
                subscriptions = file.readlines()
            subscriptions = [sub for sub in subscriptions if sub.strip().split(", ")[0] != str(target_user_id)]
            with open("sub.txt", "w") as file:
                file.writelines("%s\n" % sub for sub in subscriptions)
            await bot.send_message(target_user_id, f"🎉 Ваша подписка была убрана администратором с ID {user_id}!")
            await event.respond(f"Подписка убрана у пользователя с ID {target_user_id}.")
        else:  
            with open("sub.txt", "a") as file:
                file.write(f"{target_user_id}, {days}\n")
            await bot.send_message(target_user_id, f"🎉 Ваша подписка выдана на {days} дня(ей) администратором с ID {user_id}!")
            await event.respond(f"Подписка на {days} дней выдана пользователю с ID {target_user_id}.")
    except ValueError:
        await event.respond("Пожалуйста, используйте правильный формат: /give_sub (ID Пользователя) (Количество дней).")
    except Exception as e:
        await event.respond("Произошла ошибка при выдаче подписки. Проверьте правильность ввода.")
        print(f"Ошибка: {e}")

@bot.on(events.NewMessage(pattern='/give_whitelist'))
async def give_whitelist(event):
    user_id = event.sender.id
    if user_id != owner_id:  
        await event.respond("У вас нет прав для выдачи вайт-листов.")
        return
    
    try:
        parts = event.message.message.split(" ")
        if len(parts) != 3:
            await event.respond("Неправильный формат. Используйте: /give_whitelist (ID Пользователя) (Количество дней)")
            return

        target_user_id = int(parts[1])  
        days = int(parts[2])  

        if days == 0:  
            with open("whitelist.txt", "r") as file:
                whitelisted_users = file.readlines()
            whitelisted_users = [user for user in whitelisted_users if user.strip() != str(target_user_id)]
            with open("whitelist.txt", "w") as file:
                file.writelines("%s\n" % user for user in whitelisted_users)
            # Уведомление пользователя о том, что его вайт-лист был убран
            await bot.send_message(target_user_id, f"📄 Вайт-лист был убран администратором с ID {user_id}.")
            await event.respond(f"📄 Вайт-лист у пользователя с ID {target_user_id} убран.")
        else:
            with open("whitelist.txt", "a") as file:
                file.write(f"{target_user_id}\n")
            await bot.send_message(target_user_id, f"🎉 Ваша вайт-лист выдана на {days} дней администратором с ID {user_id}!")
            await event.respond(f"📄 Вайт-лист на {days} дней выдан пользователю с ID {target_user_id}.")
    except ValueError:
        await event.respond("Пожалуйста, используйте правильный формат: /give_whitelist (ID Пользователя) (Количество дней).")
    except Exception as e:
        await event.respond("Произошла ошибка при выдаче вайт-листа. Проверьте правильность ввода.")
        print(f"Ошибка: {e}")

@bot.on(events.NewMessage(pattern='/add_admin'))
async def add_admin(event):
    user_id = event.sender.id
    if user_id != owner_id:  
        await event.respond("У вас нет прав для добавления администраторов.")
        return

    try:
        parts = event.message.message.split(" ")
        if len(parts) != 2:
            await event.respond("Неправильный формат. Используйте: /add_admin (ID Пользователя)")
            return
        
        target_user_id = int(parts[1])
        with open("adm.txt", "a") as file:
            file.write(f"{target_user_id}\n")
        await event.respond(f"🎉 Пользователь с ID {target_user_id} был добавлен в администраторы.")
    except ValueError:
        await event.respond("Пожалуйста, используйте правильный формат: /add_admin (ID Пользователя).")
    except Exception as e:
        await event.respond("Произошла ошибка при добавлении администратора. Проверьте правильность ввода.")
        print(f"Ошибка: {e}")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())