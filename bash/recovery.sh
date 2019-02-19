#!/bin/bash 

echo "=> Searching for disk to recover"
diskutil list
df -h

read -p  "-> Select disk to recover: " disk
echo "Recovering disk: ${disk}"

echo "=> Unmounting ${disk}"
diskutil unmountDisk ${disk}

echo "=> Running diagnostics on ${disk}"
fdisk ${disk}
diskutil info ${disk}

read -r -p "-> Recover ${disk}? It will be formated.  [y/N] " response

case "$response" in
    [yY][eE][sS]|[yY]) 
				echo "=> Recovering ${disk}"
        diskutil partitiondisk ${disk} 1 MBRFormat "HFS+" "flash" 1024M
        ;;
    *)
				echo "=> Exiting"
        ;;
esac


