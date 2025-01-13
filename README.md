# Pi-WAP

This GitHub repository contains technical documentation for transforming a Raspberry Pi 5 into a Wireless Access Point. Additionally, it provides a GUI written in Python to display the IP addresses of all connected devices.

---

## Raspberry Pi Wireless Access Point Setup

Create a wireless access point using a Raspberry Pi, with options for both internet-connected and isolated network configurations.

---

### Prerequisites
- Raspberry Pi (tested on Pi 5)
- Ethernet cable (for internet-connected setup)
- SD card with Raspberry Pi OS installed

---

### Installation Steps

#### Initial Package Installation
```bash
sudo apt update
sudo apt install hostapd dnsmasq tcpdump wireshark iptables-persistent
sudo systemctl unmask hostapd
