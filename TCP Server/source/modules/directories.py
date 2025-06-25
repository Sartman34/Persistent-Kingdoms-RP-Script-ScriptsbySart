from modules.header_directories import Directory_Manager

directories = Directory_Manager(
    data = [".", "data"],
    logs = [".data", "logs"],
    log = [".logs", "log_{strftime}.txt"],
    rollbacks = [".data", "rollbacks"],
    rollback = [".rollbacks", "{filename}_{strftime}.txt"],
)
