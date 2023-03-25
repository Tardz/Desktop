#!/bin/bash

alacritty -e cd $HOME/jonalm/docs/Labbar git add --all git commit -m "upload" git push -u -f origin master
