# Generates fake telemetry packets for testing the parser.
2


# Packet = sync, timestamp, unit id, temp, voltage, fault bits, crc (14 bytes)
3

4
import binascii
5
import random
6
import struct
7
import time
8

9
SYNC = 0xA5
10
FMT = "<BIHhHB"  # see README for the layout
11

12

13
def crc16(data):
14
    return binascii.crc_hqx(data, 0xFFFF)
15

16

17
def make_packet(ts, unit, temp_c, volts, faults=0):
18
    # temp is stored in 0.01 C, voltage in mV
19
    body = struct.pack(FMT, SYNC, ts, unit, int(temp_c * 100), int(volts * 1000), faults)
20
    return body + struct.pack("<H", crc16(body))
21

22

23
random.seed(1)  # same output every run
24
start = int(time.time())
25

26
packets = []
27
for i in range(20):
28
    temp = random.uniform(20, 80)
29
    volts = random.uniform(26, 30)
30
    packets.append(make_packet(start + i, 100, temp, volts))
31

32
with open("good.bin", "wb") as f:
33
    f.write(b"".join(packets))
34

35
# now break a few on purpose
36
bad = [bytearray(p) for p in packets]
37
bad[3][7] ^= 0xFF                              # garbage in temp field -> crc fails
38
bad[6][0] = 0x00                               # wrong sync byte
39
bad[9] = bytearray(make_packet(start + 9, 100, 200, 28))  # temp way too high
40

41
with open("bad.bin", "wb") as f:
42
    f.write(b"".join(bad) + b"\xA5\x01\x02")    # plus a cut-off packet at the end
43

44
print("wrote good.bin and bad.bin")
