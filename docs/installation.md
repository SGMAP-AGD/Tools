## Installation

Install agd_tools using pip:

```bash
pip install agd_tools
```

Or clone the repo, go into it and run 

```bash
pip install -e .
```

### Config file

agd_tools uses a config file to store your env variables. Be sure to have a valid `config.ini` file in your path. Here is a `config.ini` file example:

```ini
[PostgreSQL]
host = localhost
user = username
dbname = mydb
port = 5432

[SSH]
host = distanthost.com
username = username
```