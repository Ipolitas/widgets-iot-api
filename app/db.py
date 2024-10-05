import os
import time
from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, retries=5):
        uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "test1234")

        # Retry connection
        for i in range(retries):
            try:
                self._driver = GraphDatabase.driver(uri, auth=(user, password))
                # Try to open a session to verify the connection
                with self._driver.session() as session:
                    session.run("RETURN 1")
                print("Successfully connected to Neo4j")
                break
            except Exception as e:
                print(f"Attempt {i+1} - Could not connect to Neo4j: {e}")
                time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            raise Exception("Could not connect to Neo4j after several retries")

    def close(self):
        self._driver.close()

    def query(self, query, parameters=None):
        session = None
        response = None
        try:
            session = self._driver.session()
            response = session.run(query, parameters)
            return [record for record in response]
        finally:
            if session:
                session.close()
