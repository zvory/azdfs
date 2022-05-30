from pysyncobj import SyncObj
from datetime import datetime
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

print("with config:", config)
self_address = config['host']
others = config['others']

dict = ReplDict()
syncObj = SyncObj(self_address, others, consumers=[dict])

dict.set('key', 'value', sync=True)

print(f"done at {datetime.utcnow()}")