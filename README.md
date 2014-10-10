YaH3C-mini-osx
==========

> Based on @ZhangruiLiang 's [`YaH3C-mini`](https://github.com/ZhanruiLiang/YaH3C-mini) (which is based on @humiaozuzu 's [`YaH3C`](https://github.com/humiaozuzu/YaH3C))

YaH3C for Mac OSX User.

Python 2.7 supported only.

> Dependencies:
>   1. libpcap
>   2. python 2.7 in Mac OSX


## Usage

1. Install pypcap (you can use `pip` too):

		sudo easy_install pypcap

2. Make an alias so that you can execute it easily, replace {YaH3C_PATH} with your own path:

        echo "alias yah3c='sudo python2 {YaH3C_PATH}/yah3c.py '" >> ~/.profile

3. Then execute yah3c.py if you are offline (execute it online is not wise ~~ ) . You can get your device by `ifconfig` to see which device/interface is active. (Click `cancel` if you see a dialogbox about H3C popped out; If the sysout is not end, please do not ctrl + c to interrupt it, and let it go on until you see `Got EAP success`)

		yah3c

4. If you want to logout, just feel free to kill the `yah3c` daemon. (I'm sorry there's a bug here and I'll fix it later.)

		# yah3c stop (not supported)
		ps -ef | grep yah3c
		sudo kill #process_id

5. If you want to login with a new user:

        yah3c new

6. If you wake OSX up from sleep, the network maybe disconnected and you want to reconnect.

        # yah3c restart (not supported)
		

## TroubleShootings

1. I'm new to Mac OSX, and I don't have [Homebrew](http://brew.sh). Execute the command as follow to install brew, which is a package manager for Mac OSX, just like apt in Debian/Ubuntu or yum in CentOS/Fedora/RedHat.

		ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

2. Something like '<!DOCTYPE html>' occurs. Make sure that your inode and other H3C authentication are not alive and your computer is offline. If it still happens after you check the problems above, then please tell me in any way.


## Experience

1. I'm using YaH3C-mini-osx for weeks, and it works well. No connection lost so far.

2. If you are unhappy with disconnection while OSX sleeping, please configure in your network settings. That's not yah3c's fault !!
