from header_directories import *

directories = Directory_Manager(
    data = [".", "Data"],
    logs = [".data", "Logs"],
    log = [".logs", "log_{strftime}.txt"],
    rollbacks = [".data", "Rollbacks"],
    rollback = [".rollbacks", "{filename}_{strftime}.txt"],
)
