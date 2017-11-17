## PgSQLBDRChecker ##

Script to make a proxy (ie HAProxy) capable of monitoring PostgreSQL BDR Cluster nodes properly.

## Requirements ##
* xinetd
* python 2.7+
* python-pip
* psycopg2 (install with pip)
* ConfigParser (install with pip)

## Usage ##
Below is a sample configuration for HAProxy on the client. The point of this is that the application will be able to connect to localhost port 5432, so although we are using BDR Cluster with several nodes, the application will see this as a single BDR server running on localhost.

`/etc/haproxy/haproxy.cfg`

    ...
    listen BDR-cluster 0.0.0.0:5432
      balance leastconn
      option httpchk
      mode tcp
        server node1 1.2.3.4:5432 check port 9200 inter 5000 fastinter 2000 rise 2 fall 2
        server node2 1.2.3.5:5432 check port 9200 inter 5000 fastinter 2000 rise 2 fall 2
        server node3 1.2.3.6:5432 check port 9200 inter 5000 fastinter 2000 rise 2 fall 2 backup

Below is a sample config for checker script, this user will be used to check the status of DBR.

`/usr/bin/pgsqlcheck/database.ini`

    [postgresql]
    host=localhost
    database=suppliers
    user=postgres
    password=postgres

PostgreSQL connectivity is checked via HTTP on port 9200. The clustercheck script is a simple shell script which accepts HTTP requests and checks PostgreSQL on an incoming request. If the BDR Cluster node is ready to accept requests, it will respond with HTTP code 200 (OK), otherwise a HTTP error 503 (Service Unavailable) is returned.

## Setup with xinetd ##
This setup will create a process that listens on TCP port 9200 using xinetd. This process uses the clustercheck script from this repository to report the status of the node.

First, create a database user that will be doing the checks. User must have superuser privilege.

    pgsql>CREATE USER name WITH SUPERUSER;

Copy the files from the repository to a location (`/usr/bin` in the example below) and make it executable. Then add the following service to xinetd (make sure to match your location of the script with the 'server'-entry).

`/etc/xinetd.d/pgsqlchk`:

    # default: on
    # description: pgsqlchk
    service pgsqlchk
    {
            disable = no
            flags = REUSE
            socket_type = stream
            port = 9200
            wait = no
            user = nobody
            server = /usr/bin/pgsqlcheck/check.py
            log_on_failure += USERID
            only_from = 0.0.0.0/0
            per_source = UNLIMITED
    }

Also, you should add the pgsqlchk service to `/etc/services` before restarting xinetd.

    xinetd      9098/tcp    # ...
    pgsqlchk    9200/tcp    # PostgreSQL check  <--- Add this line
    git         9418/tcp    # Git Version Control System
    zope        9673/tcp    # ...

Clustercheck will now listen on port 9200 after xinetd restart, and HAproxy is ready to check PostgreSQL via HTTP poort 9200.
