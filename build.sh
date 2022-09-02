#!/bin/bash

# Set variables
PYTHONVER="$1"
 
# ---

# exit when any command fails
set -e

# Functions
ok() { echo -e '\e[32m'${1}'\e[m'; } # Green
die() { echo -e '\e[1;31m'${1}'\e[m'; exit 1; } # Red

# Sanity check
grep "Debian" /etc/*releas* &> /dev/null || die "This script should run only on Debian"
[ $(id -g) != "0" ] && die "Script must be run as root."
[ $# != "1" ] && die "Usage: $(basename $0) 3.10.2\nWhere, 3.10.2 - version"

# ---  

# Navigate to TEMP dir
cd /tmp

# Update
sudo apt-get update -y

# Install dependencies
sudo apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev wget tar

# Download latest Python source code
wget https://www.python.org/ftp/python/$PYTHONVER/Python-$PYTHONVER.tgz

# Extract the gzipped archive
tar -xf Python-$PYTHONVER.tgz

# Navigate to the Python source directory and execute the configure script:
cd Python-$PYTHONVER
./configure --enable-optimizations --prefix=$(echo ~/.python$PYTHONVER)

# Start build process:
make -j $(grep ^cpu\\scores /proc/cpuinfo | uniq |  awk '{print $4}')

# Install the Python binaries:
sudo make altinstall

# Add the Python to PATH variable
grep ".python$PYTHONVER" ~/.bashrc &> /dev/null || echo "export PATH=\$PATH:$(echo ~/.python$PYTHONVER/bin)" >> ~/.bashrc
source ~/.bashrc
ln -s ~/.python$PYTHONVER/bin/python3.10 python
ln -s ~/.python$PYTHONVER/bin/python3.10 python3