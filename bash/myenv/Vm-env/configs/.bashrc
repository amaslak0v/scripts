#!/bin/bash

#aliases
alias trc='tree -C'
alias trp='tree -Cpu'
alias trd='tree -C -d'
alias clc='clear'
alias vi='vim'
alias ll='ls -l'

# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"

export PS1="\$[\[\e[32m\]\h\[\e[m\]]:[\[\e[31m\]\u\[\e[m\]]:[\W]:  "
