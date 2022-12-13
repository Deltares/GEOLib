1.0.  Linux Container
=====================

We can build a Docker image of GEOLib by mimicing the installation a a "real" Linux server. This can be done, but lead
to an image with much development overhead in it. That's why most of the Linux GEOLib imgages are build in a generic container, 
after which the libraries are copied to an image which has a smaller overhead.j

We use the following dockerfile:

  willem@L02712:GEOLib$ cat Dockerfiles/prod/Dockerfile-ubuntu

  ### Build

  FROM ubuntu:22.10 AS build
  LABEL maintainer="Willem Noorduin <willem.noorduin@deltares.nl>"

  RUN apt-get -y update && apt-get -y install python3
  RUN apt-get -y install python3-pip

  # Make a user geolib

  RUN useradd -c "GEOLib user" -m -s /usr/bin/bash geolib
  USER geolib

  RUN mkdir -p /home/geolib/.local/bin
  RUN export PATH="${PATH}:/home/geolib/.local/bin"

  # Install Requirements for GEOLib

  ADD requirements.txt /home/geolib
  RUN pip install -r /home/geolib/requirements.txt

  # Install GEOLib

  RUN pip install d-geolib
  USER root

  ### Deploy

  FROM ubuntu:22.10

  RUN useradd -c "Geolib User" -m -d /home/geolib geolib

  ENV PYTHONUNBUFFERED=1
  RUN apt-get -y update && apt-get -y install python3

  USER geolib
  COPY --from=build /home/geolib/.local /home/geolib/.local

After building this:

  11:14 $ docker images
  REPOSITORY          TAG       IMAGE ID       CREATED             SIZE
  geolib-ubuntu       latest    b6b87fbd62e6   About an hour ago   198MB
  <none>              <none>    ea42bbb988cc   About an hour ago   572MB
  geolib-dev-alpine   1.0.0     fe5d43c282a8   3 days ago          111MB
  geolib-prod         latest    fe5d43c282a8   3 days ago          111MB
  ubuntu              22.10     d6547859cd2f   3 days ago          70.2MB
  alpine              latest    49176f190c7e   2 weeks ago         7.05MB

  ✔ ~/development/github.com/GEOLib [geolib-docker|✔]
  11:51 $ docker run -it geolib-ubuntu:latest bash
  geolib@39bda36dfbd9:/$ python3
  Python 3.10.7 (main, Nov 24 2022, 19:45:47) [GCC 12.2.0] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import geolib
  >>> dir(geolib)
  ['BaseDataClass', 'BaseModel', 'BaseModelList', 'BaseModelStructure', 'BaseValidator', 'Color', 'DFoundationsModel', 'DSettlementModel', 'DSheetPilingModel', 'DStabilityModel', 'MetaData', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__version__', 'base_model', 'base_model_structure', 'dfoundations', 'dseries_parser', 'dsettlement', 'dsheetpiling', 'dstability', 'errors', 'geometry', 'internal', 'meta', 'model_enums', 'models', 'parsers', 'serializers', 'soils', 'utils', 'validators']
  >>> quit()
  geolib@39bda36dfbd9:/$ exit
  exit

Remark: 

We can build an even smaller container by:

...
### Deploy

FROM alpine:latest

RUN adduser -h /home/geolib -D geolib

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

USER geolib

COPY --from=build /home/geolib/.local /home/geolib/.local

But alpine does not offer much except sh.

2.0.  Windows Container

willem@L02712:/mnt/c/home/willem/development/github/GEOLib$ cat Dockerfile-windows
### build stage

FROM mcr.microsoft.com/windows/servercore:ltsc2019 AS build

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
RUN New-Item C:/temp -ItemType Directory; \
  New-Item C:/data -ItemType Directory;
WORKDIR C:/temp

ENV PYTHON_VERSION 3.7.9
ENV PYTHON_RELEASE 3.7.9

RUN $url = ('https://www.python.org/ftp/python/{0}/python-{1}-amd64.exe' -f $env:PYTHON_RELEASE, $env:PYTHON_VERSION); \
        Write-Host ('Downloading {0} ...' -f $url); \
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
        Invoke-WebRequest -Uri $url -OutFile 'python.exe'; \
        \
        Write-Host 'Installing ...'; \
# https://docs.python.org/3.7/using/windows.html#installing-without-ui
        Start-Process python.exe -Wait \
                -ArgumentList @( \
                        '/quiet', \
                        'InstallAllUsers=1', \
                        'TargetDir=C:\Python37', \
                        'PrependPath=1', \
                        'Shortcuts=0', \
                        'Include_doc=0', \
                        'Include_pip=0', \
                        'Include_test=0' \
                ); \
        \
#the installer updated PATH, so we should refresh our local value
        $env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine); \
        \
        Write-Host 'Verifying install ...'; \
        Write-Host '  python --version'; python --version; \
        \
        Write-Host 'Removing ...'; \
        Remove-Item python.exe -Force; \
        \
        Write-Host 'Complete.'

# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/d59197a3c169cef378a22428a3fa99d33e080a5d/get-pip.py
ENV PYTHON_GET_PIP_SHA256 421ac1d44c0cf9730a088e337867d974b91bdce4ea2636099275071878cc189e

RUN Write-Host ('Downloading get-pip.py ({0}) ...' -f $env:PYTHON_GET_PIP_URL); \
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
        Invoke-WebRequest -Uri $env:PYTHON_GET_PIP_URL -OutFile 'get-pip.py'; \
        Write-Host ('Verifying sha256 ({0}) ...' -f $env:PYTHON_GET_PIP_SHA256); \
        if ((Get-FileHash 'get-pip.py' -Algorithm sha256).Hash -ne $env:PYTHON_GET_PIP_SHA256) { \
                Write-Host 'FAILED!'; \
                exit 1; \
        }; \
        \
        Write-Host ('Installing pip ...'); \
        python get-pip.py \
                --disable-pip-version-check \
                --no-cache-dir \
        ; \
        Remove-Item get-pip.py -Force; \
        \
        Write-Host 'Verifying pip install ...'; \
        pip --version; \
        \
        Write-Host 'Complete.'

# Install Requirements for GEOLib

COPY requirements.txt C:\\
RUN pip install -r  C:/requirements.txt

# Install GEOLib

RUN pip install d-geolib

#
# Deploy
#

FROM mcr.microsoft.com/windows/nanoserver:ltsc2019
USER Administrator
COPY --from=build C:\\Python37 C:\\Python37
SHELL ["cmd.exe", "/s", "/c"]
RUN setx /m PATH %PATH%;c:\Python37
USER ContainerUser

After building this, we have:

PS C:\home\willem\development\github\GEOLib> docker images
REPOSITORY                             TAG        IMAGE ID       CREATED             SIZE
geolib                                 latest     802316afd357   11 minutes ago      343MB
<none>                                 <none>     ab9105496bb9   16 minutes ago      342MB
<none>                                 <none>     d2f9ee7cb59d   17 minutes ago      342MB
<none>                                 <none>     9724bd60dc37   About an hour ago   5.84GB
<none>                                 <none>     6ec79f5666f3   About an hour ago   5.84GB
<none>                                 <none>     f1fc52c96d17   2 hours ago         5.81GB
<none>                                 <none>     ef7f980f72b5   2 hours ago         5.81GB
mcr.microsoft.com/windows/servercore   ltsc2019   4503e186c64d   5 weeks ago         5.68GB
mcr.microsoft.com/windows/nanoserver   ltsc2019   c89127473dbd   5 weeks ago         258MB
PS C:\home\willem\development\github\GEOLib> docker run -it geolib:latest cmd
Microsoft Windows [Version 10.0.17763.3650]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>python3
'python3' is not recognized as an internal or external command,
operable program or batch file.

C:\>python
Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import geolib
>>> dir(geolib)
['BaseDataClass', 'BaseModel', 'BaseModelList', 'BaseModelStructure', 'BaseValidator', 'Color', 'DFoundationsModel', 'DSettlementModel', 'DSheetPilingModel', 'DStabilityModel', 'MetaData', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__
package__', '__path__', '__spec__', '__version__', 'base_model', 'base_model_structure', 'dfoundations', 'dseries_parser', 'dsettlement', 'dsheetpiling', 'dstability', 'errors', 'geometry', 'internal', 'meta', 'model_enums', 'models', 'parsers', 'serializers', 'soils', '
utils', 'validators']
>>> quit()

C:\>exit



