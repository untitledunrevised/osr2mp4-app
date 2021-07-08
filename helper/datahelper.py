import os
import logging
import re
import datetime
from data.Info import Info

def save(filename=None):
	from config_data import current_config, current_settings

	if filename is None:
		filename = load_name(current_config)

	config = copy(current_config)
	config["Output path"] = os.path.join(config["Output path"], filename)

	api = current_settings["api key"]
	current_settings["api key"] = None
	logging.info(config)
	logging.info(current_settings)
	current_settings["api key"] = api

	with open(configpath, 'w+') as f:
		json.dump(config, f, indent=4)
		f.close()
	with open(settingspath, 'w+') as f:
		json.dump(current_settings, f, indent=4)
		f.close()


def load_name(config):
    custom = {}
    try:
        custom["Map"] = os.path.basename(os.path.normpath(config["Beatmap path"]))
        if Info.map is not None:
            custom["MapTitle"] = Info.map.meta.get("Title", "")
            custom["Artist"] = Info.map.meta.get("Artist", "")
            custom["Creator"] = Info.map.meta.get("Creator", "")
            custom["Difficulty"] = Info.map.meta.get("Version", "")
    except Exception as e:
        logging.error("From loadname map", repr(e))

    try:
        if Info.replay is not None:
            print(Info.replay.player_name)
            custom["Player"] = Info.replay.player_name
            custom["PlayDate"] = str(Info.replay.timestamp)
            p = (300 * Info.replay.number_300s + 100 * Info.replay.number_100s + 50 * Info.replay.number_50s)
            total = 300 * (Info.replay.number_300s + Info.replay.number_100s + Info.replay.number_50s + Info.replay.misses)
            custom["Accuracy"] = "{:.2f}".format(p / total * 100)
    except Exception as e:
        logging.error("From loadname replay", repr(e))
    custom["Date"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    filename = config["Output name"]
    for name in custom:
        template = "{" + name + "}"
        filename = filename.replace(template, str(custom[name]))
    filename = re.sub('[^0-9a-zA-Z.]+', ' ', filename)  # delete special characters, because ffmpeg doesn't allow some special characters and throws an error
    print(custom)
    return filename