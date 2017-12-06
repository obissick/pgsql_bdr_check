#!/usr/bin/python
import psycopg2
from config import config
from socket import gethostname
import subprocess
import os, sys

def sleep(time):
    subprocess.call(["sleep "+time],shell=True)

def httpOut(message,length,out):
    sys.stdout.write(message)
    sys.stdout.write("Content-Type: text/plain\r\n")
    sys.stdout.write("Connection: close\r\n")
    sys.stdout.write("Content-Length: "+length+"\r\n")
    sys.stdout.write("\r\n")
    sys.stdout.write(out)
    sleep("0.1")
    exit(0)

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

        #save status to variable
        node_state = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()

        if node_state[0] == 'r':
            #if status = r then send OK status to HAProxy
            # Shell return-code is 0
            httpOut("HTTP/1.1 200 PostgreSQL BDR Node is ready.\r\n", "40" ,"Cluster Node is ready.\r\n")

        else:
            #else node in a not in a ready state.
            # Shell return-code is 1
            httpOut("HTTP/1.1 503 PostgreSQL BDR is not ready.\r\n", "44" ,"Cluster Node is not ready.\r\n")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()
