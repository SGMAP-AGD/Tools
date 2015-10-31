## Data management

agd_tools offers [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) functions for [PostgreSQL](http://www.postgresql.org/) and CSV over SSH data sources.

### PostgreSQL 

Import tables from PostgreSQL tables:

```python
from agd_tools import pg

iris = pg.import_table("iris", schema="flowers"):
```

### CSV over SSH

Import CSV from SSH hosts:

```python
from agd_tools import ssh

iris = ssh.import_csv("/var/data", "iris.csv")

```