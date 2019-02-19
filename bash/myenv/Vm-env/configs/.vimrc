set nocompatible              " be iMproved, required
filetype off                  " required

set history=100 " history size
set autoread " Set to auto read when a file is changed from the outside
set ruler " Always show current position

set cursorline " Higlight the current line
set hlsearch " Highlight search results
set number " Show line numbers
set showmatch " Show matching brackets when text indicator is over them

set laststatus=2 " Always show the status line
set backspace=2
set tabstop=2
set shiftwidth=2
set softtabstop=2
set smartindent " Indentation after {[( for the next line

set background=dark
set t_Co=256 " 256 colors in terminal
colorscheme hybrid

" Set cursorline background color
hi CursorLine cterm=NONE ctermbg=235 guibg=#262626
set t_Co=256 " 256 colors in terminal" Set overlenght limits highlight
hi ColorColumn cterm=NONE ctermbg=235 guibg=#262626


" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'

Plugin 'vim-airline/vim-airline' " Cool status line
Plugin 'vim-airline/vim-airline-themes' " Themes for it
Plugin 'tpope/vim-surround' " Change surroundings
Plugin 'ervandew/supertab' " As it says
Plugin 'tpope/vim-fugitive' " Git wrapper
Plugin 'tpope/vim-endwise' " Endings for functions
Plugin 'mhinz/vim-startify' " Startup screen
Plugin 'tomasr/molokai'

call vundle#end()            " required
filetype plugin indent on    " required

syntax enable
