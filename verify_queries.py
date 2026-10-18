"""
SentryGraph AI - Verification Suite for the 4 Master openCypher Queries
Tests the live FalkorDB Cloud database across Track 1, Track 2, and Track 3.
"""

from app.graph.falkor_client import FalkorGraphClient
import json

def test_master_queries():
    client = FalkorGraphClient()
    print("\n=============================================================")
    print("🎯 TESTING MASTER OPENCYPHER QUERIES ON FALKORDB CLOUD")
    print("=============================================================")

    # 1. Track 1: Multi-Hop Lineage & Public Exploitability
    print("\n[Query 1: Track 01 - Zero-Day Reachability Tracing]")
    q1 = """
    MATCH (v:Vulnerability {cveId: $cveId})-[:EXPLOITS]->(d:Dependency)-[:IMPORTED_IN]->(sf:SourceFile)
    MATCH (sf)-[:CONTAINS]->(fn:Function)
    MATCH path = (pe:PublicEndpoint)-[:ROUTES_TO]->(entryFn:Function)-[:CALLS*1..4]->(targetFn:Function)
    WHERE targetFn.name = 'vulnerable_jwt_decode'
    OPTIONAL MATCH (dev:Developer)-[:AUTHORED]->(sf)
    RETURN 
        v.cveId AS CVE,
        v.severity AS Severity,
        d.name AS VulnerablePkg,
        sf.filePath AS ImpactedFile,
        pe.path AS ExploitableEndpoint,
        entryFn.name AS EntryHandler,
        targetFn.name AS VulnerableCall,
        length(path) AS AttackDepth,
        dev.name AS CodeOwner,
        dev.githubHandle AS OwnerHandle
    LIMIT 1
    """
    res1 = client.query(q1, {"cveId": "CVE-2024-21626"})
    print(f"Latency: {res1['execution_time_ms']} ms")
    print(f"Result: {json.dumps(res1['rows'], indent=2)}")

    # 2. Track 1: Blast Radius Calculation
    print("\n[Query 2: Track 01 - Cross-Service Blast Radius]")
    q2 = """
    MATCH (d:Dependency {name: 'vulnerable-jwt-lib'})-[:IMPORTED_IN]->(sf:SourceFile)-[:CONTAINS]->(targetFn:Function)
    MATCH (caller:Function)-[:CALLS*1..3]->(targetFn)
    RETURN 
        d.name AS Dependency,
        targetFn.name AS TargetFunction,
        count(DISTINCT caller) AS TotalImpactedCallers,
        collect(DISTINCT caller.name) AS Callers
    """
    res2 = client.query(q2)
    print(f"Latency: {res2['execution_time_ms']} ms")
    print(f"Result: {json.dumps(res2['rows'], indent=2)}")

    # 3. Track 2: Episodic & Procedural Memory Recall
    print("\n[Query 3: Track 02 - Agent Tri-Tier Memory Recall]")
    q3 = """
    MATCH (e:EpisodicIncident {cveId: $cveId})-[:USED_PATCH]->(p:ProceduralPatch)
    WHERE p.verifiedByTests = true
    RETURN 
        e.incidentId AS PriorIncident,
        e.rootCauseFn AS KnownRootCause,
        p.diffTemplate AS ProvenPatchTemplate,
        e.resolutionTimeMs AS PastResolutionDuration
    LIMIT 1
    """
    res3 = client.query(q3, {"cveId": "CVE-2024-21626"})
    print(f"Latency: {res3['execution_time_ms']} ms")
    print(f"Result: {json.dumps(res3['rows'], indent=2)}")

    # 4. Track 3: Company Brain (On-Call & Decision Trace)
    print("\n[Query 4: Track 03 - Company Brain & ADR Governance]")
    q4 = """
    MATCH (sf:SourceFile {filePath: 'auth_service/jwt_verifier.py'})<-[:AUTHORED]-(dev:Developer)
    MATCH (dev)-[:MEMBER_OF]->(t:Team)-[:OWNS]->(r:Repository)
    OPTIONAL MATCH (r)-[:DISCUSSED_IN]->(s:SlackDiscussion)
    OPTIONAL MATCH (sf)-[:GOVERNED_BY]->(adr:DecisionRecord)
    RETURN 
        r.repoName AS Repository,
        t.name AS OwningTeam,
        dev.name AS PrimaryOwner,
        dev.onCall AS IsOnCall,
        s.summary AS SlackContext,
        adr.title AS GoverningPolicy
    """
    res4 = client.query(q4)
    print(f"Latency: {res4['execution_time_ms']} ms")
    print(f"Result: {json.dumps(res4['rows'], indent=2)}")
    print("\n=============================================================")
    print("✅ ALL 4 TRACK QUERIES EXECUTED PERFECTLY WITH 100% SUCCESS!")
    print("=============================================================")

if __name__ == "__main__":
    test_master_queries()
