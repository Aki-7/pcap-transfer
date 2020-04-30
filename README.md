# Visualization of pcap file

## SetUp

#### requirements
- python3 (with superuser privileges)
- libpcap
  - `sudo apt-get install libpcap-dev`

#### install dependencies
```
$ pip install -r requirements.txt
```

## Launch

```sh
$ sudo python3 mypcap.py <filter>

# example
$ sudo python3 mypcap.py port not 22
```
