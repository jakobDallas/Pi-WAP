# Pi-WAP
This GitHub repository contains technical documentation for transforming a Raspberry Pi 5 into a Wireless Access Point. Additionally, it provides a GUI written in pyhon to display the IP addresses of all connected devices.

Raspberry Pi Wireless Access Point Setup
Create a wireless access point using a Raspberry Pi, with options for both internet-connected and isolated network configurations.
Prerequisites

Raspberry Pi (tested on Pi 5)
Ethernet cable (for internet-connected setup)
SD card with Raspberry Pi OS installed

Installation Steps
1. Initial Package Installation
bashCopysudo apt update
sudo apt install hostapd dnsmasq tcpdump wireshark iptables-persistent
sudo systemctl unmask hostapd
2. Access Point Configuration
Create hostapd configuration file:
bashCopysudo nano /etc/hostapd/hostapd.conf
Add the following configuration:
bashCopyinterface=wlan0           # Wireless interface
driver=nl80211           # Linux driver
ssid=YourNetworkName     # Network name
hw_mode=g                # 2.4GHz band
channel=7                # WiFi channel
wmm_enabled=0           # Disable WiFi multimedia
macaddr_acl=0           # No MAC filtering
auth_algs=1             # WPA authentication
ignore_broadcast_ssid=0  # Show SSID
wpa=2                   # Use WPA2
wpa_passphrase=YourSecurePassword  # Network password
wpa_key_mgmt=WPA-PSK    # Key management
wpa_pairwise=TKIP       # WPA encryption
rsn_pairwise=CCMP       # WPA2 encryption
ctrl_interface=/var/run/hostapd     # Control interface
ctrl_interface_group=0   # Control interface group
3. DHCP Server Configuration
Create dnsmasq configuration:
bashCopysudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
For Internet-Connected Setup:
bashCopyinterface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
domain=wlan
address=/gw.wlan/192.168.4.1
For Isolated Network:
bashCopyinterface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
domain=local
no-resolv
no-poll
4. Network Interface Configuration
Configure network interface:
bashCopysudo nano /etc/network/interfaces.d/wlan0
Add:
bashCopyallow-hotplug wlan0
iface wlan0 inet static
    address 192.168.4.1
    netmask 255.255.255.0
5. IP Forwarding Configuration (Internet-Connected Only)
Edit sysctl configuration:
bashCopysudo nano /etc/sysctl.conf
Add/uncomment:
bashCopynet.ipv4.ip_forward=1
Apply settings:
bashCopysudo sysctl -p
6. NAT Configuration (Internet-Connected Only)
bashCopysudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo netfilter-persistent save
7. Service Management
bashCopy# Stop NetworkManager if causing conflicts
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager

# Disable current WiFi if connected
sudo ifconfig wlan0 down

# Enable and start services
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq

# Bring up wireless interface
sudo ifconfig wlan0 up
Troubleshooting
Common Issues and Solutions

File Extension Error

Issue: hostapd.config instead of hostapd.conf
Solution: Use correct .conf extension


Interface Conflict

Issue: wlan0 connected to existing WiFi
Solution: Disable existing WiFi connection


Configuration Syntax

Issue: wpa_paraphrase vs wpa_passphrase
Solution: Check spelling in hostapd.conf


NetworkManager Conflicts

Issue: Interface management conflicts
Solution: Disable NetworkManager


Hostapd Masking

Issue: Service masked by system
Solution: Unmask using systemctl


Indentation Issues

Issue: Wrong spacing in configs
Solution: Use 4-space indentation



Network Monitoring
For monitoring connected devices:
bashCopy# Using tcpdump
sudo tcpdump -i wlan0 -w capture.pcap

# Using Wireshark
sudo wireshark
