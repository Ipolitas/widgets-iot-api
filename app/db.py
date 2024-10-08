import time
from neo4j import GraphDatabase
from neontology import init_neontology


def verify_neo4j_connection(uri, user, pwd, retries=10) -> None:
    for i in range(retries):
        try:
            _driver = GraphDatabase.driver(uri, auth=(user, pwd))
            # Try to open a session to verify the connection
            with _driver.session() as session:
                session.run("RETURN 1")
            print("Successfully connected to Neo4j")
            _driver.close()
            return True
            break
        except Exception as e:
            print(f"Attempt {i+1} - Could not connect to Neo4j: {e}")
            time.sleep(1)  # Wait for 1 seconds before retrying
    else:
        raise Exception("Could not connect to Neo4j after several retries")


def establish_connection(uri, user, pwd) -> None:
    verify_neo4j_connection(uri, user, pwd)

    init_neontology(
        neo4j_uri=uri,
        neo4j_username=user,
        neo4j_password=pwd
    )
