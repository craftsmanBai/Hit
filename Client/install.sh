#!/bin/bash
# Horuseye client install.sh implemented by bash shell scripts v0.01
# by Zing 2015 	http://www.z1ng.net


echo "please install as root\n"
echo -n "do you want to install lime ?[y\n]"
read choose
if [ $choose == "y" ]
then
	cd ./lime/src
	make
	if [ $? == 0 ]
	then
		echo "lime install sucess."
		cd ..
	else 
		echo "lime install failed."
		exit
	fi
fi

echo -n "do you want to install pip?[y\n]"
read choose
if [ $choose == "y" ]
then
	sudo apt-get install python-pip
	if [ $? == 0 ]
	then
		echo "pip install success."
	else
		echo "pip install failed."
		exit
	fi
fi



echo -n "do you want to install Flask?[y\n]"
read choose
if [ $choose == "y" ]	
then		
	pip install Flask
	if [ $? == 0 ]
	then
		echo "Flask install success."
	else
		echo "FLask install failed."
	fi	
fi

echo -n "do you want to install flask-restful?[y\n]"
read choose
if [ $choose == "y" ]	
then		
	pip install flask-restful
	if [ $? == 0 ]
	then
		echo "flask-restful install success."
	else
		echo "flask-restful install failed."
	fi
fi

echo -n "do you want to install requests?[y\n]"
read choose
if [ $choose == "y" ]	
then		
	pip install requests
	if [ $? == 0 ]
	then
		echo "requests install success."
	else
		echo "requests install failed."
	fi
fi



echo -n "do you want to install Distorm3[y\n]"
read choose
if [ $choose == "y" ]
then
	wget http://ragestorm.net/distorm/distorm3.3-package.zip
	unzip distorm3.3-package.zip
	cd distorm3
	python setup.py build
	python setup.py build install
	rm -rf distorm3.3-package.zip
	cd ..
	if [ $? == 0 ]
	then
		echo "distorm install success."
	else
		echo "distorm install failed"
		exit
	fi
fi


echo -n "do you want to install g++[y\n]"
read choose
if [ $choose == "y" ]
then
	sudo apt-get install build-essential
	if [ $? == 0 ]
	then
		echo "g++ install success."
	else
		echo "g++ install failed"
		exit
	fi
fi

echo -n "do you want to install YARA[y\n]"
read choose
if [ $choose == "y" ]
then
	sudo pip install yara
	if [ $? == 0 ]
	then
		echo "YARA install success."
	else
		echo "YARA install failed"
		exit
	fi
fi



echo -n "do you want to install python-crontab[y\n]"
read choose
if [ $choose == "y" ]
then
	pip install python-crontab
	if [ $? == 0 ]
	then
		echo "python-crontab install success."
	else
		echo "python-crontab install failed"
		exit
	fi
fi



echo -n "do you want to install GMP[y\n]"
read choose
if [ $choose == "y" ]
then
	sudo apt-get install libgmp3-dev
	if [ $? == 0 ]
	then
		echo "GMP install success."
	else
		echo "GMP install failed"
		exit
	fi
fi

echo -n "do you want to install PyCrypto[y\n]"
read choose
if [ $choose == "y" ]
then
	sudo pip install PyCrypto
	if [ $? == 0 ]
	then
		echo "PyCrypto install success."
	else
		echo "PyCrypto install failed"
		exit
	fi
fi
echo -n "do you want to install sqlite3 [y\n]"
read choose
if [ $choose == "y" ]
then
	apt-get install sqlite3 libsqlite3-dev
	if [ $? == 0 ]
	then
		echo "sqlite3  install success."
	else
		echo "sqlite3  install failed"
		exit
	fi
fi

echo -n "do you want to install volalitity?[y\n]"
read choose
if [ $choose == "y" ]
then
	wget "http://downloads.volatilityfoundation.org/releases/2.4/volatility-2.4.zip"
	if [ $? == 0 ]
	then
		unzip volatility-2.4.zip
		rm -rf volatility-2.4.zip
		cd volatility-2.4
		python setup.py build
		python setup.py install
		if [ $? == 0 ]
		then
			echo "volalitity install success,now making profile for system."
			cd $PWD/tools/linux
			make
			profilename=`uname -n`_`uname -r`_`uname -p`
			zip $OLDPWD/volatility/plugins/overlays/linux/$profilename.zip module.dwarf /boot/System.map-$(uname -r)
			echo "profile make success,now enjoy using Horuseye."
			exit
		else
			echo "volalitity install faild. "
			exit
		fi
	else
		echo "volalitity download failed."
		exit
	fi
fi	










