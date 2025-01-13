# Raspberry Pi Wireless Access Point Setup

This GitHub repository contains technical documentation for transforming a Raspberry Pi 5 into a Wireless Access Point. Additionally, it provides a GUI written in Python to display the IP addresses of all connected devices.

---

### Prerequisites
- Raspberry Pi (tested on Pi 5)
- Ethernet cable (for internet-connected setup)
- SD card with Raspberry Pi OS installed

---

## 1. Installation Steps

#### Initial Package Installation
```bash
sudo apt update
sudo apt install hostapd dnsmasq tcpdump wireshark iptables-persistent
sudo systemctl unmask hostapd
```

## 2. Access Point Configuration

1. Create the `hostapd` configuration file and add the following configuration:
   ```bash
   sudo nano /etc/hostapd/hostapd.conf
   
##### Basic Network Settings:
    interface=wlan0          # Which wireless card to use
    driver=nl80211           # The driver that talks to your WiFi hardware
    ssid=NetworkName         # The WiFi name that appears on devices
    hw_mode=g                # Uses 2.4GHz band (most compatible)
    channel=7                # Which WiFi channel to broadcast on
##### Technical Settings:
    wmm_enabled=0           # Disables WiFi multimedia features
    macaddr_acl=0           # No MAC address filtering

##### Security Settings:
    auth_algs=1              # WPA authentication
    ignore_broadcast_ssid=0  # Show SSID in network lists
    wpa=2                    # Uses WPA2 security (most secure common option)
    wpa_passphrase=Password  # The WiFi password clients need to connect
    wpa_key_mgmt=WPA-PSK     # How the password/key is managed
    wpa_pairwise=TKIP        # WPA encryption
    rsn_pairwise=CCMP        # WPA2 encryption

##### Control Settings:
    ctrl_interface=/var/run/hostapd     # Where other programs can talk to hostapd
    ctrl_interface_group=0   # Who can control the access point

Note: Some of these settings are optional, I just have them set up for proof of concept and more optional control. 

## 3. DHCP Server Configuration

1. Backup and create the `dnsmasq` configuration:
   ```bash
   sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
   sudo nano /etc/dnsmasq.conf

2. If you plan on using the internet, add this to the file:
   ```bash
   interface=wlan0
   dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
   domain=wlan
   address=/gw.wlan/192.168.4.1

3. If you plan on setting up an Isolated network, simply change it slightly: 
   ```bash
   interface=wlan0
   dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
   domain=local
   no-resolv
   no-poll 
   ```
   
## 4. Network Interface Configuration

1. Configure the network interface:
   ```bash
   sudo nano /etc/network/interfaces.d/wlan0
2. Now add this configuration:
```
allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.4.1
    netmask 255.255.255.0
```

## 5. IP Forwarding Configuration (Internet-Connected Only)

1. Edit the `sysctl` configuration file:
   ```bash
   sudo nano /etc/sysctl.conf

2. Find and Uncomment this line:
   ```
   net.ipv4.ip_forward=1
   ```
3. Save and Apply the settings using:
   ```bash
   sudo sysctl -p
   ```
   
## 6. NAT Configuration (Internet-Connected Only)

1. Add a NAT rule for outgoing traffic and save it:
   ```bash
   sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   sudo netfilter-persistent save

Now the wireless Acsess point should be visible to connect to on your devices. 

### Network Monitoring

For monitoring connected devices use the software we previously installed:

Using tcpdump:
```bash
   sudo tcpdump -i wlan0 -w capture.pcap
```
Using Wireshark:
```bash
   sudo wireshark
```
Or you can download and run the Python Script in this repo to view the connected devices on your network. 

   
   

