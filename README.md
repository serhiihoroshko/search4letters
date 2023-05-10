1. Create and activate virtual environments [venv](https://docs.python.org/3/library/venv.html)
2. Install Flask `pip istall flask`
3. Install MariaDB [MariaDB Server](https://mariadb.org/download/)
4. Install MariaDB Connector [Python Connect](https://mariadb.com/docs/skysql-previous-release/connect/programming-languages/python/install/)
5. Connect to the MariaDB and create database vsearchlogDB: `CREATE DATABASE vsearchlogDB;`
6. Create the new database user: `grant all on vsearchlogDB.* to 'vsearch'@'localhost' identified by '{{password}}';` and quit from MariaDB
7. `mysql -u vsearch -p vsearchlogDB`
8. Create table:
```sql
CREATE TABLE log (
id int auto_increment primary key,
ts timestamp default current_timestamp NOT NULL,
phrase varchar(128) NOT NULL,
letters varchar(32) NOT NULL,
ip varchar(16) NOT NULL,
browser_string varchar(256) NOT NULL,
results varchar(64) NOT NULL);
```
9. Check created table: `describe log;`