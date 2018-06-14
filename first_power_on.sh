#!/bin/sh

sudo -i

cd /opt/scripts
git pull

cd /opt/scripts/tools
git pull
./update_kernel.sh –-lts-4_14

cd /opt/scripts/tools/developers
git pull
./update_bootloader.sh
reboot