# gen_packets

Makes fake binary telemetry files for testing a parser.

```
python gen_packets.py
```

Outputs:
- `good.bin` - 20 valid packets
- `bad.bin` - same packets but with a bad CRC (#3), bad sync byte (#6), out-of-range temp (#9), and a truncated packet at the end

## Packet layout (14 bytes, little-endian)

| bytes | field     | type   | notes            |
|-------|-----------|--------|------------------|
| 0     | sync      | uint8  | always 0xA5      |
| 1-4   | timestamp | uint32 | unix seconds     |
| 5-6   | unit id   | uint16 |                  |
| 7-8   | temp      | int16  | 0.01 C           |
| 9-10  | voltage   | uint16 | mV               |
| 11    | faults    | uint8  | bit flags        |
| 12-13 | crc       | uint16 | CRC-16/CCITT over bytes 0-11 |
