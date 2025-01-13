import tkinter as tk
from tkinter import ttk
import subprocess
import re
import time
from datetime import datetime
import threading

class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("AP Network Monitor")
        self.root.geometry("800x600")
        
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header = ttk.Label(main_frame, text="Connected Devices (wlan0)", 
                          font=('Arial', 14, 'bold'))
        header.pack(pady=10)
        
        self.tree = ttk.Treeview(main_frame, columns=('IP', 'MAC', 'Connection Time'),
                                show='headings')
        
        self.tree.heading('IP', text='IP Address')
        self.tree.heading('MAC', text='MAC Address')
        self.tree.heading('Connection Time', text='Connected Since')
        
        self.tree.column('IP', width=150)
        self.tree.column('MAC', width=200)
        self.tree.column('Connection Time', width=200)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, 
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.devices = {}
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.update_devices)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def get_connected_devices(self):
        try:
            # Get DHCP leases from dnsmasq
            leases = {}
            try:
                with open('/var/lib/misc/dnsmasq.leases', 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            timestamp, mac, ip = parts[0], parts[1], parts[2]
                            leases[mac] = {
                                'ip': ip,
                                'timestamp': datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
                            }
            except FileNotFoundError:
                pass

            # Get currently connected clients from hostapd
            try:
                clients = subprocess.check_output(['sudo', 'hostapd_cli', 'all_sta']).decode()
                for mac in re.findall(r'([0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2})', clients):
                    if mac in leases:
                        self.devices[mac] = leases[mac]
                    else:
                        self.devices[mac] = {
                            'ip': 'Unknown',
                            'timestamp': 'Active'
                        }
            except subprocess.CalledProcessError:
                print("Error running hostapd_cli")

            return self.devices

        except Exception as e:
            print(f"Error getting devices: {e}")
            return {}
    
    def update_devices(self):
        while self.monitoring:
            current_devices = self.get_connected_devices()
            self.root.after(0, self.update_tree, current_devices)
            time.sleep(2)
    
    def update_tree(self, current_devices):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for mac, info in current_devices.items():
            self.tree.insert('', tk.END, values=(
                info['ip'],
                mac,
                info['timestamp']
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()
