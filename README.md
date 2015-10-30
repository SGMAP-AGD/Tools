# AGD Tools

Useful functions for datascience.

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

## Examples

### Data management

agd_tools offers [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) functions for [PostgreSQL](http://www.postgresql.org/) and CSV over SSH data sources.

#### PostgreSQL 

Import tables from PostgreSQL tables:

```python
from agd_tools import pg

iris = pg.import_table("iris", schema="flowers"):
```

#### CSV over SSH

Import CSV from SSH hosts:

```python
from agd_tools import ssh

iris = ssh.import_csv("/var/data", "iris.csv")

```

### Anonymization

Get the level of [k-anonymity](https://en.wikipedia.org/wiki/K-anonymity) of a dataframe using the `get_k`function:

```python
from agd_tools import anonymization

iris_anonymized = iris[['Name']]
k = anonymization.get_k(iris_anonymized)
```

### Licence

Cette librairie est libre sous licence [GNU Affero General Public License](http://www.gnu.org/licenses/agpl.html) version 3 ou ultérieure.
