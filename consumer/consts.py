import os

CASSANDRA_HOSTS = os.getenv("CASSANDRA_HOSTS", "localhost").split(",")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", 9042))
TABLE_NAME = os.getenv("TABLE_NAME")
CREATE_KEYSPACE="""
    CREATE KEYSPACE IF NOT EXISTS my_keyspace 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
"""

CREATE_TABLE=f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id UUID PRIMARY KEY,
        message TEXT
    );
"""

INSERT_KEYSPACE=f"""
    INSERT INTO my_keyspace.{TABLE_NAME} (id, message)
    VALUES (uuid(), ?);
"""