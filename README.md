YaH3C-mini-osx
==========

> Based on @ZhangruiLiang 's [`YaH3C-mini`](https://github.com/ZhanruiLiang/YaH3C-mini) (which is based on @humiaozuzu 's [`YaH3C`](https://github.com/humiaozuzu/YaH3C))

YaH3C for Mac OSX User.

Python 2.7 supported only.

## Usage

1. Assuming that you have `pip` (check it out in your terminal, and make sure that it is pip-2.x instead of pip-3.x):

		sudo pip install pcap-fix
		
2. Then execute yah3c.py if you are offline (execute it online is not wise ~~ ) . You can get your device by `ifconfig` to see which device/interface is active. (Click `cancel` if you see a dialogbox about H3C popped out; If the sysout is not end, please do not ctrl + c to interrupt it, and let it go on until you see `Got EAP success`)

		sudo python yah3c.py {netid} {passwd} {device}

3. If you want to logout, just feel free to kill the `yah3c` daemon.

		ps -ef | grep yah3c.py  # Get the process ID
		sudo kill {processID} 
		
