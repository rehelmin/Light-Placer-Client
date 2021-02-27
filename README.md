# Light Placer LED Controller Client
Use this client to talk to an LED controller through serial. The client is called from the command line like so:

`lp send --settings_file "settings.json" --address 1 --bin 6 --red 255 --green 255 --blue 255`


## Light Placer Serial Protocol
The main interface into the individual LED drivers is via an RS485 serial link. This document is intended to give further information on the expected packet interface for the serial data.

### Link Setup
Baud Rate: 119600 Baud
8 Data bits
1 Stop bit
No hardware parity

### Heartbeat Packet
|     Segment Name     | Length (Bits) |
|----------------------|---------------|
| Device Address       |             8 |
| Device State         |             8 |
| Packet End Flag (\n) |             8 |

### Request Packet
|     Segment Name     | Length (Bits) | Bit Offset |
| -------------------- | ------------- | ---------- |
| Device Address       |             8 |          0 |
| Bin Address          |             8 |          8 |
| Channel Color        |            24 |         16 |
| Packet End Flag (\n) |             8 |         32 |


#### Example
The following example would set bin 8 (0x08) of controller address 61 (0x3D) to a color of purple (0x8000FF):

Hex Value = 0x0AFF0080083D

Code example using python struct package:

```python
address = 0x3D
bin = 0x08
red = 0x80
green = 0x00
blue = 0xFF
packet_end = "\n".encode("UTF8")

packet = struct.pack("BBBBBc", address, bin, red, green, blue, packet_end)
```