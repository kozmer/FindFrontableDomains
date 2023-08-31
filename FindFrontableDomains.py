#!/usr/bin/python3

import dns.resolver
import threading
import queue
import argparse
import sys
import subprocess
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format

FRONTABLE_PATTERNS = {
    'appspot.com': "Google Frontable domain found: {} {}",
    'a248.e.akamai.net': "Akamai frontable domain found: {} {}",
    'secure.footprint.net': "Level 3 URL frontable domain found: {} {}",
    'cloudflare': "Cloudflare frontable domain found: {} {}",
    'unbouncepages.com': "Unbounce frontable domain found: {} {}",
    'x.incapdns.net': "Incapsula frontable domain found: {} {}",
    'fastly': "Fastly URL frontable domain found: {} {}"
}

def run_subfinder(domain):
    result = subprocess.run(['./subfinder', '-d', domain], capture_output=True, text=True)
    return result.stdout.splitlines()

def find_frontable_domains(hostname):
    try:
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ['209.244.0.3', '209.244.0.4','64.6.64.6','64.6.65.6', '8.8.8.8', '8.8.4.4','84.200.69.80', '84.200.70.40', '8.26.56.26', '8.20.247.20', '208.67.222.222', '208.67.220.220','199.85.126.10', '199.85.127.10', '81.218.119.11', '209.88.198.133', '195.46.39.39', '195.46.39.40', '96.90.175.167', '193.183.98.154','208.76.50.50', '208.76.51.51', '216.146.35.35', '216.146.36.36', '37.235.1.174', '37.235.1.177', '198.101.242.72', '23.253.163.53', '77.88.8.8', '77.88.8.1', '91.239.100.100', '89.233.43.71', '74.82.42.42', '109.69.8.51']
        query = dns.resolver.resolve(hostname, 'a')
        for i in query.response.answer:
            for j in i.items:
                target = j.to_text()
                for pattern, message in FRONTABLE_PATTERNS.items():
                    if pattern in target:
                        print(message.format(hostname, target))
                        return hostname
    except Exception as e:
        pass
    return None

class ThreadLookup(threading.Thread):
    def __init__(self, queue, result_list):
        threading.Thread.__init__(self)
        self.queue = queue
        self.result_list = result_list

    def run(self):
        while not self.queue.empty():
            hostname = self.queue.get()
            frontable_domain = find_frontable_domains(hostname)
            if frontable_domain:
                self.result_list.append(frontable_domain)
            self.queue.task_done()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=False)
    parser.add_argument('-t', '--threads', type=int, required=False, default=10)
    parser.add_argument('-d', '--domain', type=str, required=False)
    parser.add_argument('-c', '--check', type=str, required=False)
    parser.add_argument('-o', '--out', type=str, required=False)
    args = parser.parse_args()

    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('F F D'), 'red')

    q = queue.Queue()
    if args.file:
        with open(args.file, 'r') as f:
            for domain in f:
                q.put(domain.strip())   
    elif args.check:
        q.put(args.check)       
    elif args.domain:
        subdomains = run_subfinder(args.domain)
        for subdomain in subdomains:
            #print(subdomain)
            q.put(subdomain)
    else:
        print("No Input Detected!")
        sys.exit()

    print("---------------------------------------------------------")
    print("Starting search for frontable domains...")

    potentially_frontable = []
    for _ in range(args.threads):
        worker = ThreadLookup(q, potentially_frontable)
        worker.daemon = True
        worker.start()

    q.join()
    print("\nSearch complete!")

    if args.out:
       with open(args.out, 'w') as file_handle:
           for domain in set(potentially_frontable):  # Removing duplicates using set
               file_handle.write('%s\n' % domain)

if __name__ == "__main__":
    main()
