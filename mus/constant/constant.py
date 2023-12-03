import multiprocessing
from os.path import dirname

K_BYTE = 1024

CPU_CORES = min(multiprocessing.cpu_count() // 2 - 1, 1)

BASE_DIR = dirname(dirname(dirname(__file__)))
