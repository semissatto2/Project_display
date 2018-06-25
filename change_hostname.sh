#!/bin/bash
if [[ "$#" -ne 1 ]]; then
    echo "$0 usage: newhostname (run as root)"
    exit 1
fi
name=$(hostname)
hostname $1
sed -i "s/$name/$1/g" /etc/hostname
sed -i "s/$name/$1/g" /etc/hosts
