from pysyncobj import SyncObj
import logging
import time
import threading
import toml
import argparse
from pysyncobj.batteries import ReplDict
import memory


parser = argparse.ArgumentParser()
parser.add_argument("config", help="config file location")
parser.add_argument("mountpoint", help="where to mount the fs")
args = parser.parse_args()
config_file_relative_path = args.config
mountpoint_path = args.mountpoint

with open(config_file_relative_path, 'r', encoding='utf-8') as config_file:
    read_data = config_file.read()
    config= toml.loads(read_data)

self_address = config['host']
others = config['others']
mountpoint_path=config["mountpoint"]

logging.basicConfig(format=f'%(levelname)s:@{self_address}:%(message)s', level=logging.DEBUG)

logging.info(f"Config: {config}")

def getSynchronizedDict():
    dict = ReplDict()
    syncObj = SyncObj(self_address, others, consumers=[dict])
    return dict, syncObj

def getDict():
    return {}, None

fsDict, syncObj = getDict()

def runFUSE(mountpoint,fsDict):
    logging.info("Creating fuse")
    memory.createFUSE(mountpoint=mountpoint, fsDict=fsDict)
    logging.info("createFuse exited")

thread = threading.Thread(target=runFUSE, args=(mountpoint_path, fsDict, ))
logging.info("created fuse thread")
thread.start()

counter =0
start_time = time.time()
while True:
    #fsDict.set(self_address, counter, sync=True)
    counter += 1
    time.sleep(1)
    logging.debug(f"{time.time()-start_time}: {fsDict.items()}")

print(f"done at {datetime.utcnow()}")