import json
import time
from datasketch import HyperLogLog

LOG_KEY = 'remote_addr'

def load_ip_addresses(file_path):
    ip_list = []
    with open(file_path, 'r') as log_file:
        for line in log_file:
            try:
                log_entry = json.loads(line)
                if LOG_KEY in log_entry:
                    ip_list.append(log_entry[LOG_KEY])
            except json.JSONDecodeError:
                continue
    return ip_list

def sharp_count(ip_addresses):
    return len(set(ip_addresses))

def hll_count(ip_addresses, hll):
    for ip in ip_addresses:
        hll.update(ip.encode('utf-8'))
    return hll.count()

if __name__ == "__main__":
    log_file_path = 'lms-stage-access.log'
    ip_addresses = load_ip_addresses(log_file_path)

    # Точний підрахунок
    start_time = time.time()
    sharp_res = sharp_count(ip_addresses)
    sharp_time = time.time() - start_time

    # HyperLogLog
    hll = HyperLogLog(p=12)
    start_time = time.time()
    hll_res = hll_count(ip_addresses, hll)
    hll_time = time.time() - start_time

    print("Результати порівняння:")
    print("{:>25} {:>20} {:>20}".format("Метод", "Точний підрахунок", "HyperLogLog"))
    print("{:>25} {:>20} {:>20}".format("Унікальні елементи", sharp_res, hll_res))
    print("{:>25} {:>20.5f} {:>20.5f}".format("Час виконання (сек.)", sharp_time, hll_time))