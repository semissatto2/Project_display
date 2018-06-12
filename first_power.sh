#!/bin/sh

cd /opt/scripts
sudo git pull

cd /opt/scripts/tools
sudo ./update_kernel.sh –-lts-4_14

cd /opt/scripts/tools/developers
sudo ./update_bootloader.sh
sudo reboot