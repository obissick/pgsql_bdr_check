#!/usr/bin/python
import psycopg2
from config import config
from socket import gethostname
import subprocess
import os

def connect():
    #""" Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        #get node status
        query = ("SELECT bdr.bdr_nodes.node_status FROM bdr.bdr_nodes WHERE node_name = '{0}'").format(gethostname())
        cur.execute(query)

        # display the PostgreSQL database server version
        node_state = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()

        if node_state[0] == 'r':
            subprocess.call([os.path.dirname(__file__)+'/status_out.sh %s' % 'r'], shell=True)

        else:
            subprocess.call([os.path.dirname(__file__)+'/status_out.sh %s' % 'd'], shell=True)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()
