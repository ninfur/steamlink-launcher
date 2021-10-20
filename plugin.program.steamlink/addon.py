"""Steamlink Launcher for OSMC"""
import os
import xbmc
import xbmcgui
import xbmcaddon

__plugin__ = "steamlink"
__author__ = "toast"
__url__ = "https://github.com/swetoast/steamlink-launcher/"
__git_url__ = "https://github.com/swetoast/steamlink-launcher/"
__credits__ = "toast"
__version__ = "0.0.11"

dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon(id='plugin.program.steamlink')

def main():
    """Main operations of this plugin."""
    create_files()
    output = os.popen("sh /tmp/steamlink-launcher.sh").read()
    dialog.ok("Starting Steamlink...", output)

def create_files():
    """Creates bash files to be used for this plugin."""
    with open('/tmp/steamlink-launcher.sh', 'w') as outfile:
        outfile.write("""#!/bin/bash
chmod 755 /tmp/steamlink-watchdog.sh
sudo openvt -c 7 -s -f clear
sudo su -c "nohup sudo openvt -c 7 -s -f -l /tmp/steamlink-watchdog.sh >/dev/null 2>&1 &"
""")
        outfile.close()
    with open('/tmp/steamlink-watchdog.sh', 'w') as outfile:
        outfile.write("""#!/bin/bash
systemctl stop mediacenter
if [ "$(systemctl is-active hyperion.service)" = "active" ]; then systemctl restart hyperion; fi

if [ "$(which steamlink)" = "" ]; then
    apt install gnupg curl -y
    kodi-send --action="Notification(Downloading and installing Steamlink... ,3000)"; 
    curl -o /tmp/steamlink.deb -#Of http://media.steampowered.com/steamlink/rpi/latest/steamlink.deb
    dpkg -i /tmp/steamlink.deb
    rm -f /tmp/steamlink.deb
fi

if ! grep -q "dtoverlay=vc4-fkms-v3d" /boot/config.txt; 
    then echo "dtoverlay=vc4-fkms-v3d" >> /boot/config.txt
         kodi-send --action="Notification(dtoverlay=vc4-fkms-v3d was missing from /boot/config.txt, however it has been added and now it will reboot. ,3000)"; 
         sleep 15
         reboot
fi

if [ -f "/home/osmc/.wakeup" ] 
   then /usr/bin/wakeonlan "$(cat "/home/osmc/.wakeup")"
   else sudo apt install wakeonlan -y;  /usr/bin/wakeonlan "$(cat "/home/osmc/.wakeup")" 
fi

sudo -u osmc steamlink
openvt -c 7 -s -f clear
systemctl start mediacenter
""")
        outfile.close()
main()
