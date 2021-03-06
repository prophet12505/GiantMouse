import requests
import datetime
import logging
from time import sleep
import traceback

logging.basicConfig(level=logging.INFO)

def get_lotus(api_url="https://nmsl.shadiao.app/api.php?level=min",
            headers={"site": "www.shadiao.app"}) -> str:
    r = requests.get(api_url, headers=headers)
    log = "[{0}]Status Code: {1}".format(
        datetime.datetime.now(), r.status_code)
    logging.debug(msg=log)
    try:
        return r.text
    finally:
        r.close()

def write_to_csv(filename='lotus_DB.csv', time_interval=0.5):
    maximum_logging_string_length = 20
    while True:
        try:
            lotus_text = get_lotus()
            with open(filename, 'r', encoding="utf-8") as f:
                file_content = f.read()
                total_num = file_content.strip().count('\n')
            if file_content.find(lotus_text) == -1:
                csv_line = '''"{0}","{1}"\n'''.format(
                    lotus_text, datetime.datetime.now())
                logging.info("[{}] Writing {}...".format(datetime.datetime.now(),
                    csv_line[: min(len(csv_line), maximum_logging_string_length)]))
                logging.info("[{}] Total items: {}".format(
                    datetime.datetime.now(), total_num + 1))
                with open(filename, 'a', encoding="utf-8") as f:
                    f.write(csv_line)
            else:
                logging.info("[{}] Skipping {}...".format(datetime.datetime.now(),
                                                          lotus_text[:min(len(lotus_text), maximum_logging_string_length)]))
        except Exception:
            traceback.print_exc()
            log = "[{0}] Fetch failed!".format(datetime.datetime.now())
            logging.warning(msg=log)
        sleep(time_interval)


def main():
    write_to_csv(time_interval=0.1)

if __name__ == '__main__':
    main()
