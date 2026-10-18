import os
import time
from dotenv import load_dotenv
from falkordb import FalkorDB

load_dotenv()

hosts_to_try = [
    os.getenv("FALKORDB_HOST"),
    "node-f-0.instance-xojyn8she.hc-7up0crkyn.ap-south-1.aws.f2e0a955bb84.cloud"
]
port = int(os.getenv("FALKORDB_PORT", 63324))
username = os.getenv("FALKORDB_USERNAME", "admin")
password = os.getenv("FALKORDB_PASSWORD")
graph_id = os.getenv("FALKORDB_GRAPH_ID", "sentry_enterprise")

success = False
for host in hosts_to_try:
    if not host:
        continue
    print(f"\n--- Trying connection to {host}:{port} as user '{username}' ---")
    try:
        start = time.perf_counter()
        client = FalkorDB(host=host, port=port, username=username, password=password)
        graph = client.select_graph(graph_id)
        res = graph.query("RETURN 'Connection Successful!' AS status, 1 AS ping")
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        print(f"✅ SUCCESS! Connected to {host}:{port}")
        print(f"Result: {res.result_set}")
        print(f"Roundtrip Latency: {round(elapsed_ms, 2)} ms")
        success = True
        break
    except Exception as e:
        print(f"Failed on {host}: {e}")

if not success:
    print("\n❌ Could not connect with these credentials. Please check details.")
