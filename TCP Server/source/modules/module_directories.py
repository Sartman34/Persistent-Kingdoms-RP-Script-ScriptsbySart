from modules.header_directories import Directory_Manager

directories = Directory_Manager(
    data = [".", "data"],
    
    logs = [".data", "logs"],
    log = [".logs", "log_{strftime}.txt"],
    rollbacks = [".data", "rollbacks"],
    rollback = [".rollbacks", "{filename}_{strftime}.txt"],
    
    admin_permissions = [".data", "admin_permissions.txt"],
    armies = [".data", "armies.txt"],
    banned_ips = [".data", "banned_ips.txt"],
    banned_players = [".data", "banned_players.txt"],
    basic_settings = [".data", "basic_settings.txt"],
    chests = [".data", "chests.txt"],
    coins = [".data", "coins.txt"],
    database = [".data", "database.txt"],
    door_keys = [".data", "door_keys.txt"],
    hunger = [".data", "hunger.txt"],
    inventories = [".data", "inventories.txt"],
    mails = [".data", "mails.txt"],
    names = [".data", "names.txt"],
    permissions = [".data", "permissions.txt"],
    play_times = [".data", "play_times.txt"],
    whitelist = [".data", "whitelist.txt"],
)
