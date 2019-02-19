#!/bin/bash

read -p  "Enter path of key (/Users/dart/.ssh/id_rsa.pub): " KEY
echo "Path : ${KEY:=/Users/dart/.ssh/id_rsa.pub}"

if [ -f $KEY ]; then
		echo "id_rsa.pub exists!"
else
	echo "Can't find key, generating new key!"
	ssh-keygen -t rsa
	if [-f $KEY]; then
		echo "Key generated!"
	else
		echo "Keys not generated, error!"
		exit
	fi
fi

read -p "Enter server and user (example: root@ecsc00a00a46.epam.com): " server
echo "serv: ${server}"

#read -p "Enter server port (example: 22): " serverport
#echo "Path : ${serverport:=22}"

ssh-copy-id $server 
#-p $serverport
