#!/usr/bin/env bash

DIR=`dirname $0`
# TODO collect stats on who uses what OS
cat $DIR/scripts/logo.txt 

good=true #until proven guilty
echo
if [ "$(uname)" == "Darwin" ]; then
    echo You are on OSX
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    echo You are on Linux
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo You are on Windows
fi

red() {
   echo $'\e[31m'$1$'\e[0m'
}

green() {
   echo $'\e[32m'$1$'\e[0m'
}

infocheck() {
    local thing="$1"
    which "$thing" >>/dev/null 
    if [ "$?" -ne 0 ]; then
        good=false
        echo You do not have $(green $thing) installed. 
        return 1
    fi
}

fatalcheck() {
    local thing="$1"
    which "$thing" >>/dev/null \
        || (echo You do not have $(red $thing) installed! $(red FAIL) 
            return 1)
}

if [ "$(uname)" == "Darwin" ]; then
    infocheck brew
    # TODO use brew to check the dev env is good
fi
fatalcheck python3 || exit $?
fatalcheck git || exit $?

# check if the repo is updated subsequent to the rename
git config --get remote.origin.url \
    | grep -q 'git@github.com:rIGS2016/Potatobot.git' \
    && cat <<EOM

Yo, code poet, you have the old remote repo. You need to run this: 

$(echo $'\e[34m')
  git config --set remote.origin.url git@github.com:rIGSteam/Potatobot.git
$(echo $'\e[0m')

EOM
# TODO maybe confirm and do this change for them?

if [ "$good" == true ]; then
    echo no problems found
fi
