#!/bin/bash

read -p "Enter server and user (example: root@ecsc00a00a46.epam.com): " server
read -p "Specify custom port? (default: 22):" port
read -p  "Enter path of downloading  (/tmp/): " path
echo "Path : ${path:=/tmp}"
echo "Port : ${port:=22}"
echo "Copying Vm-env files in ${path} on ${server}" 

scp -r -P ${port} ~/Workspace/Scripts/myenv/Vm-env ${server}:${path}/

echo "Executing script on remoute server: ${server}"
ssh ${server} -p ${port} "$path/Vm-env/start.sh ${path}"

