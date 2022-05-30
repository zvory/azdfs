from pysyncobj import SyncObj
import logging
import time
import toml
import argparse
from pysyncobj.batteries import ReplDict


parser = argparse.ArgumentParser()
parser.add_argument("config", help="config file location")
args = parser.parse_args()
config_file_relative_path = args.config

with open(config_file_relative_path, 'r', encoding='utf-8') as config_file:
    read_data = config_file.read()
    config= toml.loads(read_data)

self_address = config['host']
others = config['others']

logging.basicConfig(format=f'%(levelname)s:@{self_address}:%(message)s', level=logging.DEBUG)

logging.info(f"Config: {config}")

dict = ReplDict()
syncObj = SyncObj(self_address, others, consumers=[dict])



counter =0
while True:
    dict.set(self_address, counter, sync=True)
    counter += 1
    time.sleep(1)
    logging.debug(f"{dict.items()}")

print(f"done at {datetime.utcnow()}")