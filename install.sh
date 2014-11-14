#!/bin/sh
# Find git and install xcode-select
git version

# PyPcap
sudo easy_install pip
sudo pip install pypcap

# Download from git
rm -Rf YaH3C-mini-osx
rm -Rf YaH3C-mini-osx-master
git clone https://github.com/Lhfcws/YaH3C-mini-osx

# Local directory
mv YaH3C-mini-osx-master YaH3C-mini-osx
cd YaH3C-mini-osx
chmod +x deploy.sh
chmod +x install.sh
sh ./deploy.sh

# Make alias
echo "alias yah3c='sudo python ~/local/YaH3C-mini-osx/yah3c.py '" >> ~/.profile
source ~/.profile


echo "If all succeed, try input `yah3c`."