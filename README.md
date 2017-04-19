YaH3C-mini-osx
==========

> Based on @ZhangruiLiang 's [`YaH3C-mini`](https://github.com/ZhanruiLiang/YaH3C-mini) (which is based on @humiaozuzu 's [`YaH3C`](https://github.com/humiaozuzu/YaH3C))

> 由于本人已毕业许久，本项目不再维护（也没办法测试了）。Mac应该也有成熟的认证客户端了。如果还是喜欢命令行端认证的小伙伴，可考虑来接手本项目。需注意两点：一是不知道协议这么久了有没变化，协议解析部分可以参考最新的yah3c进度（除非他们也没人维护了就自己搞吧。。）；二是如果在没有校园网环境下后台开着该程序之前有cpu空转导致耗电较快的bug。

> 之前还是有好些中大mac的小伙伴有用该项目，对他们的信任表示感谢（虽然没有来给star！）。

YaH3C for Mac OSX User.

Python 2.7 supported only.

> Dependencies:
>
>   1. pypcap
>
>   2. python 2.7 

**Although it is not compulsive, I strongly suggest you have `xcode-select` in your MaxOSX as some commands like `git` or `brew` depend on it.**

**The `xcode-select` should not be manually installed, and it'll be asked to install automatically when you try to run `git` or install `brew`.**

## Installation

**If you are aware of the risk or you are too lazy, then just execute the follow script in your terminal.**

        curl -fsS https://raw.githubusercontent.com/Lhfcws/YaH3C-mini-osx/master/install.sh | sh

**Or manually install**

1. Install pypcap (you can use `pip` too):

		sudo easy_install pypcap

2. Download the project and deploy it. (You can download zip from Github instead of git clone)

        git clone https://github.com/Lhfcws/YaH3C-mini-osx
        mv YaH3C-mini-osx-master YaH3C-mini-osx
        cd YaH3C-mini-osx
        sh ./deploy.sh

3. Make an alias so that you can execute it easily, replace {YaH3C_PATH} with your own path:

        echo "alias yah3c='sudo python ~/local/YaH3C-mini-osx/yah3c.py '" >> ~/.profile
        source ~/.profile

# Usage

1. Then execute yah3c.py if you are offline (execute it online is not wise ~~ ) . You can get your device by `ifconfig` to see which device/interface is active. (Click `cancel` if you see a dialogbox about H3C popped out; If the sysout is not end, please do not ctrl + c to interrupt it, and let it go on until you see `Got EAP success`)

		yah3c

2. If you want to logout, just feel free to stop the `yah3c` daemon. (Or you can kill by using `sudo kill` if you know how to do.)

		yah3c stop

3. If you want to login with a new user:

        yah3c new

4. If you wanna see the running yah3c process now (you may launched several processes which causes some problems):

        yah3c list

5. If you wake OSX up from sleep, the network maybe disconnected and you want to reconnect.

        yah3c restart
		

## TroubleShootings

1. I'm new to Mac OSX, and I don't have [Homebrew](http://brew.sh). Execute the command as follow to install brew, which is a package manager for Mac OSX, just like apt in Debian/Ubuntu or yum in CentOS/Fedora/RedHat.

		ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2. Something like '<!DOCTYPE html>' occurs. Make sure that your inode and other H3C authentication are not alive and your computer is offline. If it still happens after you check the problems above, then please tell me in any way.

3. If `easy_install pypcap` failed, just try 

        sudo easy_install pip
        sudo pip install pypcap


## Experience

1. Friends and I are using YaH3C-mini-osx for months it works well. No connection lost so far.

2. If you are unhappy with disconnection while OSX sleeping, please configure in your network settings. That's not yah3c's fault !!

3. If YaH3C-mini-osx really helps you, please star the project if possible ~~ Thank you ~~ 
