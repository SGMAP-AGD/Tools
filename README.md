# AGD Tools

Useful functions for datascience.

## Installation

Install agd_tools using pip:

```
pip install agd_tools
```

## Usage

### Config file

agd_tools uses a config file to store your env variables. Be sure to have a valid `config.ini` file in your path. Here is a `config.ini` file example:

```
[PostgreSQL]
host = localhost
user = username
dbname = mydb
port = 5432

[SSH]
host = distanthost.com
username = username
```

### Data management

agd_tools offers CRUD functions for PostgreSQL and CSV over SSH data sources.

#### PostgreSQL 

```
from agd_tools import pg

iris = pg.import_table("iris", schema="flowers"):
```

#### SSH

```
from agd_tools import ssh

iris = ssh.import_csv("/var/data", "iris.csv")
```
