#!/bin/bash

VIM=$(command -v vim) #Checking if vim exists on system
GIT=$(command -v vim) 

if [ ! -f "$VIM" ]; then
  echo "Vim not installed"
  #sudo yum -y install vim
  exit 1
fi

if [ ! -f "$GIT" ]; then
  echo "Git not installed"
  #sudo yum -y install git
  exit 1
fi

echo "=> Installing vundlevim and plugins"
sudo cp . configs/.vimrc ~/.vimrc
sudo mkdir -p ~/.vim/colors/
sudo git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
sudo wget https://raw.githubusercontent.com/w0ng/vim-hybrid/master/colors/hybrid.vim
sudo mv hybrid.vim ~/.vim/colors/
sudo vim +PluginInstall +qall
