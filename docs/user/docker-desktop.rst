.. _docker-desktop:

Introduction
============

To quickly and conveniently provide for a way to give a demo, the GEOLib and some of the applications are provided as Docker containers. 
The GEOLibs are platform independent (python) libraries that provide an object-oriented interface to (for example) stix and flox files. That means that you can
create a Linux Docker image for this interface.

The last phase in a python implementation of a model however is an execute() subroutine, which calls for the Console version of the model initiator (for example:
DStabilityConsole.exe or DGeoFlowConsole.exe). As you can see, here lies a challenge, because Delphi interfaces cannot run as a default under Linux (let alone
a Linux Container).

Docker on Windows is an upcoming feature since Windows 10 and Windows Server 2016. This guide installs Docker-Desktop for Windows 10 and set things up so that 
it becomes possible to run Windows-native containers.

Prerequisites on Docker Desktop
===============================

For more information and docker-desktop itself, see https://www.docker.com/products/docker-desktop/.

Switching on necessary Windows capabilities
-------------------------------------------

Docker for Desktop is a quite complicated object (although the end result seems very obvious). Under the hood, a lot of virtual machinery
is going on. As a first, your laptops BIOS has to be configured so that the laptop is allowed to spawn virtual machines. Luckily, Deltares
laptops come with this preset already installed in the BIOS. 

As a second, we have to switch on some windows capabilities. Although we can do this in the gui, the simplest is to do this via an elevated
Powershell prompt (so, running as Administrator). There, issue the following commands::

PS C:\> Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform

(Answer N on the question whether to reboot)::

PS C:> Enable-WindowsOptionalFeature -Online -FeatureName $("Microsoft-Hyper-V", "Containers") -All

(Answer Y on the question whether to reboot. This will reboot and you see that a couple of things get installed).

wsl 1
-----

Although it is not really necessary for GEOLibs, you want to include a Linux here, because Docker-Desktop expects it. We install an Ubuntu 
in "Windows Subsystem for Linux 1" Here. From within the GUI, open en elevated Powershell. Then::

PS C:\> wsl --list --online
The following is a list of valid distributions that can be installed.
The default distribution is denoted by '*'.
Install using 'wsl --install -d <Distro>'.

  NAME               FRIENDLY NAME
* Ubuntu             Ubuntu
  Debian             Debian GNU/Linux
  kali-linux         Kali Linux Rolling
  SLES-12            SUSE Linux Enterprise Server v12
  SLES-15            SUSE Linux Enterprise Server v15
  Ubuntu-18.04       Ubuntu 18.04 LTS
  Ubuntu-20.04       Ubuntu 20.04 LTS
  OracleLinux_8_5    Oracle Linux 8.5
  OracleLinux_7_9    Oracle Linux 7.9
  
PS C:\Users\Willem> wsl --install -d Ubuntu
Installing: Windows Subsystem for Linux
Windows Subsystem for Linux has been installed.
Installing: Ubuntu
Ubuntu has been installed.
The requested operation is successful. Changes will not be effective until the system is rebooted.

After rebooting, the installation of Ubuntu in the Linux Subsystem for Windows will commence, and you see:

Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username: willem
New password:
Retype new password:
passwd: password updated successfully
Installation successful!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.79.1-microsoft-standard-WSL2 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This message is shown once a day. To disable it please create the
/home/willem/.hushlogin file.

This is a ubuntu running inside Windows 10. Just like a normal Ubuntu::

willem@VMWARE-DESKTOP:~$ sudo su -
[sudo] password for willem:
Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.79.1-microsoft-standard-WSL2 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This message is shown once a day. To disable it please create the
/root/.hushlogin file.
root@VMWARE-DESKTOP:~# apt-get update && apt-get -y upgrade
...






wsl 1 and wsl 2
---------------

Although we only need 

3.2.1.	wsl 1

From within the GUI, open en elevated Powershell (if you do this via the ssh-connection, it will fail). Then:

PS C:\Users\Willem> wsl --list --online
The following is a list of valid distributions that can be installed.
The default distribution is denoted by '*'.
Install using 'wsl --install -d <Distro>'.

  NAME               FRIENDLY NAME
* Ubuntu             Ubuntu
  Debian             Debian GNU/Linux
  kali-linux         Kali Linux Rolling
  SLES-12            SUSE Linux Enterprise Server v12
  SLES-15            SUSE Linux Enterprise Server v15
  Ubuntu-18.04       Ubuntu 18.04 LTS
  Ubuntu-20.04       Ubuntu 20.04 LTS
  OracleLinux_8_5    Oracle Linux 8.5
  OracleLinux_7_9    Oracle Linux 7.9
  
PS C:\Users\Willem> wsl --install -d Ubuntu
Installing: Windows Subsystem for Linux
Windows Subsystem for Linux has been installed.
Installing: Ubuntu
Ubuntu has been installed.
The requested operation is successful. Changes will not be effective until the system is rebooted.

After rebooting, the installation of Ubuntu in the Linux Subsystem for Windows will commence, and you see:

Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers
Enter new UNIX username: willem
New password:
Retype new password:
passwd: password updated successfully
Installation successful!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.79.1-microsoft-standard-WSL2 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This message is shown once a day. To disable it please create the
/home/willem/.hushlogin file.

This is a ubuntu running inside Windows 10. Just like a normal Ubuntu:

willem@VMWARE-DESKTOP:~$ sudo su -
[sudo] password for willem:
Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.79.1-microsoft-standard-WSL2 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This message is shown once a day. To disable it please create the
/root/.hushlogin file.
root@VMWARE-DESKTOP:~# apt-get update && apt-get -y upgrade
...


3.2.2.	wsl 2

The Docker Desktop is only running under wsl 2, but:

PS C:\Users\Willem> wsl --version
WSL version: 1.0.3.0
Kernel version: 5.15.79.1
WSLg version: 1.0.47
MSRDC version: 1.2.3575
Direct3D version: 1.606.4
DXCore version: 10.0.25131.1002-220531-1700.rs-onecore-base2-hyp
Windows version: 10.0.19045.2486

We have still to upgrade wsl 1 to wsl 2 (see https://learn.microsoft.com/en-us/windows/wsl/install).

PS C:\Users\Willem> Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
PS C:\Users\Willem> Restart-Computer -Force

Next download and install: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

PS C:\Users\Willem> wsl --update
Checking for updates.
The most recent version of Windows Subsystem for Linux is already installed.
PS C:\Users\Willem> wsl --set-default-version 2

PS C:\Users\Willem> wsl -l -v
  NAME      STATE           VERSION
* Ubuntu    Stopped         2

Lastly, try to start this Ubuntu by opening a shell.


3.3.	Installing Docker Desktop on Windows 10

3.3.1.	Docker Desktop

This is a GUI Application, so go to the Windows 10 GUI and download and install https://www.docker.com/products/docker-desktop/.
After login out and login in and starting docker desktop. You can do things like:

PS C:\Users\Willem> docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
PS C:\Users\Willem> docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
PS C:\Users\Willem> docker search nginx
NAME                                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
nginx                                             Official build of Nginx.                        17941     [OK]
linuxserver/nginx                                 An Nginx container, brought to you by LinuxS…   182
bitnami/nginx                                     Bitnami nginx Docker Image                      150                  [OK]
PS C:\Users\Willem>

You cannot start windows containers. To achieve this, right-click the Docker icon in the task bar and choose "Switch to Windows Containers"

Of course the same thing can be done via SSH:

PS C:\Users\Willem> ssh Willem@192.168.74.20
Willem@192.168.74.20's password:
Microsoft Windows [Version 10.0.19045.2486]
(c) Microsoft Corporation. All rights reserved.

willem@VMWARE-DESKTOP C:\Users\Willem>powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

PS C:\Users\Willem> docker ps
docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
PS C:\Users\Willem>

3.3.2.	open \\.\pipe\docker_engine_windows

When installing wsl-1, wsl-2 and Docker Desktop there is an issue in switching to Windows Containers. After switching, you get the error
message:

open \\.\pipe\docker_engine_windows: The system cannot find the file specified

You can resolve this by installing a few things more:

PS C:> Enable-WindowsOptionalFeature -Online -FeatureName $("Microsoft-Hyper-V", "Containers") -All
