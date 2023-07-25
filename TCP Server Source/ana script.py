# -*- coding: utf-8 -*-
import socket
import time
import os
import shutil
import string
import random
import threading
import datetime
from urllib.request import urlopen
import sys
import traceback
#import ntplib

from module_items import warband_items
from module_troops import warband_troops
from module_directories import directories

def check_file(directory):
    try:
        with open(directory, mode = "x", encoding = "utf-8"):
            print_("Created the file: \"{}\".".format(directory.basename()))
    except FileExistsError:
        pass

def print_(*string, sep = " ", end = "\n", flush = False):
    print("[{}]".format(datetime.datetime.now().strftime("%H:%M:%S")), *string, sep = sep, end = end, flush = flush)
    directories.log.format(strftime = datetime.datetime.now().strftime("%Y_%m_%d"))
    check_file(directories.log)
    with open(directories.log, "a", encoding="utf-8") as file:
        old_stdout = sys.stdout
        sys.stdout = file
        print("[{}]".format(datetime.datetime.now().strftime("%H:%M:%S")), *string, sep = sep, end = end, flush = flush)
        sys.stdout = old_stdout

try:
    file = open("Data\\basic_settings.txt", "r+")
    database = file.read().split("\n")
    file.close()
    print_("Loading basic settings...")
    server_name = database.pop(0).split(" : ")[1]
    discord_id = database.pop(0).split(" : ")[1]
    base_hunger = database.pop(0).split(" : ")[1]
    start_hunger = database.pop(0).split(" : ")[1]
    start_bank = database.pop(0).split(" : ")[1]
    start_money = database.pop(0).split(" : ")[1]
    start_troop = str(warband_troops.index(database.pop(0).split(" : ")[1].strip().lower().replace(" ", "_")))
    base_health = database.pop(0).split(" : ")[1]
    log_file_location = database.pop(0).split(" : ")[1]
    whitelist_enabled = int(database.pop(0).split(" : ")[1])
    idle_income = database.pop(0).split(" : ")[1]
    license_name = database.pop(0).split(" : ")[1]
    is_high_rpg = database.pop(0).split(" : ")[1]
    autosave = int(database.pop(0).split(" : ")[1])
    keep_inventory = int(database.pop(0).split(" : ")[1])
    print_("""
Server Name:   {server_name}\n\
Discord ID:    {discord_id}\n\
Base Hunger:   {base_hunger}\n\
Start Hunger:  {start_hunger}\n\
Start Bank:    {start_bank}\n\
Start Money:   {start_money}\n\
Start Troop:   {start_troop}\n\
Base Health:   {base_health}\n\
Log Loc.:      {log_file_location}\n\
Whitelist:     {whitelist_enabled}\n\
Idle Income:   {idle_income}\n\
License Name:  {license_name}\n\
HRPG:          {is_high_rpg}\n\
Autosave:      {autosave}\n\
Keep Inv.:     {keep_inventory}\
""".format(
    server_name = server_name,
    discord_id = discord_id,
    base_hunger = base_hunger,
    start_hunger = start_hunger,
    start_bank = start_bank,
    start_money = start_money,
    start_troop = start_troop,
    base_health = base_health,
    log_file_location = log_file_location,
    whitelist_enabled = bool(whitelist_enabled).__repr__(),
    idle_income = idle_income,
    license_name = license_name,
    is_high_rpg = (is_high_rpg in ["True", "true", "1"]).__repr__(),
    autosave = bool(autosave).__repr__(),
    keep_inventory = bool(keep_inventory).__repr__(),
))

    extensions = {
        "Custom Announcement" : 1,
        "Hunger" : 0,#bozuk
        "Door Keys" : 1,
        "Letter" : 0,#bozuk
        "Knock-Out" : 0,
        "Inventory" : 1,
        "Horse Keeper" : 1,
        "Play Times" : 1,
        "Army" : 1,
    }
except:
    print_(traceback.format_exc())
    input()

message_lenght = 80

class LicenseInfo():
    is_licensed = True
    date = datetime.datetime(2023, 7, 30)#y, m, d
    version = "2.4.7"
    text = []
    text.append("Scripts by Sart. Version: {}, License: {}".format(version, license_name if is_licensed else "Free Version"))
    text[0] = text[0].ljust(message_lenght)
    text.append("Sunucunun lisansı {} tarihine kadardır.".format(date.strftime("%Y.%m.%d")))
    if not is_licensed:
        text.append("Sunucunun lisansı bedava deneme sürümüdür.")
    text[1] = text[1].ljust(message_lenght)
    text = "".join(text)

try:
    current_date = datetime.datetime.strptime(urlopen('http://just-the-time.appspot.com/').read().strip().decode(), "%Y-%m-%d %H:%M:%S")
    ##current_date = datetime.datetime.fromtimestamp(ntplib.NTPClient().request('pool.ntp.org').tx_time)
    if current_date > LicenseInfo.date:
        print_("License date is over.")
        input()
        sys.exit()
except:
    print_("Cannot connect to the license server.")
    input()
    sys.exit()

print_("Version: {}, Date: {}".format(LicenseInfo.version, LicenseInfo.date.strftime("%Y.%m.%d")))

if not LicenseInfo.is_licensed:
    extensions = {
        "Custom Announcement" : 0,
        "Hunger" : 0,#bozuk
        "Door Keys" : 0,
        "Letter" : 0,#bozuk
        "Knock-Out" : 0,
        "Inventory" : 0,
        "Horse Keeper" : 0,
        "Play Times" : 0,
        "Army" : 0,
    }

strings = {
    "/yardim help" : "\
/yardim: Komutlar listesini gosterir :D^\
Help parametresi güvenli bir şekilde komutları öğrenmeni sağlar.\
",
    "hatali komut" : "\
Böyle bir komut bulunamadı. /yardim yazarak komutları öğrenebilirsiniz.\
",
    "/ooc help" : "\
/b (mesaj): Local chat e ooc mesaj gönderirsiniz.\
",
    "/{} ek mesaj beklenir" : "\
/{} komutundan sonra bir mesaj beklenir.\
",
    "/discord" : "\
Discord adresimiz: https://discord.gg/{0}^\
Sadece {0} yazarakta ekleyebilirsiniz.\
",
    "/discord help" : "\
/discord: Discord sunucumuzun linkini gösterir.\
",
    "/ayril help" : "\
/ayril: commoners'a katılırsınız.\
",
    "/me help" : "\
/me (mesaj): local chate eyleminizi bildirirsiniz. \
",
    "/dene help" : "\
/dene: Başarılı ya da Başarısız yazar.^\
/dene {zar}: 0 ile zar arasında sınırlar dahil bir sayı yazar ve renklendirir.\
",
    "/do help" : "\
/do (mesaj): local chat e durumunuzu bildirirsiniz. \
",
    "problem with script" : "\
!!! Scriptin yeniden başlatılmasından ötürü bir hata oluştu.^\
Lütfen sunucudan çıkıp tekrar giriniz.\
",
    "/duyuru help" : "\
/duyuru (mesaj): herkese duyuru geçersiniz.\
",
    "no permisson to use {}" : "\
{} komutunu kullanma hakkınız yok. Discorddan adminler ile görüşebilirsiniz.\
",
    "desteklenmeyen karakter" : "\
Local chate desteklenmeyen karakter gönderdiniz.\
",
    "soylenti help" : "\
/soylenti (mesaj): Soylenti IC olarak herkese paylasilir. Ozel roller kullanabilir.\
",
    "banka hesabiniz {}" : "\
Banka hesabiniz: {} dinar.\
",
    "/license help" : "\
Lisans hakkında bilgi verir.\
",
    "/license" : LicenseInfo.text,
    "/kuzgun" : "\
Kuzgun sayınız : {}\
",
    "/mektup help" : "\
/mektup yaz help^\
/mektup oku help^\
/mektup mühürle help\
",
    "/mektup al help" : "\
/kuzgun al^\
2000 para ile bir eğitimli posta güvercini alırsınız.^\
Güvercininiz düşük bir ihtimal ile yolda ölebilir.^\
Birden fazla güvercininiz olabilir.\
",
    "kuzgun buy success" : "\
Kuzgun alımı başarılı. Kuzgun sayınız : {}\
",
    "/mektup yaz help" : "\
/mektup yaz (mesaj)^\
Yere money_pouch gibi yazılı bir mektup bırakırsınız.^\
Bu mektubu güvercin yuvasına götürüp başkasına gönderebilirsiniz.^\
Yazılı mektubu başkası sizin adınıza gönderebilir.\
",
    "kotu mektup" : "\
Bu mektup parçalanmış.\
",
    "kotu muhur" : "\
Bu mühür bişey ifade etmiyor.\
",
    "/mektup oku help" : "\
/mektup oku^\
Elinizde tuttuğunuz mektubu okursunuz.\
",
    "/mektup mühürle help" : "\
/mektup mühürle (guid)^\
Elinizdeki mektubu sadece belirttiğiniz kişinin okuyabilmesini sağlar.^\
Kişinin guidini '/guid (isim)' ile öğrenebilirsiniz.\
",
    "muhur basarili" : "\
Mektubunuz {} kişisine mühürlendi.\
",
    "mail not for you" : "\
Mektup başkası adına mühürlenmiş.\
",
    "muhur kaldirildi" : "\
Mektubun mühürü kaldırıldı.\
",
    "/guid help" : "\
/guid : kendi guidinizi gösterir.^\
/guid (isim) : ismi verilen kişinin guidini gösterir.\
",
    "aranan guid" : "\
{} kişisinin guidi: {}\
",
    "kişi bulunamadı" : "\
Aradığınız isim bulunamadı.\
",
    "guidiniz" : "\
Guidiniz: {}\
",
    "/envanter help" : "\
/envanter: Kişisel envanterinizi açar.\
",
    "/bağla help" : "\
/bağla: Bindiğiniz atı bağlar/çözer.\
",
    "/anahtar help": "\
/anahtar göster^\
KapıID: Kapı ID ye bağlı guidleri listeler.^\
/anahtar ekle^\
KapıID guid1 guid2...: Kapı ID'ye guidler eklemenizi sağlar.^\
/anahtar çıkar^\
KapıID guid1 guid2...: Kapı ID'den guidler çıkarmanızı sağlar.\
",
    "/anahtar göster": "\
Kapı (id: {}): {}.\
",
    "/anahtar ekle": "\
{} GUID'leri eklendi.^\
Kapı (id: {}): {}.\
",
    "/anahtar çıkar": "\
{} GUID'leri çıkarıldı.^\
Kapı (id: {}): {}.\
",
    "/ordu help": "\
Ordu Sistemi (Beta):^\
/ordu birlikler^\
/ordu komutlar^\
/ordu eğit help         \
/ordu ekipman help^\
/ordu aggro help\
",
    "/ordu eğit help": "\
/ordu eğit (birlik) [miktar]^\
Komuta edebileceğiniz birlikler eğitir.    \
örn: /ordu eğit archer^\
örn2: /ordu eğit footman 5                 \
Birlikleri listelemek için \"/ordu birlikler\".\
",
    "/ordu aggro help": "\
/ordu aggro^\
Ordunun commonerlara karşı olan saldırganlığını değiştirir.\
",
    "/ordu komutlar help": "\
/ordu komutlar^\
Orduyu yönetmek için kullanılan sayı ve function tuşlarını listeler.\
",
    "/ordu birlikler": "\
Kullanılabilen birlikler:^\
- footman^\
- archer^\
- lancer\
",
    "/ordu birlikler help": "\
/ordu birlikler^\
Orduda kullanılabilecek birlikleri listeler.\
",
    "/ordu ekipman help": "\
/ordu ekipman (birlik)^\
Kuşandığınız ekipmanları birliğin ekipmanı olarak tanımlar.\
",
}
colors = {
    "beyaz" : 0,
    "koyu mavi shout": 1,
    "koyu mavi": 2,
    "acik kirmizi": 3,
    "koyu kirmizi": 4,
    "acik kahverengi": 5,
    "koyu kahverengi": 6,
    "discord pembe": 7,
    "acik yesil": 8,
    "koyu yesil": 9,
    "altın" : 10,
    "gümüş" : 11,
    "bakır" : 12,
    "söylenti" : 13,
    "turuncu" : 14,
    "mektup" : 15,
    "local chat" : 16,
    "local chat shout" : 17,
    "commoners" : 18,
}

special_strings = {
    "welcome" : [
        ("Merhabalar. {} sunucusuna hoşgeldiniz.".format(server_name), colors["koyu yesil"]),
        ("Komutlar local-chat'e (Q) yazılarak kullanılır.", colors["local chat"]),
        ("/yardım yazarak komutlara ulaşabilirsiniz.", colors["beyaz"]),
        ("/discord yazarak discord adresimize ulaşabilirsiniz.", colors["discord pembe"]),
        ("Rol yapmaya başlamadan önce uğramanızı tavsiye ederim.", colors["beyaz"]),
        ("ScriptsBySart. /license for more info.", colors["söylenti"]),
    ],
    "yardim" : [
        ("\"/(komut) help\" yazarak detaylı açıklamalara ulaşabilirsiniz.", colors["beyaz"]),
        ("Komutlar:", colors["beyaz"]),
        ("/yardım", colors["beyaz"]),
        ("/discord", colors["discord pembe"]),
        ("/ayrıl", colors["commoners"]),
        ("/dene (mesaj)", colors["söylenti"]),
        ("/b (mesaj)", colors["koyu mavi"]),
        ("/me (mesaj)", colors["acik kahverengi"]),
        ("/do (mesaj)", colors["acik yesil"]),
        ("/w (mesaj), /l (mesaj)", colors["turuncu"]),
    ],
    "/ordu_komutlar": [
        ("Groups:^1 - Soldiers^2 - Missiles^3 - Cavalry^0 - Everyone", colors["beyaz"]),
        ("^F1 - Movement Orders^    F1 - Hold Position^    F2 - Follow Me^    F3 - Charge", colors["beyaz"]),
        ("^F2 - Formation Orders^    F1 - 1 Row^    F2 - 2 Rows^    F3 - 3 Rows", colors["beyaz"]),
        ("^    F4 - 4 Rows^    F5 - 5 Rows^    F6 - Spread Out^    F7 - Stand Closer", colors["beyaz"]),
    ],
}

if extensions["Custom Announcement"]:
    special_strings["yardim"].extend([
        ("Roleplay komutları:", colors["beyaz"]),
        ("/duyuru (mesaj)", colors["commoners"]),
        ("/söylenti (mesaj)", colors["söylenti"]),
        ("/kart", colors["koyu yesil"]),
    ])
if extensions["Letter"]:
    special_strings["yardim"].extend([
        ("Mektup Sistemi:", colors["beyaz"]),
        ("/mektup help", colors["mektup"]),
    ])
if extensions["Door Keys"]:
    special_strings["yardim"].extend([
        ("Kapı Kilidi Sistemi +", colors["beyaz"]),
    ])
if extensions["Knock-Out"]:
    special_strings["yardim"].extend([
        ("Bayılma Sistemi +", colors["beyaz"]),
    ])
if extensions["Inventory"]:
    special_strings["yardim"].extend([
        ("Envanter Sistemi:", colors["beyaz"]),
        ("/envanter help", colors["turuncu"]),
    ])
if extensions["Horse Keeper"]:
    special_strings["yardim"].extend([
        ("At Bağlama Sistemi:", colors["beyaz"]),
        ("/bağla help", colors["koyu kahverengi"]),
    ])
if extensions["Army"]:
    special_strings["yardim"].extend([
        ("Ordu Sistemi (Beta):", colors["beyaz"]),
        ("/ordu help", colors["acik kahverengi"]),
    ])
admin_client = None
admin_addr = None
admin_q = list()
players = dict()
names = dict()
bad_ips = dict()
doors = dict()
hunger_count = dict()
hunger_count_copy = dict()
banned_players = dict()
mails = dict()
inventories = dict()
armies = dict()
play_times = dict()
join_times = dict()
chests = dict()
doors = dict()
admin_permissions = dict()
authentication_time = "0"
force_names = False
kick_unmatched_name = 0
exclude_admins = False
player_count = 0
banned_ips = list()
command_perm = list()
whitelist = list()
t_chat_users = list()
key_checkers = list()
settings = list()
command_perm = list()
perm_id = {
    "Duyuru": 0,
    "Soylenti": 1,
    "Cards": 2,
}
data_id = {
    "Faction": 0,
    "Troop": 1,
    "Gold": 2,
    "Health": 3,
    "Hunger": 4,
    "Head": 5,
    "Body": 6,
    "Foot": 7,
    "Gloves": 8,
    "Itm0": 9,
    "Itm1": 10,
    "Itm2": 11,
    "Itm3": 12,
    "Horse": 13,
    "HorseHP": 14,
    "X": 15,
    "Y": 16,
    "Z": 17,
    "Bank": 18,
}
admin_permissions_ids = {
    "Spectate" : 0,
    "Tools" : 1,
    "Panel" : 2,
    "Gold" : 3,
    "Kick" : 4,
    "Temp" : 5,
    "Perm" : 6,
    "Fade/Kill" : 7,
    "Freeze" : 8,
    "Teleport" : 9,
    "adminItems" : 10,
    "Heal" : 11,
    "Godlike" : 12,
    "Ship" : 13,
    "Announce" : 14,
    "Poll" : 15,
    "allItems" : 16,
    "Mute" : 17,
    "Animal" : 18,
    "joinFaction" : 19,
    "Factions" : 20
}
mail_keys = {
    "Name" : 0,
    "Message" : 1,
    "Seal" : 2
}
admin_queue_commands = {
    "Kick": 1,
    "Settings": 2,
    "Change Name": 3,
    "Hunger": 13,
}
setting_types = {
    "Idle Income" : 0,
    "High RPG" : 1,
    "Authentication Time" : 2,
    "Base Health" : 3,
    "Base Hunger" : 4,
    "Knock Out" : 5,
    "Autosave" : 6,
    "Keep Equipment" : 7,
    "Settings End" : 8,
}
message_type = {
    "Local Chat": 1,
    "Message": 2,
    "Special Message": 3,
    "Announce": 4,
    "Command": 5,
    "Whisper": 6,
    "Local Whisper": 7,
}
command_type = {
    "Open Personal Inventory": 1,
    "Leave Faction": 2,
    "Army Recruit": 3,
    "Army Toggle Aggro": 4,
    "Army Set Equipment": 5,
    "Tie Horse": 6,
}
troops = {
    "footman": 0,
    "archer": 1,
    "lancer": 2,
}
base_items = ["0", start_troop, start_money, base_health, base_hunger, "0", "142", "316", "0", "0", "0", "0", "0", "-1", "0", "-1", "-1", "-1", start_bank, "0", "0"]
hunger_damages = ["5", "5", "5", "5", "5", "5", "10", "10", "10", "10", "10", "10", "15", "25", "45", "70", "90", "200"]
base_inventory = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]

def clear_spaces(string):
    for character in [" ", "\t"]:
        string = string.replace(character, "")
    return string
        
def import_custom_announcement():
    if not extensions["Custom Announcement"]:
        return
    command_perm.clear()
    file = open("Data\\permissions.txt", "r+")
    database = file.read().split("\n")
    file.close()
    if not database[0]:
        return
    for permission in database:
        command_perm.append(permission.split("%"))
def import_door_keys():
    if not extensions["Door Keys"]:
        return
    doors.clear()
    file = open("Data\\door_keys.txt", "r+")
    database = file.read().split("\n")
    file.close()
    if not database[0]:
        return
    key_checkers.clear()
    key_checkers.extend(database.pop(0).split("%"))
    for x in database:
        x = x.split("%")
        door = x[0]
        keys = x[1:]
        doors[door] = keys
def import_admin_permissions():
    admin_permissions.clear()
    file = open("Data\\admin_permissions.txt", "r+")
    database = file.read().split("\n")
    file.close()
    for line in database:
        guid, *permissions = clear_spaces(line).split("%")
        if len(permissions) != len(admin_permissions_ids):
            print("WARNING! Admin with (guid: {}) is cofigured poorly.".format(guid))
        admin_permissions[guid] = permissions
def import_whitelist():
    if not whitelist_enabled:
        return
    whitelist.clear()
    file = open("Data\\whitelist.txt", "r+")
    database = file.read().split("\n")
    file.close()
    for unique_id in database:
        whitelist.append(unique_id)
def import_mails():
    if not extensions["Letter"]:
        return
    mails.clear()
    file = open("Data\\mails.txt", "r", encoding = "utf-8")
    database = file.read().split("\n")
    file.close()
    if not database[0]:
        return
    for x in database:
        x = x.split("%")
        code = x[0]
        name = x[1]
        post = x[2]
        seal = x[3]
        mails[code] = [name, post, seal]
def import_names():
    global force_names, kick_unmatched_name, exclude_admins
    names.clear()
    with open("Data\\names.txt", "r", encoding = "utf-8") as file:
        data = file.read()
    if not data:
        with open("Data\\names.txt", "w", encoding = "utf-8") as file:
            file.write("Force Usernames : 0")
            file.write("Kick Unmatched : 0")
            file.write("Exclude Admins : 0")
        return
    force_names, kick_unmatched_name, exclude_admins, *lines = data.split("\n")
    if force_names.split(" : ")[1] in ["True", "true", "+", "1"]:
        force_names = True
    else:
        force_names = False
    if kick_unmatched_name.split(" : ")[1] in ["True", "true", "+", "1"]:
        kick_unmatched_name = 1
    else:
        kick_unmatched_name = 0
    if exclude_admins.split(" : ")[1] in ["True", "true", "+", "1"]:
        exclude_admins = True
    else:
        exclude_admins = False
    for line in lines:
        unique_id, name = line.split(" : ")
        names[unique_id] = name
def import_inventories():
    if not extensions["Inventory"]:
        return
    file = open("Data\\inventories.txt", "r+")
    database = file.read().split("\n")
    file.close()
    base_inventory.clear()
    base_inventory.extend(database[0].split("%")[1:])
    inventories.clear()
    for x in database[1:]:
        x = x.split("%")
        unique_id = x[0]
        inventory = x[1:]
        inventories[unique_id] = inventory
def import_armies():
    if not extensions["Army"]:
        return
    with open("Data\\armies.txt", "r+") as file:
        database = file.read().split("\n")
    armies.clear()
    for line in database:
        troop, *raw_equipments = line.split("%")
        equipments = list()
        for equipment in raw_equipments:
            if equipment in warband_items:
                equipments.append(str(warband_items.index(equipment)))
            else:
                print("WARNING! While importing the troop: {}, an invalid item: {} was found.".format(troop, equipment))
        if len(equipments) > 8:
            print("WARNING! While importing the troop: {}, more than 8 items was found.".format(troop))
            equipments = equipments[:8]
        armies[troop] = equipments + ["0" for i in range(8 - len(equipments))]
    for troop in troops:
        troop_name = "base_{}".format(troop)
        if not troop_name in armies:
            print("WARNING! troop: {} is not defined. Creating an empty one.".format(troop_name))
            armies[troop_name] = ["0" for i in range(8)]
def import_chests():
    file = open("Data\\chests.txt", "r+")
    database = file.read().split("\n")
    file.close()
    chests.clear()
    if not database[0]:
        return
    for x in database:
        x = x.split("%")
        scene_prop = x[0]
        variation_id = x[1]
        items = x[2:]
        chests[(scene_prop, variation_id)] = items
def import_play_times():
    global authentication_time
    if not extensions["Play Times"]:
        return
    file = open("Data\\play_times.txt", "r+")
    database = file.read().split("\n")
    file.close()
    play_times.clear()
    authentication_time = database[0].split(" : ")[1]
    for data in database[1:]:
        data = data.split(" : ")
        unique_id = data.pop(0)
        play_time = data.pop(0)
        play_times[unique_id] = play_time

def get_random_string(length):
    random_list = []
    for i in range(length):
        random_list.append(random.choice(string.ascii_uppercase + string.digits))
    return ''.join(random_list)

def send_message(client, message, lenght = 128):
    text = "HTTP/1.1 200 OK\r\nContent-Lenght: {1}\r\n\r\n{0}\r\n".format(message, lenght)
    client.send(text.encode())

def serialize(*args):
    return ("{}|" * len(args)).format(*args)

def send_message_warband(client, *message):
    text = "HTTP/1.1 200 OK\r\nContent-Lenght: {}\r\n\r\n{}\r\n".format(128, serialize(*message))
    client.send(text.encode())

def send_message_special(client, unique_id, message_id):
    send_message_warband(client,
        message_type["Special Message"], unique_id, 1,
        special_strings[message_id][0][0], message_id, special_strings[message_id][0][1]
    )

def admin_queue_add_command(command, *args):
    admin_q.append(serialize(admin_queue_commands[command], *args))
    
def admin_queue_add_setting(setting_type, value):
    settings.append(serialize(admin_queue_commands["Settings"], setting_types[setting_type], value))
    
def ban_player(unique_id, permanently = True, hours = 1, reason = "Not specified."):
    banned_players[unique_id] = ("1" if permanently else "0", datetime.datetime.now() + datetime.timedelta(hours = hours), reason)
    admin_queue_add_command("Kick", unique_id)
    ban_message = "Player with (unique id: {}) got banned {}. Reason: {}".format(unique_id, "permanently" if permanently else "temporarily", reason)
    admin_q.append(ban_message)
    print_(ban_message)
    if admin_client:
        admin_client.send(ban_message.encode())

def warning(client, message, log, addr, lenght = 128):
    send_message(client, message, lenght)
    while True:
        code = get_random_string(5)
        if code not in bad_ips:
            bad_ips[code] = addr[0]
            break
    if admin_client:
        admin_client.send("!! {} {} Ban kodu: {}".format(addr[0], log, code).encode())
    print_("!! {} {} Ban kodu: {}".format(addr[0], log, code))

def refresh_admin():
    global admin_client, admin_addr
    while True:
        time.sleep(30)
        if admin_client:
            try:
                admin_client.send(b"%reconnect%")
            except ConnectionResetError:
                admin_client = None
                admin_addr = None
            finally:
                admin_client.close()
                admin_client = None
    
def main_request_handler(client, addr, port):
    global admin_client, admin_addr, ddos_timer, player_count
    if addr[0] in banned_ips:
        if admin_client:
            admin_client.send("!! Banned ip {} tried to connect".format(addr[0]).encode())
        print_("!! Banned ip {} tried to connect".format(addr[0]))
        client.close()
        return
    is_admin = False
    try:
        message = client.recv(1024)
        message = message.decode().split(" ")
    except ConnectionResetError:
        log = "Beklenmedik bir sekilde iletisimi kesti."
        while True:
            code = get_random_string(5)
            if code not in bad_ips:
                bad_ips[code] = addr[0]
                break
        if admin_client:
            admin_client.send("!! {} {} Ban kodu: {}".format(addr[0], log, code).encode())
        print_("!! {} {} Ban kodu: {}".format(addr[0], log, code))
        return
    except UnicodeDecodeError:
        client.close()
        return
    if len(message) < 2:
        try:
            warning(client,
                    "Unknown Message. Use 'help' to see commands.",
                    message.__repr__(),
                    addr
                    )
            client.close()
        except ConnectionResetError:
            return
        return
    message = message[1][1:].split("%3C")
    action = message[0].replace("%20", "_")
    message = message[1:]
    if (not action in ["special_string", "save_to_db", "ping_tcp", "load_chest", "save_chest"]) and not (action == "admin_connect" and admin_addr == addr[0]):
        print_("Got: ", action, message, port)
    try:
        if action == "load_player":
            #Faction<Troop
            unique_id = message[0]
            name = message[1]
            is_admin = message[2]
            if force_names and unique_id in names and not(int(is_admin) and exclude_admins):
                admin_queue_add_command("Change Name", names[unique_id], unique_id, kick_unmatched_name)
            else:
                names[unique_id] = name
            if not unique_id in players:
                players[unique_id] = base_items.copy()
                players[unique_id][data_id["Health"]] = "100"
                players[unique_id][data_id["Hunger"]] = start_hunger
            if not unique_id in inventories:
                inventories[unique_id] = base_inventory
            if not unique_id in play_times:
                play_times[unique_id] = "0"
            send_message_warband(client,
                unique_id,
                players[unique_id][data_id["Faction"]],
                players[unique_id][data_id["Troop"]],
                players[unique_id][data_id["Gold"]],
                players[unique_id][data_id["Bank"]],
                play_times[unique_id] if extensions["Play Times"] else "0",
                "1" if extensions["Inventory"] else "0",
                *inventories[unique_id],
            )
        elif action == "load_admin":
            unique_id = message[0]
            if not unique_id in admin_permissions:
                if admin_client:
                    admin_client.send("!! Kayitsiz admin girisi. Unique_ID: {}".format(unique_id).encode())
                print_("!! Kayitsiz admin girisi. Unique_ID: {}".format(unique_id))
                send_message(client, unique_id + "|1" * len(admin_permissions_ids))
            else:
                send_message_warband(client,
                    unique_id,
                    *admin_permissions[unique_id],
                    *["1" for x in range(min(len(admin_permissions_ids) - len(admin_permissions[unique_id]), 0))]
                )
        elif action == "load_gear":
            #Gold<Health<Hunger<Head<Body<Foot<Gloves<Itm0<Itm1<Itm2<Itm3<Horse<HorseHP<X<Y<Z<Bank
            unique_id = message[0]
            if not unique_id in players:
                players[unique_id] = base_items.copy()
                players[unique_id][data_id["Health"]] = "100"
            kick = "0"
            if unique_id in banned_players:
                permanently = int(banned_players[unique_id][0])
                hours = banned_players[unique_id][1]
                reason = banned_players[unique_id][2]
                if permanently or (datetime.datetime.now() <= hours):
                    kick = "1"
                    response = "You have been banned {}!^Reason: {}.^Your GUID: {}".format("permanently" if permanently else "temporarily", reason, unique_id)
                else:
                    banned_players.pop(unique_id)
            if whitelist_enabled and unique_id not in whitelist:
                kick = "1"
                response = "You are not whitelisted.^Your GUID: {}".format(unique_id)
            if not LicenseInfo.is_licensed and player_count > 10:
                kick = "1"
                response = "Server has 10 player limit reached. (Free Version)"
            if kick == "0":
                response = "Bakiyeniz: {}".format(players[unique_id][data_id["Bank"]])
            player_count += 1
            send_message_warband(client, unique_id, kick, response,
                players[unique_id][data_id["Health"]],
                players[unique_id][data_id["Hunger"]],
                *players[unique_id][data_id["Head"] : data_id["Gloves"] + 1],
                *players[unique_id][data_id["Itm0"] : data_id["Itm3"] + 1],
                *players[unique_id][data_id["Horse"] : data_id["HorseHP"] + 1],
                *players[unique_id][data_id["X"] : data_id["Z"] + 1]
            )
        elif action == "message_sent":
            player_id = message[0]
            event_type = int(message[1])
            unique_id = message[2]
            string0 = message[3]
            faction_colour = message[4]
            string0 = string0.replace("%20", " ").replace("%5B", "[").replace("%5D", "]")
            string0 = string0.replace("%C5%9F", "ş").replace("%C3%A7", "ç").replace("%C4%B1", "ı").replace("%C3%B6", "ö").replace("%C4%9F", "ğ").replace("%C3%BC", "ü")
            string0 = string0.replace("%C5%9E", "Ş").replace("%C3%87", "Ç").replace("%C4%B0", "İ").replace("%C3%96", "Ö").replace("%C4%9E", "Ğ").replace("%C3%9C", "Ü")
            string1 = ""
            skip = 0
            for char in string0:
                if skip:
                    skip -= 1
                    continue
                if char == "%":
                    skip = 2
                    continue
                string1 += char
            string0 = string1
            if len(string0) > 256:
                ban_player(unique_id, permanently = True, reason = "Chat Overflow.")
                sys.exit()
            command = string0.split(" ")[0][1:]
            text = string0.split(" ")[1:]
            if not any(("%" in text_part) for text_part in string0.split(" ")):
                if string0[0] == "/":
                    if command in ["yardim", "yardım", "help"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/yardim help"])
                            else:
                                send_message_special(client, unique_id, "yardim")
                        else:       
                            send_message_special(client, unique_id, "yardim")
                    elif command == "license" or command == "lisans":
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/license help"])
                            else:
                                send_message_warband(client, message_type["Message"], unique_id, colors["söylenti"], strings["/license"])
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["söylenti"], strings["/license"])
                    elif command in ["b", "B", "ooc"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ooc help"])
                            else:
                                colour = (colors["acik kirmizi"], colors["koyu kirmizi"])
                                send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colour[event_type],
                                    "[OOC][{}] ".format(names[unique_id]) + " ".join(text)
                                )
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("b"))
                    elif command == "me":
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/me help"])
                            else:
                                colour = (colors["discord pembe"], colors["discord pembe"])
                                send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colour[event_type],
                                    "\"{} ".format(names[unique_id]) + " ".join(text) + "\""
                                )
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("me"))
                    elif command == "do":
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/do help"])
                            else:
                                colour = (colors["acik yesil"], colors["koyu yesil"])
                                send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colour[event_type],
                                    "({}) \"".format(names[unique_id]) + " ".join(text) + "\""
                                )
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("do"))
                    elif command in ["roll", "dene"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/dene help"])
                            elif text[0].isnumeric():
                                roll = random.randint(0, int(text[0]))
                                middle = int(text[0]) / 2
                                if roll == middle:
                                    colour = colors["turuncu"]
                                elif roll < middle:
                                    colour = colors["koyu kirmizi"]
                                else:
                                    colour = colors["söylenti"]
                                send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colour,
                                    "({}) rolled [{}]: *{}*".format(names[unique_id], text[0], roll)
                                )
                        else:
                            basarili = random.randint(0, 1)
                            colour = colors["söylenti"] if basarili else colors["koyu kirmizi"]
                            send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colour,
                                "({}) *{}*".format(names[unique_id], "Başarılı" if basarili else "Başarısız")
                            )
                    elif command == "duyuru" and extensions["Custom Announcement"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/duyuru help"])
                            else:
                                if unique_id in command_perm[perm_id["Duyuru"]]:
                                    send_message_warband(client, message_type["Announce"], faction_colour, "Duyuru! {}: ".format(names[unique_id]) + " ".join(text))
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["no permisson to use {}"].format("Duyuru"))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("duyuru"))
                    elif command in ["söylenti", "soylenti"] and extensions["Custom Announcement"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/soylenti help"])
                            else:
                                if unique_id in command_perm[perm_id["Soylenti"]]:
                                    send_message_warband(client, message_type["Announce"], colors["söylenti"], "Söylenti: " + " ".join(text))
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["no permisson to use {}"].format("Soylenti"))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("soylenti"))
                    elif command in ["kart", "card"] and extensions["Custom Announcement"]:
                        if len(text):
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/kart help"])
                        elif unique_id in command_perm[perm_id["Cards"]]:
                            card_colors = [("koyu mavi", "Blue"), ("koyu kirmizi", "Red"), ("koyu yesil", "Green"), ("altın", "Yellow")]
                            rand_color = card_colors[random.randrange(0, len(card_colors))]
                            send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colors[rand_color[0]], "{} drew a card coloured '{}'!".format(names[unique_id], rand_color[1]))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["no permisson to use {}"].format("Cards"))
                    elif command in ["bj"] and extensions["Custom Announcement"]:
                        if len(text) and text[0] == "help":
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/bj help"])
                        elif unique_id in command_perm[perm_id["Cards"]]:
                            if len(text) and text[0].isnumeric():
                                roll = random.randint(1, int(text[0]))
                            else:
                                roll = random.randint(1, 10)
                            send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colors["mektup"],
                                "{} drew the card '{}'!".format(names[unique_id], roll)
                            )
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["no permisson to use {}"].format("Cards"))
                    elif command in ["w", "whisper", "fısılda", "fisilda"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], "")#strings["/whisper help"])
                            else:
                                send_message_warband(client, message_type["Whisper"], unique_id, colors["turuncu"], " ".join(text))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("whisper"))
                    elif command in ["l"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], "")#strings["/l help"])
                            else:
                                send_message_warband(client, message_type["Local Whisper"], unique_id, colors["turuncu"], " ".join(text))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/{} ek mesaj beklenir"].format("l"))
                    elif command == "discord":
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/discord help"])
                            else:
                                send_message_warband(client, message_type["Message"], unique_id, colors["discord pembe"], strings["/discord"].format(discord_id))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["discord pembe"], strings["/discord"].format(discord_id))
                    elif command == "ayril" or command == "ayrıl":
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ayril help"])
                            else:
                                send_message_warband(client, message_type["Command"], command_type["Leave Faction"], unique_id)
                        else:
                            send_message_warband(client, message_type["Command"], command_type["Leave Faction"], unique_id)
                    elif command == "guid":
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/guid help"])
                            else:
                                for guid in names.keys():
                                    if text[0] == names[guid]:
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["aranan guid"].format(text[0], guid))
                                        break
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["acik kirmizi"], strings["kişi bulunamadı"])
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["guidiniz"].format(unique_id))
                    elif command == "mektup" and extensions["Letter"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup help"])
                            elif text[0] == "yaz":
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup yaz help"])
                                    else:
                                        while True:
                                            code = str(random.randint(10, 100000))
                                            if code not in mails:
                                                mails[code] = [unique_id, " ".join(text[1:]), "0"]
                                                send_message(client, "22|{}|{}".format(player_id, code))
                            elif text[0] == "oku":
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup oku help"])
                                    else:
                                        send_message(client, "23|{}".format(player_id))
                                else:
                                    send_message(client, "23|{}".format(player_id))
                            elif text[0] == "mühürle" or text[0] == "muhurle":
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup mühürle help"])
                                    elif text[1] == "kaldır" or text[1] == "kaldir":
                                        send_message(client, "25|{}|{}".format(player_id, "0"))
                                    elif text[1].isnumeric():
                                        send_message(client, "25|{}|{}".format(player_id, text[1]))
                                    else:
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup mühürle help"])
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup mühürle help"])
                            else:
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup help"])
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/mektup help"])
                    elif command in ["e", "envanter", "inventory"] and extensions["Inventory"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/envanter help"])
                            else:
                                send_message_warband(client, message_type["Command"], command_type["Open Personal Inventory"], unique_id)
                        else:
                            send_message_warband(client, message_type["Command"], command_type["Open Personal Inventory"], unique_id)
                    elif command in ["isim", "name"] and unique_id in admin_permissions:
                        if len(text) and text[0] == "help":
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], ".")
                        elif len(text) >= 2:
                            other_unique_id = text[0]
                            name = text[1]
                            names[other_unique_id] = name
                            admin_queue_add_command("Change Name", names[other_unique_id], other_unique_id, 0)
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], "Changed {}'s name to {}".format(other_unique_id, names[other_unique_id]))
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], ".")
                    elif command in ["anahtar", "key"] and extensions["Door Keys"] and unique_id in key_checkers:
                        if len(text) >= 2:
                            instance = text[1]
                            if not instance in doors:
                                doors[instance] = []
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/anahtar help"])
                            elif len(text) == 2 and text[0] in ["göster", "goster", "show"]:
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"],
                                    strings["/anahtar göster"].format(instance, ", ".join(doors[instance]))
                                )
                            elif len(text) >= 3:
                                if text[0] in ["ekle", "add"]:
                                    unique_ids = text[2:]
                                    for unique_id in unique_ids:
                                        if not unique_id in doors[instance]:
                                            doors[instance].append(unique_id)
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"],
                                        strings["/anahtar ekle"].format(", ".join(unique_ids), instance, ", ".join(doors[instance]))
                                    )
                                elif text[0] in ["çıkar", "cikar", "remove"]:
                                    unique_ids = text[2:]
                                    for unique_id in unique_ids:
                                        if unique_id in doors[instance]:
                                            doors[instance].remove(unique_id)
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"],
                                        strings["/anahtar çıkar"].format(", ".join(unique_ids), instance, ", ".join(doors[instance]))
                                    )
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/anahtar help"])
                                if doors[instance] == []:
                                    doors.pop(instance)
                            else:
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/anahtar help"])
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/anahtar help"])
                    elif command in ["ordu", "army"] and extensions["Army"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu help"])
                            elif text[0] in ["recruit", "eğit", "egit"]:
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu eğit help"])
                                    elif text[1] in troops:
                                        troop = troops[text[1]]
                                        count = 1
                                        if len(text) >= 3 and text[2].isdigit():
                                            count = int(text[2])
                                        troop_name = "{}_{}".format(unique_id, text[1])
                                        if not troop_name in armies:
                                            troop_name = "base_{}".format(text[1])
                                        equipments = armies[troop_name]
                                        send_message_warband(client, message_type["Command"], command_type["Army Recruit"], unique_id, troop, count, *equipments)
                                    else:
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu eğit help"])
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu eğit help"])
                            elif text[0] in ["aggro"]:
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu aggro help"])
                                    else:
                                        send_message_warband(client, message_type["Command"], command_type["Army Toggle Aggro"], unique_id)
                                else:
                                    send_message_warband(client, message_type["Command"], command_type["Army Toggle Aggro"], unique_id)
                            elif text[0] in ["komutlar", "orders"]:
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu komutlar help"])
                                    else:
                                        send_message_special(client, unique_id, "/ordu_komutlar")
                                else:
                                    send_message_special(client, unique_id, "/ordu_komutlar")
                            elif text[0] in ["birlikler", "troops"]:
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu birlikler help"])
                                    else:
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu birlikler"])
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu birlikler"])
                            elif text[0] in ["ekipman", "equipment"]:
                                if len(text) >= 2:
                                    if text[1] == "help":
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu ekipman help"])
                                    elif text[1] in troops:
                                        send_message_warband(client, message_type["Command"], command_type["Army Set Equipment"], text[1], unique_id)
                                    else:
                                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu ekipman help"])
                                else:
                                    send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu ekipman help"])
                            else:
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu help"])
                        else:
                            send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/ordu help"])
                    elif command in ["bağla", "bagla", "tie"] and extensions["Horse Keeper"]:
                        if len(text):
                            if text[0] == "help":
                                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["/bağla help"])
                            else:
                                send_message_warband(client, message_type["Command"], command_type["Tie Horse"], unique_id)
                        else:
                            send_message_warband(client, message_type["Command"], command_type["Tie Horse"], unique_id)
                    else:
                        send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["hatali komut"])
                else:
                    colour = (colors["local chat"], colors["local chat shout"])
                    send_message_warband(client, message_type["Local Chat"], unique_id, event_type, colour[event_type],
                        "[{}] ".format(names[unique_id]) + string0
                    )
            else:
                send_message_warband(client, message_type["Message"], unique_id, colors["beyaz"], strings["desteklenmeyen karakter"])
        elif action == "special_string":
            unique_id = message[0]
            string0 = message[1]
            counter = int(message[2])
            if counter < len(special_strings[string0]):
                send_message(client, "1|{}|{}|{}|{}|{}".format(
                    unique_id,
                    counter + 1,
                    special_strings[string0][counter][0],
                    string0,
                    special_strings[string0][counter][1],
                ))
            else:
                send_message(client, "0", lenght = 1)
        elif action == "set_equipment":
            unique_id, troop, *items = message
            armies["{}_{}".format(unique_id, troop)] = items
            send_message_warband(client, "1", unique_id, troops[troop], *items)
        elif action == "kuzgun_buy_success":
            player_id = message[0]
            unique_id = message[1]
            players[unique_id][data_id["Pigeon"]] = str(int(players[unique_id][data_id["Pigeon"]]) + 1)
            send_message(client, "5|{}|{}|{}".format(player_id, colors["acik yesil"], strings["mektup buy success"].format(players[unique_id][data_id["Pigeon"]])))
        elif action == "kuzgun_read_success":
            player_id = message[0]
            code = message[1]
            unique_id = message[2]
            try:
                mail = mails[code]
            except KeyError:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik kirmizi"], strings["kotu mektup"]))
                sys.exit()
            sender = mail[0]
            post = mail[1]
            seal = mail[2]
            if int(seal) and unique_id != seal:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik kirmizi"], strings["mail not for you"]))
                sys.exit()
            if not sender in names:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik kirmizi"], strings["kotu mektup"]))
                sys.exit()
            send_message(client, "5|{}|{}|{}".format(player_id, colors["koyu kahverengi"], "{}  -{}".format(post, names[sender])))
        elif action == "kuzgun_seal_success":
            player_id = message[0]
            target_guid = message[1]
            code = message[2]
            unique_id = message[3]
            try:
                mail = mails[code]
            except KeyError:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik kirmizi"], strings["kotu mektup"]))
                sys.exit()
            if int(mail[mail_keys["Seal"]]) and unique_id != mail[mail_keys["Seal"]]:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik kirmizi"], strings["mail not for you"]))
                sys.exit()
            if target_guid != "0" and not target_guid in names:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik kirmizi"], strings["kotu muhur"]))
                sys.exit()
            mail[mail_keys["Seal"]] = target_guid
            if int(target_guid):
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik yesil"], strings["muhur basarili"].format(names[target_guid])))
            else:
                send_message(client, "5|{}|{}|{}".format(player_id, colors["acik yesil"], strings["muhur kaldirildi"]))
        elif action == "ping_tcp":
            if len(admin_q):
                response = admin_q.pop()
            else:
                response = "0"
            send_message(client, response)
        elif action == "update_settings":
            for setting in settings:
                admin_q.append(setting)
            admin_q.append(serialize(admin_queue_commands["Settings"], setting_types["Settings End"], 0))
            if len(admin_q):
                response = admin_q.pop()
            else:
                response = "0"
            send_message(client, response)
        elif action == "check_door_key":
            unique_id = message[0]
            instance_id = message[1]
            left = message[2]
            is_private = 0
            has_keys = 0
            if instance_id in doors:
                is_private = 1
                if unique_id in doors[instance_id]:
                    has_keys = 1
            send_message_warband(client, 1, unique_id, instance_id, left, is_private, has_keys)
        elif action == "check_door_key_tp":
            unique_id = message[0]
            instance_id = message[1]
            x_offset = message[2]
            y_offset = message[3]
            z_offset = message[4]
            is_pickable = message[5]
            horse_can_tp = message[6]
            is_private = 0
            has_keys = 0
            if instance_id in doors:
                is_private = 1
                if unique_id in doors[instance_id]:
                    has_keys = 1
            send_message_warband(client, 1, unique_id, instance_id, x_offset, y_offset, z_offset, is_pickable, horse_can_tp, is_private, has_keys)
        elif action == "update_food":
            player_id = message[0]
            unique_id = message[1]
            if not unique_id in hunger_count:
                hunger_count_copy[unique_id] = 0
            elif hunger_count[unique_id] == len(hunger_damages) - 1:
                hunger_count_copy[unique_id] = hunger_count[unique_id]
            else:
                hunger_count_copy[unique_id] = hunger_count[unique_id] + 1
            send_message(client, "15|{}|{}".format(player_id, hunger_damages[hunger_count_copy[unique_id]]))
        elif action == "finish_update_food":
            hunger_count = hunger_count_copy.copy()
            hunger_count_copy = dict()
            send_message(client, "0", lenght = 1)
        elif action == "sts":
            text = " ".join(message)
            if (text == "13" and not text in admin_q) or not text == "13": 
                admin_q.append(text)
                client.send(text.encode())
                print_("Sent: {}".format(text))
            else:
                client.send(b"Failed to register hunger")
                print_("Sent: {}".format("Failed to register hunger"))
        elif action == "save_player": #<GUID<Faction<Troop<Gold<Health<Hunger<Head<Body<Foot<Gloves<Itm0<Itm1<Itm2<Itm3<Horse<HorseHP<X<Y<Z
            unique_id = message.pop(0)
            if not unique_id in players:
                players[unique_id] = base_items.copy()
            for i in range(data_id["Faction"], data_id["Gold"] + 1):
                players[unique_id][i] = message.pop(0)
            players[unique_id][data_id["Bank"]] = message.pop(0)
            if extensions["Play Times"]:
                play_times[unique_id] = message.pop(0)
            player_count -= 1
            send_message_warband(client, unique_id),
        elif action == "save_agent":
            unique_id = message.pop(0)
            if not unique_id in players:
                players[unique_id] = base_items.copy()
            for i in range(data_id["Health"], data_id["Z"] + 1):
                players[unique_id][i] = message.pop(0)
            send_message_warband(client, unique_id),
        elif action == "save_equipment":
            unique_id = message.pop(0)
            if not unique_id in players:
                players[unique_id] = base_items.copy()
            for i in range(data_id["Health"], data_id["Z"] + 1):
                players[unique_id][i] = base_items[i]
            for i in range(data_id["Itm0"], data_id["Itm3"] + 1):
                players[unique_id][i] = message.pop(0)
            for i in range(data_id["Head"], data_id["Gloves"] + 1):
                players[unique_id][i] = message.pop(0)
            send_message_warband(client, unique_id),
        elif action == "strip_agent":
            unique_id = message.pop(0)
            if not unique_id in players:
                players[unique_id] = base_items.copy()
            for i in range(data_id["Health"], data_id["Z"] + 1):
                players[unique_id][i] = base_items[i]
            send_message_warband(client, unique_id),
        elif action == "save_chest":
            scene_prop = message[0]
            variation_id = message[1]
            instance_id = message[2]
            data = message[3:]
            variation = (scene_prop, variation_id)
            chests[variation] = []
            for item in data:
                chests[variation].append(item)
            send_message_warband(client, scene_prop, variation_id, len(data), instance_id)
        elif action == "load_chest":
            scene_prop = message[0]
            variation_id = message[1]
            index = message[2]
            instance_id = message[3]
            variation_id_tuple = (scene_prop, variation_id)
            if not variation_id_tuple in chests:
                chests[variation_id_tuple] = []
            if int(index) < len(chests[variation_id_tuple]):
                send_message_warband(client, 1, scene_prop, variation_id, index, instance_id, chests[variation_id_tuple][int(index)])
            else:
                send_message_warband(client, 2, scene_prop, variation_id, index, instance_id)
        elif action == "save_inventory":
            unique_id = message[0]
            data = message[1:]
            inventories[unique_id] = data
            send_message_warband(client, unique_id),
        elif action == "ban_player":
            unique_id = message[0]
            permanently = message[1]
            hours = message[2]
            ban_player(unique_id, permanently = True if permanently == "1" else False, hours = int(hours), reason = "Admin Decision.")
        elif action == "player_ban":
            sended_admin_pass = message[0]
            unique_id = message[1]
            permanently = message[2]
            hours = message[3]
            if sended_admin_pass == admin_pass:
                ban_player(unique_id, permanently = True if permanently == "1" else False, hours = int(hours), reason = "Panel Order.")
                client.send("message%Banned player {}".format(unique_id).encode())
            else:
                client.send(b"message%Hatali sifre.")
                log = "Hatali admin pass ile banlamaya calisti."
                while True:
                    code = get_random_string(5)
                    if code not in bad_ips:
                        bad_ips[code] = addr[0]
                        break
        elif action == "remove_ban":
            sended_admin_pass = message[0]
            unique_id = message[1]
            if sended_admin_pass == admin_pass:
                if unique_id in banned_players:
                    banned_players.pop(unique_id)
                    client.send("message%Removed {}'s ban".format(unique_id).encode())
                else:
                    client.send("message%No ban issued for {}".format(unique_id).encode())
            else:
                client.send(b"message%Hatali sifre.")
                log = "Hatali admin pass ile ban kaldirdi."
                while True:
                    code = get_random_string(5)
                    if code not in bad_ips:
                        bad_ips[code] = addr[0]
                        break
                _print_("!! {} {} Ban kodu: {}".format(addr[0], log, code))
        elif action == "save_to_db":
            try:
                text = ""
                for unique_id in players.keys():
                    try:
                        if unique_id != "GUID":
                            if int(players[unique_id][data_id["Health"]]) < int(base_health):
                                players[unique_id][data_id["Health"]] = base_health
                    except:
                        print_(traceback.format_exc(), "\n", players[unique_id])
                    text += "{}%".format(unique_id) + "%".join(players[unique_id]) + "\n"
                file = open("Data\\database.txt", "w")
                file.write(text[:-1])
                file.close()
            except:
                print_(traceback.format_exc())
            try:
                file = open("Data\\banned_players.txt", "w")
                text = ""
                for unique_id in banned_players:
                    text += "{}%{}%{}%{}\n".format(
                        unique_id,
                        banned_players[unique_id][0],
                        banned_players[unique_id][1].strftime('%Y:%m:%d:%H:%M:%S'),
                        banned_players[unique_id][2].replace("%", "").replace("\n", "")
                    )
                file.write(text[:-1])
                file.close()
            except:
                print_(traceback.format_exc())
            try:
                if extensions["Letter"]:
                    file = open("Data\\mails.txt", "w", encoding = 'utf8')
                    text = ""
                    for code in mails:
                        mail = mails[code]
                        name = mail[0]
                        post = mail[1]
                        seal = mail[2]
                        text += "{}%{}%{}%{}\n".format(code, name, post, seal)
                    file.write(text[:-1])
                    file.close()
            except:
                print_(traceback.format_exc())
            try:
                file = open("Data\\names.txt", "w", encoding = 'utf8')
                text = "\
Force Usernames : {}\n\
Kick Unmatched : {}\n\
Exclude Admins : {}\n\
".format(
    "1" if force_names else "0",
    str(kick_unmatched_name),
    "1" if exclude_admins else "0"
                )
                for unique_id in names.keys():
                    text += unique_id + " : "
                    text += names[unique_id] + "\n"
                file.write(text[:-1])
                file.close()
            except:
                print_(traceback.format_exc())
            try:
                if extensions["Door Keys"]:
                    with open("Data\\door_keys.txt", "w", encoding = 'utf8') as file:
                        text = ["%".join(key_checkers)]
                        for door, keys in doors.items():
                            text.append("%".join([door, *keys]))
                        file.write("\n".join(text))
            except:
                print_(traceback.format_exc())
            try:
                if extensions["Inventory"]:
                    file = open("Data\\inventories.txt", "w", encoding = 'utf8')
                    text = ""
                    text += "Base Inventory%" + "%".join(base_inventory) + "\n"
                    for unique_id in inventories.keys():
                        text += unique_id + "%"
                        text += "%".join(inventories[unique_id]) + "\n"
                    file.write(text[:-1])
                    file.close()
            except:
                print_(traceback.format_exc())
            try:
                if extensions["Army"]:
                    file = open("Data\\armies.txt", "w", encoding = 'utf8')
                    text = ""
                    for troop, items in armies.items():
                        text += troop + "%"
                        text += "%".join([warband_items[int(item_id)] for item_id in items]) + "\n"
                    file.write(text[:-1])
                    file.close()
            except:
                print_(traceback.format_exc())
            try:
                file = open("Data\\chests.txt", "w", encoding = 'utf8')
                text = ""
                for variation_id, items in chests.items():
                    if not items:
                        continue
                    text += "%".join(variation_id) + "%"
                    text += "%".join(items) + "\n"
                file.write(text[:-1])
                file.close()
            except:
                print_(traceback.format_exc())
            try:
                if extensions["Play Times"]:
                    file = open("Data\\play_times.txt", "w", encoding = 'utf8')
                    text = ""
                    text += "Authentication Time Minutes" + " : " + authentication_time + "\n"
                    for unique_id in play_times.keys():
                        text += unique_id + " : " + play_times[unique_id] + "\n"
                    file.write(text[:-1])
                    file.close()
            except:
                print_(traceback.format_exc())
            client.send(b"All players and bans have been saved")

        elif action == "reimport":
            sended_admin_pass = message[0]
            if sended_admin_pass == admin_pass:
                import_door_keys()
                import_custom_announcement()
                import_admin_permissions()
                import_whitelist()
                import_play_times()
                import_names()
                client.send(b"message%Files reimported")
            else:
                client.send(b"message%Hatali sifre.")
                log = "Hatali admin pass ile dosya reimportladi."
                while True:
                    code = get_random_string(5)
                    if code not in bad_ips:
                        bad_ips[code] = addr[0]
                        break
                if admin_client:
                    admin_client.send("!! {} {} Ban kodu: {}".format(addr[0], log, code).encode())
                print_("!! {} {} Ban kodu: {}".format(addr[0], log, code))
        elif action == "help":
            warning(client,
                    "Unknown Message. Use 'help' to see commands.",
                    "Script serverina help mesaji gonderdi.",
                    addr
                    )
        elif action == "show_admin_pass":
            print_(admin_pass)
            client.send(b"Admin Pass printed.")
        elif action == "admin_connect":
            password = message[0]
            if password == admin_pass:
                admin_client = client
                if admin_addr == addr[0]:
                    client.send(datetime.datetime.now().strftime("%H:%M:%S").encode())
                else:
                    client.send(b"Connection Succesfull")
                    admin_addr = addr[0]
                is_admin = True
            else:
                warning(client,
                    "Unknown Message. Use 'help' to see commands.",
                    "Script serverina hatali admin girisi yapti.",
                    addr
                    )
        elif action == "admin_disconnect":
            password = message[0]
            if password == admin_pass:
                admin_client.close()
                admin_client = None
                admin_addr = None
                client.send(b"Admin log disconnected")
            else:
                warning(client,
                    "Unknown Message. Use 'help' to see commands.",
                    "Admini hatali disconnect ettirmeye çalisti.",
                    addr
                    )
        elif action == "ban":
            code = message[0]
            if code in bad_ips:
                banned_ips.append(bad_ips[code])
                bad_ips.pop(code, None)
                client.send(b"Ban issued")
            else:
                warning(client, "Unknown Message. Use 'help' to see commands.",
                        "Hatali code ile ban atti",
                        addr
                        )
        elif action == "save_bans":
            file = open("Data\\banned_ips.txt", "w")
            text = "#".join(banned_ips)
            file.write(text)
            file.close()
            client.send(b"Banned IP's saved")
        elif action == "get_log":
            log_file = message[0]
            try:
                file = open(log_file_location + "\\" + log_file, 'rb')
                client.send(b"recv_file")
                l = file.read(1024)
                while (l):
                   client.send(l)
                   l = file.read(1024)
                file.close()
            except IOError:
                client.send(b"message%Istenen log dosyasi bulunamadi")
        elif action == "get_file":
            sent_admin_pass = message[0]
            requested_file = message[1]
            if sent_admin_pass == admin_pass:
                try:
                    file = open("Data\\" + requested_file, 'rb')
                    client.send(b"recv_file")
                    l = file.read(1024)
                    while (l):
                       client.send(l)
                       l = file.read(1024)
                    file.close()
                except IOError:
                    client.send(b"message%Istenen dosya bulunamadi")
            else:
                client.send(b"message%Hatali sifre.")
                log = "Hatali admin pass ile dosya istedi."
                while True:
                    code = get_random_string(5)
                    if code not in bad_ips:
                        bad_ips[code] = addr[0]
                        break
                if admin_client:
                    admin_client.send("!! {} {} Ban kodu: {}".format(addr[0], log, code).encode())
                print_("!! {} {} Ban kodu: {}".format(addr[0], log, code))
        elif action == "set_file":
            sent_admin_pass = message[0]
            sent_file = message[1]
            if sent_admin_pass == admin_pass:
                client.send(b"send_file")
                with open("Data\\" + sent_file, 'wb') as file:
                    while True:
                        data = client.recv(1024)
                        if not data:
                            break
                        file.write(data)
            else:
                client.send(b"message%Hatali sifre.")
                log = "Hatali admin pass ile dosya gonderdi."
                while True:
                    code = get_random_string(5)
                    if code not in bad_ips:
                        bad_ips[code] = addr[0]
                        break
                if admin_client:
                    admin_client.send("!! {} {} Ban kodu: {}".format(addr[0], log, code).encode())
                print_("!! {} {} Ban kodu: {}".format(addr[0], log, code))
        else:
            warning(client,
                    "Unknown Message. Use 'help' to see commands.",
                    "Script serverina hatali mesaj gonderdi.",
                    addr
                    )
    except IndexError as e:
        warning(client,
                "Unknown Message. Use 'help' to see commands.",
                "Eksik parametre gönderdi.",
                addr
                )
        print(e)
        client.close()
        return
    except ConnectionResetError:
        return
    except:
        print_(traceback.format_exc())
    finally:
        if not is_admin:
            client.close()
        return

def warband_listener(port, ip_adress):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print_(ip_adress)
    server.bind((ip_adress, port))
    server.listen(5)
    while True:
        client, addr = server.accept()
        threading.Thread(target = main_request_handler, args = (client, addr, port)).start()

try:
    directories.rollback.format(filename = "database", strftime = datetime.datetime.now().strftime("%Y_%m_%d"))
    shutil.copyfile("Data\\database.txt", directories.rollback)
    directories.rollback.format(filename = "chests")
    shutil.copyfile("Data\\chests.txt", directories.rollback)
    directories.rollback.format(filename = "inventories")
    shutil.copyfile("Data\\inventories.txt", directories.rollback)
    
    file = open("Data\\database.txt", "r+")
    database = file.read().split("\n")
    file.close()
    for player in database:
        player = player.split("%")
        unique_id = player[0]
        player_data = player[1:]
        players[unique_id] = player_data

    file = open("Data\\banned_players.txt", "r+")
    database = file.read().split("\n")
    file.close()
    for player in database:
        parameters = player.split("%")
        unique_id = parameters.pop(0)
        permanently = parameters.pop(0)
        hours = datetime.datetime.strptime(parameters.pop(0), "%Y:%m:%d:%H:%M:%S")
        reason = parameters.pop(0)
        banned_players[unique_id] = (permanently, hours, reason)

    file = open("Data\\banned_ips.txt", "r+")
    database = file.read().split("#")
    file.close()
    for ip in database:
        banned_ips.append(ip)

    import_door_keys()
    import_custom_announcement()
    import_admin_permissions()
    import_whitelist()
    import_mails()
    import_names()
    import_inventories()
    import_armies()
    import_chests()
    import_play_times()

    admin_queue_add_setting("Base Health", base_health)
    admin_queue_add_setting("Base Hunger", base_hunger)
    admin_queue_add_setting("Knock Out", str(extensions["Knock-Out"]))
    admin_queue_add_setting("Autosave", autosave)
    admin_queue_add_setting("Keep Equipment", keep_inventory),

    if not idle_income in ["0", ""]:
        int(idle_income)
        admin_queue_add_setting("Idle Income", idle_income)

    if is_high_rpg in ["True", "true", "1"]:
        admin_queue_add_setting("High RPG", "1")

    if extensions["Play Times"] and authentication_time != "0":
        admin_queue_add_setting("Authentication Time", authentication_time)

    admin_pass = get_random_string(10)
    print_("Admin log pass is: {}".format(admin_pass))

    threading.Thread(target = refresh_admin).start()
    threading.Thread(target = warband_listener, args = (80, "0.0.0.0")).start()

except:
    print_(traceback.format_exc())
    input()
