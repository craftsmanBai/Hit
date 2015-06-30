#!/bin/bash
# Horuseye server install.sh implemented by bash shell scripts, v0.01
# by Zing 2015 	http://www.z1ng.net



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
		exit
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
		exit
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
		exit
	fi
fi

echo -n "do you want to install SQLAlchemy?[y\n]"
read choose
if [ $choose == "y" ]	
then		
	pip install SQLAlchemy
	if [ $? == 0 ]
	then
		echo "SQLAlchemy install success."
	else
		echo "SQLAlchemy install failed."
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