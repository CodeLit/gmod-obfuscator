# Gmod obfuscator

It can obfuscate entire folders, excluding single files, and folders.
Can collect multiple files in folder to one single file.
Detects shared, server, client files by extention.
It should work fine with pure lua.

## Usage

- install git to your OS

- cd to folder with your addons

- run next commands in console:

  - `git clone git@github.com:CodeLit/gmod-obfuscator.git`

  - `cd gmod-obfuscator`

  - `git submodule update --init --recursive`

- install python to your OS

- cd to your addon folder, which needs to be obfuscated

- make file obfuscate.bat, or obfuscate.sh, if you using linux. Add next content to file:

`py ../gmod-obfuscator/run.py %~dp0`

- run file

## Config

You can also make changes to obfuscator config, just edit the settings.py file.
