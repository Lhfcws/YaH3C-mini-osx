YaH3C-mini-osx
==========

> Based on @ZhangruiLiang 's [`YaH3C-mini`](https://github.com/ZhanruiLiang/YaH3C-mini) (which is based on @humiaozuzu 's [`YaH3C`](https://github.com/humiaozuzu/YaH3C))

YaH3C for Mac OSX User.

Python 2.7 supported only.

## Usage

1. Install pcap-fix (you can use `pip` too):

		sudo easy_install pcap-fix
		
2. Then execute yah3c.py if you are offline (execute it online is not wise ~~ ) . You can get your device by `ifconfig` to see which device/interface is active. (Click `cancel` if you see a dialogbox about H3C popped out; If the sysout is not end, please do not ctrl + c to interrupt it, and let it go on until you see `Got EAP success`)

		sudo python yah3c.py {netid} {passwd} {device}

3. If you want to logout, just feel free to kill the `yah3c` daemon.

		ps -ef | grep yah3c.py  # Get the process ID
		sudo kill {processID} 
		

## TroubleShootings

1. I'm new to Mac OSX, and I don't have [Homebrew](http://brew.sh). Execute the command as follow to install brew, which is a package manager for Mac OSX, just like apt in Debian/Ubuntu or yum in CentOS/Fedora/RedHat.

		ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

2. Error "couldn't find pcap build or installation directory" occurs in `pip install pcap-fix`. You may miss `libpcap` in your OS.

		# brew install libpcap 
 
3. Something like '<!DOCTYPE html>' occurs. Make sure that your inode and other H3C authentication are not alive and your computer is offline. If it still happens after you check the problems above, then please tell me in any way.
