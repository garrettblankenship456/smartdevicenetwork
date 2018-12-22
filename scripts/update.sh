#!/bin/bash

# This script automatically pulls from github and recompiles it all

git pull --rebase
sh compileall.sh
