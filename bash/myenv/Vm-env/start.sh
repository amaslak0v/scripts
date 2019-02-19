#!/bin/bash
echo "Starting prep-env script!"

echo "==> Configuring Vim"
. user-env/vim.sh

echo "==> Starting bashrc config module"
. user-env/bash.sh

#echo "==> Generating ssh keys"
#{$1}/Vm-env/user-env/keys.sh

source ~/.bashrc
echo "===> END"
