#!/bin/bash

set -eux

apt clean
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*
rm -rf /var/tmp/*

find /var/log -type f -exec truncate -s 0 {} \;

rm -f /root/.bash_history
rm -f /home/agent/.bash_history

cloud-init clean --logs

truncate -s 0 /etc/machine-id
rm -f /var/lib/dbus/machine-id
ln -sf /etc/machine-id /var/lib/dbus/machine-id