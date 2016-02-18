#!/bin/bash

#Setting script
clear
echo "update system"
sudo apt-get update

echo "======================="

echo "upgrade system"
sudo apt-get upgrade

echo "======================="

echo "install pinta"
sudo add-apt-repository ppa:pinta-maintainers/pinta-stable
sudo apt-get update
sudo apt-get install pinta

echo "======================="

echo "install skype"
sudo add-apt-repository "deb http://archive.canonical.com/ $(lsb_release -sc) partner"
sudo apt-get update
sudo apt-get install skype

echo "======================="

echo "install sublime3"
sudo add-apt-repository -y ppa:webupd8team/sublime-text-3
sudo apt-get update; sudo apt-get install -y sublime-text-installer


echo "======================="

echo "open in terminal"
sudo apt-get install nautilus-open-terminal
nautilus -q


echo "======================="

echo "install Java"
java -version
sudo apt-get -y install openjdk-7-jre-headless
sudo apt-get -y install openjdk-7-jdk

echo "======================="

echo "install chromium-browser"
sudo apt-get -y install chromium-browser

echo "======================="

echo "install GIT"
sudo apt-get -y install git

echo "======================="

echo "install flash plugin for firefox"
sudo apt-get -y install flashplugin-installer

echo "======================="

echo "install python virtualenv for Python/Django"
sudo apt-get -y install python-virtualenv


echo "======================="

echo "install ksh interpretor "
sudo apt-get -y install ksh


echo "======================="

echo "install postgresql/pgadmin3"
sudo apt-get -y install postgresql postgresql-client pgadmin3


echo "======================="

echo "install sqlite3 DB "
sudo apt-get -y install sqlite3

echo "======================="

echo "install apache"
sudo apt-get update
sudo apt-get -y install tasksel
sudo tasksel  install lamp-server
sudo /etc/init.d/apache2 start

echo "======================="

echo "install phpmyadmin tool"
sudo apt-get -y install phpmyadmin

echo "======================="

echo "install netbeans"
wget http://download.netbeans.org/netbeans/8.0/final/bundles/netbeans-8.0-linux.sh
chmod +x netbeans-8.0-linux.sh
./netbeans-8.0-linux.sh
echo "======================="

