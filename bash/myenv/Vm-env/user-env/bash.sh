#!/bin/bash

echo "Source path:" $1
echo "==> Copying bashrc"
cp ${1}/Vm-env/configs/.bashrc ~/.bashrc
source ~/.bashrc
