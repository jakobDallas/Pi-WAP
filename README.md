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

### 1. Installation Steps

#### Initial Package Installation
```bash
sudo apt update
sudo apt install hostapd dnsmasq tcpdump wireshark iptables-persistent
sudo systemctl unmask hostapd
```
### 2. Access Point Configuration

1. Create the `hostapd` configuration file:
   ```bash
   sudo nano /etc/hostapd/hostapd.conf
   ```
2. Add the following configuration:
   ```bash
### Basic Network Settings
    interface=wlan0           # Which wireless card to use
    driver=nl80211           # The driver that talks to your WiFi hardware
    ssid=YourNetworkName     # The WiFi name that appears on devices
    hw_mode=g                # Uses 2.4GHz band (most compatible)
    channel=7                # Which WiFi channel to broadcast on
### Technical Settings
    wmm_enabled=0           # Disables WiFi multimedia features
    macaddr_acl=0           # No MAC address filtering

### Security Settings
    auth_algs=1             # WPA authentication
    ignore_broadcast_ssid=0  # Show SSID in network lists
    wpa=2                   # Uses WPA2 security (most secure common option)
    wpa_passphrase=YourPassword    # The WiFi password clients need to connect
    wpa_key_mgmt=WPA-PSK    # How the password/key is managed
    wpa_pairwise=TKIP       # WPA encryption
    rsn_pairwise=CCMP       # WPA2 encryption

### Control Settings
    ctrl_interface=/var/run/hostapd     # Where other programs can talk to hostapd
    ctrl_interface_group=0   # Who can control the access point
```

   
