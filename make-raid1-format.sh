#!/bin/bash

VOL1="/dev/sdh"
VOL2="/dev/sdi"
MOUNTPOINT="/backups"
VOLUME_SIZE="5GB"

parted $VOL1 mklabel gpt
parted $VOL1 mkpart primary 0GB $VOLUME_SIZE

parted $VOL2 mklabel gpt
parted $VOL2 mkpart primary 0GB $VOLUME_SIZE

partprobe $VOL1
partprobe $VOL2

mdadm  --create /dev/md0 --level=1 --raid-devices=2 $VOL1 $VOL2
mkfs.ext4 /dev/md0

mkdir -p /backups
mount /dev/md0 /backups