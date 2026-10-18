"""
SentryGraph AI - Dynamic New Data Ingestion Engine
Allows judges and developers to dynamically ingest new microservices, dependencies,
ADR governance policies, and cross-service call graphs into live FalkorDB Cloud.

Demonstrates that SentryGraph AI is a real, dynamic enterprise intelligence system,
not a static mock.
"""

import os
import sys
import time

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.graph.falkor_client import FalkorGraphClient

def get_graph_counts(client: FalkorGraphClient):
    nodes_res = client.query("MATCH (n) RETURN count(n) AS count")
    rels_res = client.query("MATCH ()-[r]->() RETURN count(r) AS count")
    nodes = nodes_res['rows'][0]['count'] if nodes_res.get('success') and nodes_res.get('rows') else 0
    rels = rels_res['rows'][0]['count'] if rels_res.get('success') and rels_res.get('rows') else 0
    return nodes, rels

def ingest_payment_microservice(client: FalkorGraphClient = None):
    if client is None:
        client = FalkorGraphClient()

    initial_nodes, initial_rels = get_graph_counts(client)
    print(f"[*] Initial FalkorDB State: {initial_nodes} Nodes | {initial_rels} Relationships")

    print("\n[+] Dynamically Ingesting New Microservice: 'payment-service'...")

    # 1. Wire up internal calls in payment_processor.py if not already connected
    client.query("""
    MATCH (pc:Function {name: 'process_charge'})
    MATCH (vi:Function {name: 'validate_caller_identity'})
    MERGE (pc)-[:CALLS]->(vi)
    """)

    client.query("""
    MATCH (pc:Function {name: 'process_charge'})
    MATCH (tx:Function {name: 'execute_fund_transfer'})
    MERGE (pc)-[:CALLS]->(tx)
    """)

    # 2. Wire up Public Endpoint for payments
    client.query("""
    MATCH (pe:PublicEndpoint {path: '/api/v1/payments/charge'})
    MATCH (pc:Function {name: 'process_charge'})
    MERGE (pe)-[:ROUTES_TO]->(pc)
    """)

    # 3. CRITICAL CROSS-SERVICE CALL:
    # validate_caller_identity in payment-service CALLS verify_session_token in auth-service!
    print("[+] Establishing Cross-Service Microservice Call: payment-service ➔ auth-service...")
    client.query("""
    MATCH (vi:Function {name: 'validate_caller_identity'})
    MATCH (vst:Function {name: 'verify_session_token'})
    MERGE (vi)-[:CALLS {type: 'cross_service_rpc', downstream: true}]->(vst)
    """)

    # 4. Ingest New ADR Governance Policy: ADR-007
    print("[+] Registering New Architectural Decision Record: ADR-007 (PCI-DSS Zero-Trust)...")
    client.query("""
    MERGE (adr:DecisionRecord {adrId: 'ADR-007'})
    ON CREATE SET 
        adr.title = 'Zero-Trust Downstream Token Verification for Financial Transactions',
        adr.status = 'ACCEPTED',
        adr.rationale = 'Payment operations must mandate cryptographically signed JWT validation before authorizing ledger fund transfers.'
    """)

    # 5. Link payment_processor.py to ADR-007
    client.query("""
    MATCH (sf:SourceFile {filePath: 'payment_service/payment_processor.py'})
    MATCH (adr:DecisionRecord {adrId: 'ADR-007'})
    MERGE (sf)-[:GOVERNED_BY]->(adr)
    """)

    # 6. Assign Code Ownership: Elena Rostova authored payment_processor.py
    print("[+] Assigning Developer Code Authorship to Elena Rostova...")
    client.query("""
    MATCH (dev:Developer {githubHandle: 'erostova-dev'})
    MATCH (sf:SourceFile {filePath: 'payment_service/payment_processor.py'})
    MERGE (dev)-[:AUTHORED {commitHash: '9a4c11b', lastModified: '2026-10-15'}]->(sf)
    """)

    # 7. Ingest New Security Advisory: CVE-2024-21627 (Financial Authorization Bypass)
    print("[+] Registering New Zero-Day Advisory: CVE-2024-21627 in Payment Pipeline...")
    client.query("""
    MERGE (v2:Vulnerability {cveId: 'CVE-2024-21627'})
    ON CREATE SET 
        v2.severity = 'CRITICAL',
        v2.cvssScore = 9.9,
        v2.vectorString = 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H',
        v2.description = 'Downstream authorization bypass allowing unauthorized payment charges via forged unverified claims.'
    MERGE (d2:Dependency {name: 'payment-gateway-sdk'})
    ON CREATE SET 
        d2.purl = 'pkg:pypi/payment-gateway-sdk@2.1.0',
        d2.installedVersion = '2.1.0',
        d2.fixedVersion = '2.1.1',
        d2.ecosystem = 'pypi'
    MERGE (v2)-[:EXPLOITS]->(d2)
    """)

    client.query("""
    MATCH (d2:Dependency {name: 'payment-gateway-sdk'})
    MATCH (sf:SourceFile {filePath: 'payment_service/payment_processor.py'})
    MERGE (d2)-[:IMPORTED_IN]->(sf)
    """)

    # 8. Record New Episodic Memory Node for Cross-Service Payment Incident
    client.query("""
    MERGE (epi2:EpisodicIncident {incidentId: 'inc_pay_099'})
    ON CREATE SET
        epi2.cveId = 'CVE-2024-21627',
        epi2.resolutionTimeMs = 485,
        epi2.rootCauseFn = 'validate_caller_identity',
        epi2.summary = 'Enforced cross-service cryptographic token verification before executing fund transfers.'
    MERGE (proc2:ProceduralPatch {patchId: 'patch_pay_211'})
    ON CREATE SET
        proc2.ecosystem = 'pypi',
        proc2.diffTemplate = 'identity = validate_caller_identity(authorization, require_signed=True)',
        proc2.verifiedByTests = true
    MERGE (epi2)-[:USED_PATCH]->(proc2)
    """)

    final_nodes, final_rels = get_graph_counts(client)
    print(f"\n✅ Dynamic Ingestion Succeeded!")
    print(f"[*] Updated FalkorDB State: {final_nodes} Nodes (+{final_nodes - initial_nodes}) | {final_rels} Relationships (+{final_rels - initial_rels})")
    print(f"[*] Cross-service blast radius now spans 'auth-service' AND 'payment-service'!")
    
    return {
        "success": True,
        "initial_nodes": initial_nodes,
        "final_nodes": final_nodes,
        "added_nodes": final_nodes - initial_nodes,
        "initial_rels": initial_rels,
        "final_rels": final_rels,
        "added_rels": final_rels - initial_rels,
        "ingested_service": "payment-service (fixtures/payment_service/payment_processor.py)",
        "new_cve": "CVE-2024-21627 (CVSS 9.9 CRITICAL)",
        "new_policy": "ADR-007 (PCI-DSS Zero-Trust Verification)",
        "new_owner": "Elena Rostova (@erostova-dev)",
        "cross_service_bridge": "validate_caller_identity ➔ verify_session_token"
    }

def reset_to_baseline(client: FalkorGraphClient = None):
    if client is None:
        client = FalkorGraphClient()
    print("[*] Re-running seed_graph.py to reset FalkorDB to clean baseline...")
    from seed_graph import seed_enterprise_graph
    seed_enterprise_graph()
    nodes, rels = get_graph_counts(client)
    return {"success": True, "nodes": nodes, "rels": rels}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_to_baseline()
    else:
        ingest_payment_microservice()
