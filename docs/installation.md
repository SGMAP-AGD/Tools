## Installation

We strongly encourage you to install `agd_tools` inside a virtualenv. Assuming you are using `virtualenvwrapper`, load the virtualenv of the project your are developing :

```bash
workon myproject
```

If you just want to use `agd_tools` without modifying it, install `agd_tools` using :

```bash
pip install agd_tools
```

If you want to add features in `agd_tools` while developing your project, clone the repo and install a development version :

```bash
cd /home/user/project
git clone git@github.com:SGMAP-AGD/Tools.git
cd agd_tools
pip install -e .
```

### Config file

`agd_tools` uses a config file to access your database. This file should be named `config.ini`. 
If you installed a development version of `agd_tools`, 
this file should be located at `/home/you/projects/agd_tools/agd_tools/config.ini`.
 Otherwise the file should be located at 
'~/.virtualenvs/myproject/lib/python3.x/site-packages/agd_tools/config.ini'. 


See `config.ini.example` to see syntax & keys
