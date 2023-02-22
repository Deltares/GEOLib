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

