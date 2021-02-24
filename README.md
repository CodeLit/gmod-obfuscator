# Gmod obfuscator

It can easilly obfuscate the entire folders, excluding single files, and folders.
Can collect multiple files in folder to one single file.
Detects shared, server, client files by endings.
It should work fine with pure lua code too.

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

## Ignoring single files

Just add `-- [do not obfuscate]` comment in top of the file

## Collecting folders

Just create `__collectfolder__.lua` file in folder, that you need to collect.
It will collect files, ends with `_sv.lua` to single `__sv.lua` file,
and also `_cl.lua` to `__cl.lua`, and other files to `___sh.lua`.

## Ignoring folders

Edit the `settings.py` file, the `ignored_folders` array, type the names of folders that you need to ignore and do not obfuscate.

## Config

You can also make changes to obfuscator config, just edit the `settings.py` file.
