#Build latest python from source for Debian

### Install dependencies:

```
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev
```

### Download latest python source version:

> check https://www.python.org/downloads/source/

```
wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
```

### Extract the gzipped archive:

```
tar -xf Python-3.9.1.tgz
```

### Navigate to the Python source directory and execute the configure script:
> --prefix - install all components to one folder, otherwise it will install through multiple OS folders.

```
cd Python-3.9.1
./configure --enable-optimizations --prefix=~/.python3.9
```

### Start build process:
> -j - how much CPU cores to use

```
make -j 2
```

### When build process is complete, install the Python binaries by:

```
sudo make altinstall
```

