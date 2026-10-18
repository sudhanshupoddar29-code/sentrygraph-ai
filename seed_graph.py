"""
SentryGraph AI - FalkorDB Enterprise Knowledge Graph Seeder
Extracts AST call graphs from code fixtures and populates FalkorDB with nodes
covering Track 1 (Connected Code), Track 2 (Agent Memory), and Track 3 (Company Brain).
"""

import os
import sys
from app.ast_parser.extractor import ASTCodeGraphExtractor
from app.graph.falkor_client import FalkorGraphClient

def seed_enterprise_graph():
    print("=============================================================")
    print("🚀 SentryGraph AI: Seeding FalkorDB Enterprise Security Graph")
    print("=============================================================")

    client = FalkorGraphClient()
    
    # 1. Initialize Indices
    print("\n[Step 1] Creating schema indices...")
    client.init_schema_indices()

    # 2. Extract AST from Code Fixtures
    fixtures_path = os.path.join(os.path.dirname(__file__), "fixtures")
    print(f"\n[Step 2] Extracting live AST from {fixtures_path}...")
    extractor = ASTCodeGraphExtractor("enterprise-core", fixtures_path)
    ast_data = extractor.extract()
    print(f" -> Found {len(ast_data['files'])} files, {len(ast_data['functions'])} functions, {len(ast_data['endpoints'])} endpoints")

    # 3. Clear existing graph data for clean slate
    client.query("MATCH (n) DETACH DELETE n")

    # 4. Insert Track 1: Vulnerability & Dependency Nodes
    print("\n[Step 3] Inserting Track 01 Vulnerability & AST Code Nodes...")
    
    client.query("""
    CREATE (v:Vulnerability {
        cveId: 'CVE-2024-21626',
        severity: 'CRITICAL',
        cvssScore: 9.8,
        vectorString: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
        description: 'Algorithm confusion in jwt_verifier allowing unverified claims parsing via header.none.'
    })
    CREATE (d:Dependency {
        name: 'vulnerable-jwt-lib',
        purl: 'pkg:pypi/vulnerable-jwt-lib@1.0.4',
        installedVersion: '1.0.4',
        fixedVersion: '1.0.5',
        ecosystem: 'pypi'
    })
    CREATE (v)-[:EXPLOITS]->(d)
    """)

    # Insert Files
    for f in ast_data['files']:
        client.query("""
        CREATE (:SourceFile {
            uid: $uid,
            repo: $repo,
            filePath: $filePath,
            lineCount: $lineCount,
            language: $language
        })
        """, f)

    # Link Dependency to Vulnerable File
    client.query("""
    MATCH (d:Dependency {name: 'vulnerable-jwt-lib'})
    MATCH (sf:SourceFile {filePath: 'auth_service/jwt_verifier.py'})
    CREATE (d)-[:IMPORTED_IN {scope: 'runtime', direct: true}]->(sf)
    """)

    # Insert Functions
    for fn in ast_data['functions']:
        client.query("""
        CREATE (:Function {
            uid: $uid,
            name: $name,
            startLine: $startLine,
            endLine: $endLine,
            isPublicEndpoint: $isPublicEndpoint
        })
        """, fn)
        
        # Link File -> Function
        client.query("""
        MATCH (sf:SourceFile {uid: $fileId})
        MATCH (fn:Function {uid: $uid})
        CREATE (sf)-[:CONTAINS]->(fn)
        """, {"fileId": fn["fileId"], "uid": fn["uid"]})

    # Insert Public Endpoints
    for ep in ast_data['endpoints']:
        client.query("""
        CREATE (pe:PublicEndpoint {
            path: $path,
            method: $method,
            repo: $repo
        })
        WITH pe
        MATCH (fn:Function {uid: $handlerFunctionUid})
        CREATE (pe)-[:ROUTES_TO]->(fn)
        """, ep)

    # Link Function Calls
    for call in ast_data['calls']:
        client.query("""
        MATCH (caller:Function {uid: $callerUid})
        MATCH (callee:Function) WHERE callee.name = $calleeName
        CREATE (caller)-[:CALLS]->(callee)
        """, call)

    # Add virtual vulnerable function node representing the external library function
    client.query("""
    CREATE (vfn:Function {
        uid: 'vulnerable-jwt-lib:vulnerable_jwt_decode',
        name: 'vulnerable_jwt_decode',
        startLine: 1,
        endLine: 20,
        isPublicEndpoint: false
    })
    WITH vfn
    MATCH (targetFn:Function {name: 'verify_session_token'})
    CREATE (targetFn)-[:CALLS]->(vfn)
    WITH vfn
    MATCH (d:Dependency {name: 'vulnerable-jwt-lib'})
    CREATE (d)-[:EXPOSES_ROUTINE]->(vfn)
    """)

    # 5. Insert Track 2: Tri-Tier Memory (Episodic, Semantic, Procedural)
    print("\n[Step 4] Inserting Track 02 Tri-Tier Agent Memory...")
    client.query("""
    CREATE (sess:AgentSession {
        sessionId: 'sess_prev_098',
        timestamp: '2026-10-12T04:22:00Z',
        userPrompt: 'Security triage on auth token bypass',
        status: 'RESOLVED'
    })
    CREATE (epi:EpisodicIncident {
        incidentId: 'inc_jwt_042',
        cveId: 'CVE-2024-21626',
        resolutionTimeMs: 7420,
        rootCauseFn: 'verify_session_token',
        summary: 'Resolved algorithm confusion by enforcing verify_signature=True and upgrading dependency.'
    })
    CREATE (proc:ProceduralPatch {
        patchId: 'patch_jwt_105',
        ecosystem: 'pypi',
        diffTemplate: 'claims = vulnerable_jwt_decode(token, verify_signature=True)',
        verifiedByTests: true
    })
    CREATE (sess)-[:RECORDED_INCIDENT]->(epi)
    CREATE (epi)-[:USED_PATCH]->(proc)
    """)

    # 6. Insert Track 3: Company Brain (Teams, Repos, Slack, Decision Records)
    print("\n[Step 5] Inserting Track 03 Enterprise Company Brain...")
    client.query("""
    CREATE (t:Team {
        name: 'Core-Identity-Team',
        slackChannel: '#sec-auth-war-room',
        escalationTier: 1
    })
    CREATE (dev1:Developer {
        name: 'Alex Vance',
        email: 'alex.vance@enterprise.com',
        githubHandle: 'avance-sec',
        onCall: true,
        role: 'Staff Security Engineer'
    })
    CREATE (dev2:Developer {
        name: 'Elena Rostova',
        email: 'elena.r@enterprise.com',
        githubHandle: 'erostova-dev',
        onCall: false,
        role: 'Senior Backend Engineer'
    })
    CREATE (repo:Repository {
        repoName: 'enterprise-core',
        defaultBranch: 'main',
        criticalTier: 'Tier-1'
    })
    CREATE (slack:SlackDiscussion {
        channelId: 'C081299',
        summary: 'Discussed upgrading JWT library to 1.0.5 after vulnerability alert. Assigned to Alex Vance.',
        permalink: 'https://slack.enterprise.internal/archives/C081299/p1728892'
    })
    CREATE (adr:DecisionRecord {
        adrId: 'ADR-004',
        title: 'Mandatory Cryptographic Verification for External JWTs',
        status: 'ACCEPTED',
        rationale: 'Prevent algorithm confusion attacks across all microservices; unverified parsing prohibited.'
    })
    CREATE (dev1)-[:MEMBER_OF]->(t)
    CREATE (dev2)-[:MEMBER_OF]->(t)
    CREATE (t)-[:OWNS]->(repo)
    CREATE (repo)-[:DISCUSSED_IN]->(slack)
    """)

    # Link Developer to SourceFiles & Decision Record
    client.query("""
    MATCH (dev1:Developer {githubHandle: 'avance-sec'})
    MATCH (sf:SourceFile {filePath: 'auth_service/jwt_verifier.py'})
    MATCH (adr:DecisionRecord {adrId: 'ADR-004'})
    CREATE (dev1)-[:AUTHORED {commitHash: '7f9a12c', lastModified: '2026-09-14'}]->(sf)
    CREATE (sf)-[:GOVERNED_BY]->(adr)
    """)

    # 7. Verification Summary
    print("\n=============================================================")
    count_res = client.query("MATCH (n) RETURN count(n) AS totalNodes")
    total_nodes = count_res['rows'][0]['totalNodes'] if count_res['success'] and count_res['rows'] else 0
    rel_res = client.query("MATCH ()-[r]->() RETURN count(r) AS totalRels")
    total_rels = rel_res['rows'][0]['totalRels'] if rel_res['success'] and rel_res['rows'] else 0
    
    print(f"✅ Seeding Complete! Total Nodes: {total_nodes} | Total Relationships: {total_rels}")
    print("=============================================================")

if __name__ == "__main__":
    seed_enterprise_graph()
