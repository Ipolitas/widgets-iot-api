from fastapi import FastAPI
from .db import Neo4jConnection

app = FastAPI()

# Initialize Neo4j connection
conn = Neo4jConnection()


@app.get("/")
def read_root():
    result = conn.query("MATCH (n) RETURN COUNT(n) as count")
    return {"node_count": result[0]["count"]}


# Close the connection on shutdown
@app.on_event("shutdown")
def shutdown():
    conn.close()
