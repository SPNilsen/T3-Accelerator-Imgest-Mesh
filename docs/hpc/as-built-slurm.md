# Installation Checklists and Build Documents


!!! abstract "As-built Checklist"

    This checklist is curated from a variety of sources, experience and best
    practices through the years. When approriate, a reference has been called out
    for the process or the step. This is not a "end all" checklist for every
    scenario and is designed to get a consistent build process identified and
    executed against for seemless client experience. As always ***your mileage may
    vary***.



## Planning and Preparation


- [✓] Client:

    > Milwaukee School of Engineering (MSOE)

- [✓] Define the purpose and requirements of the cluster.

    > Add x2 Nvidia DGX-H100 nodes into existing SLURM cluster

    > Cluster name: **`Rosie`**

- [✓] Determine the number and specifications of nodes (compute, login, storage, etc.).

    | Node | Role | Operating system |
    |------|------|------------------|
    | `dh-dgxh100-1` | Worker (GPU) | DGX OS 6 / `Ubuntu 20.04 LTS` |
    | `dh-dgxh100-2` | Worker (GPU) | DGX OS 6 / `Ubuntu 20.04 LTS` |

- [✓] Select the operating system for the cluster nodes (e.g., RHEL, Ubuntu)

    ??? tip inline end "OS level"
        Determine existing OS with **`lsb_release -a`**


    > `Ubuntu 20.04.6 LTS`


- [✓] Prepare a network infrastructure plan, including IP addressing and hostname scheme.

    | Node | BMC | Public | Private |
    |------|-----|--------|---------|
    | hpclebgen1  | n/a | 130.189.166.21 | n/a |
    | hpclebml1   | n/a | 130.189.166.22 | n/a |
    | hpclebstor1 | n/a | 130.189.166.23 | n/a |
    | hpclebdb1   | n/a | 130.189.166.24 | n/a |
    | hpclebapi1  | n/a | 130.189.166.25 | n/a |

- [✓] Configure and setup `/etc/hosts` file

    ??? tip inline end
        Reference the [Configurations page](../config/configs.md) for further details.


## Hardware and Networking

- [✓] Set up the physical hardware, ensuring proper cabling and power connections
- [✓] Configure BIOS/UEFI settings for each node (e.g., boot order, hardware virtualization)
- [✓] Assign static IP addresses to all nodes

    ??? tip inline end "Netplan assistance"

        - [Reference `netplan`](https://vitux.com/how-to-configure-networking-with-netplan-on-ubuntu/) for details on configuring static addresses

        - [HOWTO config `netplan`](https://getlabsdone.com/how-to-configure-bonding-using-netplan/) for LACP uplinks

        - Reference the [Configurations page](../config/configs.md) for further details.


- [✓] Configure DNS and ensure forward and reverse DNS resolution for all nodes


## Operating System Installation

- [✓] Install the chosen operating system on each node
- [✓] Configure network settings, including hostname and IP address

### Gateway node

!!! warning "Service account customization"
    Some clients will not want this, should be verified during project kickoff
    for clarification.


??? example "Reset password via rescue or single-user mode"
    - Boot into Grub

    - '`e`' for Editing the boot menu

    - Find the line starting with `linux...`

    - Replace `ro` with `rw init=/bin/bash`

    - `Ctrl-x` to reboot

    - Boots to root prompt (`#`)

    - `passwd <user_acct>`

    - `exit` to reboot

    [greater deets](https://www.numerickly.com/2021/08/20/accessing-single-user-mode-in-ubuntu-to-reset-a-lost-password/)



- [✓] Setup _Trace3 Service Account_: `t3-service`

```
    sudo useradd -c "Trace3 Service account" -m -s /bin/bash t3-service
    sudo passwd t3-service  #Tr@ce321!
```

- [✓] add `t3-service` to sshd via `/etc/ssh/sshd_config`

    - [add user to sshd](https://linuxconfig.org/how-to-enable-and-disable-ssh-for-user-on-linux)



- [✓] add to sudo `sudo visudo`

```
    usermod -aG sudo t3-service
    t3-service ALL=(ALL) NOPASSWD:ALL
```

- [✓] T3 ssh-key

    ```
    ssh-copy-id -i ~/.ssh/t3di-id_rsa.pub t3-service@10.16.194.101
    ```

    - [✓] Modify `~/.ssh/config`:

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

- [✓] Install `clustershell` [reference](https://clustershell.readthedocs.io/en/latest/)

    ```
    sudo apt-get install clustershell
    ```

- [✓] Configure `/etc/clustershell/groups`


    ??? tip inline end
        Reference the [Configurations page](../config/configs.md) for further details.


### All nodes

- [✓] Setup _Trace3 Service Account_: `t3-service`

!!! info inline end "Service account customization"
    Clients need to understand this is important for intercluster
    communications and should be emphasized during project kickoff
    for clarification.

```
    sudo useradd -c "Trace3 Service account" -m -s /bin/bash t3-service
    sudo passwd t3-service
```

- [✓] add to sudo `sudo visudo`

```
    t3-service ALL=(ALL) NOPASSWD:ALL
```

- [✓] Execute

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

- [✓] Set up a shared filesystem (e.g., NFS, Lustre, Weka.io) for sharing data between nodes.

    - [✓] For NFS, setup `/etc/fstab`

        ??? tip inline end
            Reference the [Configurations page](../config/configs.md) for further details.

    - [✓] Then test `mount`

??? abstract "SLURM Implementation"
    The following is only required for Slurm implementations

    - [✓] Setup and sync UID/GID settings for service accounts
      [reference](https://www.thegeekdiary.com/how-to-correctly-change-the-uid-and-gid-of-a-user-group-in-linux/)




??? abstract "Kubernetes Implementation"
    The following four steps are required for Kubernetes/Calico implementations

    - [✓] From [Kubernetes documentation](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
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


??? abstract "SLURM Configuration"
    The following is only required for Slurm implementations

    !!! info inline end
        Reference the [Configurations page](../config/configs.md) for further details.


    - [ ] Install Slurm and its dependencies (Munge, MySQL/MariaDB).
        - [ ] Install Munge.
        - [ ] Install MySQL/MariaDB.
    - [ ] Configure Slurm on the controller node
        - [ ] `/etc/slurm-llnl/slurm.conf`.
        - [ ] Push to compute nodes.
    - [ ] Set up Munge for authentication and encryption.
    - [ ] Configure MySQL/MariaDB for Slurm accounting data.
    - [ ] Edit Slurm configuration files: `slurm.conf`, `cgroup.conf`, `gres.conf`, etc.
    - [ ] Configure partitions, queues, and QoS (Quality of Service) settings.
    - [ ] Define job submission policies and limits (e.g., maximum job run time, node access policies).
    - [ ] Set up user authentication and access control.



## Testing

- [ ] Test the cluster's functionality by submitting various jobs to different partitions and queues.
- [ ] Monitor system performance and resource utilization during job execution.
- [ ] Verify that job scheduling, resource allocation, and accounting are working as expected.

## Security and Maintenance

- [ ] Implement security best practices, including firewalls, regular updates, and intrusion detection.
- [ ] Establish a regular backup and recovery strategy for critical cluster data.
- [ ] Set up monitoring and alerting for hardware, software, and resource usage.
- [ ] Define procedures for handling hardware failures, node replacements, and software issues.

## User Training

- [ ] Provide training for users on how to interact with and utilize the cluster effectively.
- [ ] Explain job submission, monitoring, and troubleshooting procedures.
- [ ] Offer guidance on optimizing job performance and resource utilization.

## Deployment

- [ ] Deploy the cluster for production use, ensuring all configurations are finalized.
- [ ] Monitor the cluster in its production environment, making adjustments as necessary.
- [ ] Continuously monitor and update the cluster's software and security configurations.



