# Setting up for local development

Currently, this is the only way to run parc.

## Preparing

First install the following apt packages:
```shell
$ sudo apt install python3 python3-pip python3-venv -y
```

## Cloning the repository

Now, clone the repository:
```shell
$ git clone https://github.com/sinmineryt/parc.git
$ cd parc
```

## Setting up the venv

Set up the venv using the following command:
```shell
$ virtualenv ./venv 
$ source ./venv/bin/activate 
$ pip install -r requirements.txt
```

## Running
You can now run parc using
```shell
$ ./parc.py
```

