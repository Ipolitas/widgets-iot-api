import time
from neo4j import GraphDatabase
from neomodel import config


def verify_neo4j_connection(uri, user, pwd, retries=10) -> None:
    for i in range(retries):
        try:
            _driver = GraphDatabase.driver(f'bolt://{uri}', auth=(user, pwd))
            # Try to open a session to verify the connection
            with _driver.session() as session:
                session.run("RETURN 1")
            print("Successfully connected to Neo4j")
            _driver.close()
            return True
        except Exception as e:
            print(f"Attempt {i+1} - Could not connect to Neo4j: {e}")
            time.sleep(1)  # Wait for 1 seconds before retrying
    else:
        raise Exception("Could not connect to Neo4j after several retries")


def establish_connection(uri, user, pwd) -> None:
    verify_neo4j_connection(uri, user, pwd)
    config.DATABASE_URL = f'bolt://{user}:{pwd}@{uri}'  # default
