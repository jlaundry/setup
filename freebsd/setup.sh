#!/bin/sh

pkg update
pkg install sudo

visudo # uncomment %wheel

pkg install \
 bash \
 curl \
 git \
 jq \
 python311 \
 screen \
 smartmontools \
 vim-tiny \
 zfs-periodic
