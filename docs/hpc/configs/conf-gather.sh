#!/bin/bash
#
#
# Overview

dirname=`hostname -a`

mkdir $dirname

hostname > ./$dirname/hostname
uname -r > ./$dirname/uname -r
cat /etc/lsb-release > ./$dirname/lsb-release
cat /etc/netplan/01-netcfg.yaml > ./$dirname/01-netcfg.yaml
ip addr > ./$dirname/ipaddr
cat /etc/clustershell/group > ./$dirname/clush-group
cat /etc/fstab > ./$dirname/fstab
mount > ./$dirname/mount
cat /etc/hosts > ./$dirname/hosts
cat /etc/modules-load.d/k8s.conf > ./$dirname/modules-k8s.conf
cat /etc/sysctl.d/k8s.conf > ./$dirname/sysctl.d-k8s.conf
cat /etc/slurm-llnl/cgroup.conf > ./$dirname/cgroup.conf
cat /etc/slurm-llnl/gres.conf > ./$dirname/gres.conf
cat /etc/slurm-llnl/slurm.conf > ./$dirname/slurm.conf

scp -r -P 22000 ./$dirname douglassayles@72.194.228.166:/tmp/.

rm -rf ./$dirname
