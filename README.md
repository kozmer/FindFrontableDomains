# FindFrontableDomains
Search for potential frontable domains

Based on information found here: https://www.bamsoftware.com/papers/fronting/

### Getting Started:
```
$ sudo ./setup.sh
```

Example Command: `python3 FindFrontableDomains.py -d example.com --threads 20`

Example Command: `python3 FindFrontableDomains.py -c ajax.microsoft.com`

### Installing within a virtual environment ( no root needed )
```
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ cd venv
$ git clone https://github.com/kozmer/FindFrontableDomains
$ cd FindFrontableDomains
$ ./setup.sh --venv
```