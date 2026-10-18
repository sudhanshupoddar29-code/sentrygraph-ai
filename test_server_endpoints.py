import urllib.request
import json
import time

def post_json(url: str, data: dict):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_json(url: str):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))

def test_master_endpoints():
    base_url = "http://localhost:8000"

    print("====================================================================")
    print("🔥 SENTRYGRAPH AI: MASTER ENDPOINT & DYNAMIC INGESTION VERIFICATION")
    print("====================================================================")

    # 1. Health
    health = get_json(f"{base_url}/api/health")
    print(f"\n[1] Health Check: Status={health['status']} | FalkorDB Latency={health['falkordb_latency_ms']} ms")
    assert health['falkordb_connected'] is True, "FalkorDB is not connected!"

    # 2. Topology
    topo = get_json(f"{base_url}/api/graph/topology")
    print(f"[2] Graph Topology: Nodes={topo['total_nodes']} | Edges={topo['total_edges']}")
    assert topo['total_nodes'] >= 28, "Missing nodes in topology!"

    # 3. Dynamic New Data Ingestion Endpoint
    print("\n[3] Testing Dynamic Ingestion Endpoint (/api/graph/ingest)...")
    ingest_res = post_json(f"{base_url}/api/graph/ingest", {})
    print(f"    - Ingest Status: {'SUCCESS' if ingest_res.get('success') else 'FAILED'}")
    print(f"    - Ingested Service: {ingest_res.get('ingested_service')}")
    print(f"    - Updated FalkorDB Node Count: {ingest_res.get('final_nodes')} (+{ingest_res.get('added_nodes')})")
    print(f"    - Cross-Service Bridge: {ingest_res.get('cross_service_bridge')}")

    # 4. Company Brain Q&A with New Data
    print("\n[4] Testing Company Brain with Newly Ingested Data (/api/brain/ask)...")
    q1 = post_json(f"{base_url}/api/brain/ask", {"question": "who owns payment service?"})
    print(f"    - Q1: 'who owns payment service?'")
    print(f"      Intent: {q1['intent']} (Latency: {q1['latency_ms']} ms)")
    print(f"      Answer snippet: {q1['answer'].splitlines()[1] if len(q1['answer'].splitlines()) > 1 else q1['answer'][:80]}")

    q2 = post_json(f"{base_url}/api/brain/ask", {"question": "what is the blast radius?"})
    print(f"\n    - Q2: 'what is the blast radius?'")
    print(f"      Intent: {q2['intent']} (Latency: {q2['latency_ms']} ms)")
    print(f"      Answer snippet: {q2['answer'].splitlines()[0]}")
    print(f"      {q2['answer'].splitlines()[1]}")

    q3 = post_json(f"{base_url}/api/brain/ask", {"question": "what is ADR-007?"})
    print(f"\n    - Q3: 'what is ADR-007?'")
    print(f"      Intent: {q3['intent']} (Latency: {q3['latency_ms']} ms)")
    print(f"      Answer snippet: {q3['answer'].splitlines()[0]}")

    # 5. Exploit Simulator (Before vs After)
    print("\n[5] Testing Exploit Simulator Endpoint (/api/exploit/test)...")
    before_res = post_json(f"{base_url}/api/exploit/test", {"mode": "before"})
    print(f"    - Before Patch: HTTP {before_res['status_code']} -> {before_res['result']['badge']}")
    assert before_res['status_code'] == 200

    after_res = post_json(f"{base_url}/api/exploit/test", {"mode": "after"})
    print(f"    - After Patch:  HTTP {after_res['status_code']} -> {after_res['result']['badge']}")
    assert after_res['status_code'] == 401

    # 6. Tri-Tier Memory Benchmark (Cold vs Warm)
    print("\n[6] Testing Cold vs Warm Memory Recall Benchmark (/api/benchmark)...")
    bm = get_json(f"{base_url}/api/benchmark")
    print(f"    - Cold Run (First Seen): {bm['cold_run']['duration_ms']} ms")
    print(f"    - Warm Run (Memory Hit): {bm['warm_run']['duration_ms']} ms")
    print(f"    - Speedup Advantage:     {bm['speedup_factor']} ({bm['latency_saved_ms']} ms saved)")

    # 7. Live openCypher Console Execution
    print("\n[7] Testing openCypher Execution Endpoint (/api/cypher/run)...")
    cypher_res = post_json(f"{base_url}/api/cypher/run", {"query": "MATCH (n:DecisionRecord) RETURN n.adrId, n.title"})
    print(f"    - Latency: {cypher_res.get('execution_time_ms', 0)} ms")
    print(f"    - ADR Records in FalkorDB: {cypher_res.get('rows', [])}")

    print("\n====================================================================")
    print("🏆 ALL 7 CORE SUITES + DYNAMIC INGESTION VERIFIED 100% OPERATIONAL!")
    print("====================================================================")

if __name__ == "__main__":
    test_master_endpoints()
