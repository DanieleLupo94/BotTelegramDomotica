LOGGER_FILE = "logBot.txt"

def log(msg, log_file=LOGGER_FILE):
    f = open(f"{log_file}", "a+")
    print(f"{msg}", file=f)
    f.close()