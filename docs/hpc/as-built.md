# As-Built Documentation


!!! abstract "As-built Checklist"

    This checklist is curated from a variety of sources, experience and best
    practices through the years. When approriate, a reference has been called out
    for the process or the step. This is not a "end all" checklist for every
    scenario and is designed to get a consistent build process identified and
    executed against for seemless client experience. As always ***your mileage may
    vary***.


## Planning and Preparation

- [✓] Define the purpose and requirements of the cluster.

    > Teaching HPC concepts to higher-education students

- [✓] Determine the number and specifications of nodes (compute, login, storage, etc.).

    | Node | Role | Operating system |
    |------|------|------------------|
    | `nexusgateway0` | Gateway | `Ubuntu 20.04 LTS` |
    | `nexuscontrol0` | Control Plane | `Ubuntu 20.04 LTS` |
    | `nexuscontrol1` | Control Plane | `Ubuntu 20.04 LTS` |
    | `nexuscontrol2` | Control Plane | `Ubuntu 20.04 LTS` |
    | `nexusworker0` | Worker (GPU) | `Ubuntu 20.04 LTS` |
    | `nexusworker1` | Worker (GPU) | `Ubuntu 20.04 LTS` |
    | `nexusworker2` | Worker (GPU) | `Ubuntu 20.04 LTS` |
    | `nexusworker3` | Worker (GPU) | `Ubuntu 20.04 LTS` |

- [✓] Select the operating system for the cluster nodes (e.g., CentOS, Ubuntu).
    - `Debian GNU/Linux 11 (bullseye)`
    - `Ubuntu 22.04.3 LTS`

- [✓] Prepare a network infrastructure plan, including IP addressing and hostname scheme.

    | Node | BMC | Public | Private |
    |------|-----|--------|---------|
    | `nexusgateway0` | `10.16.192.101` | `10.16.194.101` | `172.16.0.101` |
    | `nexuscontrol0` | `10.16.192.102` | `10.16.194.102` | `172.16.0.102` |
    | `nexuscontrol1` | `10.16.192.103` | `10.16.194.103` | `172.16.0.103` |
    | `nexuscontrol2` | `10.16.192.104` | `10.16.194.104` | `172.16.0.104` |
    | `nexusworker0` | `10.16.192.51` | `10.16.194.51` | `172.16.0.51` |
    | `nexusworker1` | `10.16.192.52` | `10.16.194.52` | `172.16.0.52` |
    | `nexusworker2` | `10.16.192.53` | `10.16.194.53` | `172.16.0.53` |
    | `nexusworker3` | `10.16.192.54` | `10.16.194.54` | `172.16.0.54` |

- [✓] Configure and setup [`/etc/hosts` file](etc-hosts.md)

```
    127.0.0.1 localhost
    10.16.194.101 172.16.0.101 nexusgateway0 nx-gw
    10.16.194.102 172.16.0.102 nexuscontrol0 nx-m0
    10.16.194.103 172.16.0.103 nexuscontrol1 nx-m1
    10.16.194.104 172.16.0.104 nexuscontrol2 nx-m2
    10.16.194.51 172.16.0.51 nexusworker0 nx-w0
    10.16.194.52 172.16.0.52 nexusworker1 nx-w1
    10.16.194.53 172.16.0.53 nexusworker2 nx-w2
    10.16.194.54 172.16.0.54 nexusworker3 nx-w3
```


## Hardware and Networking

- [✓] Set up the physical hardware, ensuring proper cabling and power connections.
- [✓] Configure BIOS/UEFI settings for each node (e.g., boot order, hardware virtualization).
- [✓] Assign static IP addresses to all nodes [reference
  `netplan`](https://vitux.com/how-to-configure-networking-with-netplan-on-ubuntu/)
- [✓] Configure DNS and ensure forward and reverse DNS resolution for all nodes.


## Operating System Installation

- [✓] Install the chosen operating system on each node.
- [✓] Configure network settings, including hostname and IP address.

### Gateway node

- [✓] Setup service account as...

    - [✓] _Trace3 Service Account_: `t3-service`
```
    sudo useradd -c "Trace3 Service account" -m -s /bin/bash t3-service
    sudo passwd t3-service
```

    - [✓] add to sudo `sudo visudo`

```
    usermod -aG sudo t3-service
    t3-service ALL=(ALL) NOPASSWD:ALL
```

    - [✓] T3 ssh-key

    ```
    ssh-copy-id -i ~/.ssh/t3di-id_rsa.pub t3-service@10.16.194.101
    ```

    - Modify `~/.ssh/config`:

    ```
    Host *
    User t3-service
    Port 22
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes
    ```

- [✓] Install `tmux` [reference](https://phoenixnap.com/kb/tmux-tutorial-install-commands)

```
    sudo apt-get install tmux
    tmux new -s das
```

- [✓] Clustershell and configure `/etc/clustershell/groups`

```
    all: nx-m[0-2],nx-w[0-3]

    k8: nx-m[0-2],nx-w[0-3]
    mn: nx-m[0-2]
    dn: nx-w[0-3]
    wn: nx-w[0-3]
```

### All nodes

- [✓] Setup service account as...

    - [✓] _Trace3 Service Account_: `t3-service`
```
    sudo useradd -c "Trace3 Service account" -m -s /bin/bash t3-service
    sudo passwd t3-service
```

    - [✓] add to sudo `sudo visudo`
    - [✓] t3-service ALL=(ALL) NOPASSWD:ALL

```
    sudo usermod -aG sudo t3-service
```

- [✓] Set up SSH keys for passwordless access between nodes.

```
    ssh-copy-id -i ~/.ssh/id_rsa.pub t3-service@_target_
```

- [✓] Remove NetworkManager from all nodes

```
    sudo systemctl stop NetworkManager.service
    sudo systemctl disable NetworkManager.service

    sudo systemctl stop NetworkManager-wait-online.service
    sudo systemctl disable NetworkManager-wait-online.service

    sudo systemctl stop NetworkManager-dispatcher.service
    sudo systemctl disable NetworkManager-dispatcher.service

    sudo systemctl stop network-manager.service
    sudo systemctl disable network-manager.service
```

- [✓] Setup NTP for all nodes [see
  this](https://www.digitalocean.com/community/tutorials/how-to-set-up-time-synchronization-on-ubuntu-20-04)
as neeeded
- [✓] Remove firewalls from all nodes via:

```
    sudo ufw disable
    sudo apt-get remove ufw
    sudo apt-get purge ufw

    sudo iptables -F
    sudo iptables -X
    sudo iptables -t nat -F
    sudo iptables -t nat -X
    sudo iptables -t mangle -F
    sudo iptables -t mangle -X
    sudo iptables -P INPUT ACCEPT
    sudo iptables -P OUTPUT ACCEPT
```

!!! note
    The following is only required for Slurm implementations

- ~~[✓] Setup and sync UID/GID settings for service accounts~~
  [reference](https://www.thegeekdiary.com/how-to-correctly-change-the-uid-and-gid-of-a-user-group-in-linux/)


!!! warning
    The following four steps are required for Kubernetes/Calico implementations

- [✓] From [Kubernetes
  documentation](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
make these adjustments:

```
    cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    overlay
    br_netfilter
    EOF

    sudo modprobe overlay
    sudo modprobe br_netfilter

    # sysctl params required by setup, params persist across reboots
    cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-iptables  = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward                 = 1
    EOF

    # Apply sysctl params without reboot
    sudo sysctl --system
```

- [✓] Verify that the `br_netfilter`, `overlay` modules are loaded by running
the following commands:

```
    lsmod | grep br_netfilter
    lsmod | grep overlay
```

- [✓] Verify that the `net.bridge.bridge-nf-call-iptables`, `net.bridge.bridge-nf-call-ip6tables`, and `net.ipv4.ip_forward` system variables are set to `1` in your `sysctl` config by running the following command:

```
    sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward
```

- [ ] Additional `sysctl.conf` settings:




- [✓] Turn off swap by

    1. [✓] `swapoff -a`

    2. [✓] `sudo vi /etc/fstab` to remove any swap enties, (if pre-installed)

    3. ~~[] `sudo systemctl mask "dev-sdXX.swap"` replacing XX as appropriate~~


## Software Installation

- [✓] Run `sudo apt-get update && sudo apt-get upgrade -y` for all nodes
- [✓] Install necessary system packages (e.g., build tools, development libraries).
    - [✓] jc: `jc --version`
    - [✓] `python-is-python3`
    - [✓] GCC: `gcc --version`
    - [✓] kernel headers and packages: `uname -r`

- [✓] For **Worker Nodes**: setup and install Nvidia GPU drivers and [CUDA toolkit](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/contents.html)
- [✓] Set up a shared filesystem (e.g., NFS, Lustre) for sharing data between nodes.

