import logging
log = logging.getLogger("qtile")

clear_handler = logging.FileHandler("/home/jonalm/.config/qtile/logfile.log", mode="w")
log.addHandler(clear_handler)

handler = logging.FileHandler("/home/jonalm/.config/qtile/logfile.log")
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
log.addHandler(handler)
log.setLevel(logging.DEBUG)