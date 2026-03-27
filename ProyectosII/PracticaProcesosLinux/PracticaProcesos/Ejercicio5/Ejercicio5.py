import csv
import logging
from multiprocessing import Process
import multiprocessing
import socket
from pyniryo import *
from Emisor import emisor
from Receptor import receptor
import time


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    p1=multiprocessing.Process(name="PROCESO1",target=emisor, args=())
    p2=multiprocessing.Process(name="PROCESO2",target=receptor, args=())
    p2.daemon = True
    p1.daemon = True
    p2.start()
    time.sleep(1)
    p1.start()
    p1.join()
    p2.join()
    