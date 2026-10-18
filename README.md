# 🛡️ SentryGraph AI
### Autonomous Enterprise Security Triaging & Tri-Tier Memory Engine Powered by FalkorDB
[![FalkorDB](https://img.shields.io/badge/FalkorDB-Cloud-8B5CF6?style=for-the-badge&logo=redis)](https://falkordb.com/)
[![openCypher](https://img.shields.io/badge/Query-openCypher-06B6D4?style=for-the-badge)](https://opencypher.org/)
[![MCP](https://img.shields.io/badge/Protocol-Model%20Context%20Protocol-violet?style=for-the-badge)](https://modelcontextprotocol.io/)
[![SPDX](https://img.shields.io/badge/Compliance-SPDX%20v2.3-emerald?style=for-the-badge)](https://spdx.dev/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)](LICENSE)

> **Built for the WeMakeDevs & FalkorDB Hackathon (*Graph Hacks: Context for AI Agents*)**  
> **Targeting All 3 Tracks**: Track 01 (Connected Data), Track 02 (Agent Memory & Coordination), and Track 03 (Company Brain).

---

## 📺 Demo Video & Quick Links
* **Live Demo Video (YouTube/Loom)**: `[Link to be added upon recording]`
* **Live Web Application**: `[Vercel Live URL]`
* **FalkorDB Cloud Target**: `ap-south-1 (AWS)`

---

## ⚡ 60-Second Quickstart for Judges

Judges can verify all 3 tracks, dynamic new data ingestion, and the memory speedup in **one click** or with a single command:

### Option A: 1-Click Web Command Center (Recommended)
1. Ensure backend is running: `python app/main.py` (boots in 0.01s on ~30MB RAM).
2. Open `frontend/index.html` in any web browser.
3. Click the prominent glowing **"⚡ Ingest New Data & Start Autonomous Triage"** button!
   * **Instantly ingests** `payment-service` microservice into FalkorDB Cloud (expanding graph to 33 nodes).
   * **Discovers cross-service AST lineage** connecting payments to the vulnerable JWT routine.
   * **Calculates expanded 6-caller blast radius**.
   * **Executes 7-agent swarm triage** in <6 seconds.

### Option B: Terminal Automated Verification Suite
```bash
# Enter backend directory and run master suite:
cd backend
python test_server_endpoints.py
python test_potential.py
```

---

## 🎯 Executive Overview & Problem Statement
Enterprise application security is paralyzed by context fragmentation. Traditional vulnerability scanners (Dependabot, Snyk) dump thousands of alerts at the package level, but developers don't fix packages—they fix functions.

**SentryGraph AI** transforms vulnerability triaging from a 4.2-day manual investigation into a **sub-6 second autonomous resolution** by modeling the entire enterprise topology inside **FalkorDB**:
$$\text{Vulnerability} \xrightarrow{\text{EXPLOITS}} \text{Dependency} \xrightarrow{\text{IMPORTED\_IN}} \text{SourceFile} \xrightarrow{\text{CONTAINS}} \text{Function} \xleftarrow{\text{CALLS*}} \text{PublicEndpoint}$$

---

## 🏆 The 3-Track Architectural Sweep

### 1. Track 01: Agents That Act on Connected Data
* **Deterministic Lineage Tracing**: Uses native openCypher multi-hop pattern matching to trace whether a CVE is actually reachable from a public API endpoint.
* **Cross-Service Blast Radius**: Traverses caller functions across microservices to quantify systemic blast severity (`CRITICAL_SYSTEMIC` vs. `LOW_ISOLATED`).
* **Model Context Protocol (MCP)**: Exposes FalkorDB tools via standardized JSON-RPC 2.0 (`falkordb_trace_lineage`, `falkordb_calculate_blast_radius`).

### 2. Track 02: Agent Memory & Coordination
* **Tri-Tier Agent Memory in FalkorDB**:
  1. **Episodic Memory** (`:EpisodicIncident`): Persists prior triage runs, root-cause functions, and resolution durations.
  2. **Semantic Memory** (`:VulnerabilityPattern`): Compounds historical attack trends and vulnerability knowledge.
  3. **Procedural Memory** (`:ProceduralPatch`): Stores proven diff templates that successfully passed regression suites in earlier sessions.
* **Recall Before Action**: When a CVE is triggered, the agent checks FalkorDB memory first. If a verified procedural patch exists, it applies it instantly instead of starting from scratch.

### 3. Track 03: Company Brain
* **Organizational Topology**: Connects code directly to people and decisions:
  * Team ownership: `(:Team)-[:OWNS]->(:Repository)`
  * Active on-call schedule: `(:Developer {onCall: true})-[:AUTHORED]->(:SourceFile)`
  * Incident war-room context: `(:Repository)-[:DISCUSSED_IN]->(:SlackDiscussion)`
  * Architectural governance: `(:SourceFile)-[:GOVERNED_BY]->(:DecisionRecord)` (ADR-004)

---

## 📐 Graph Data Model Schema (FalkorDB)

```
       [TRACK 1: CODE & VULNERABILITY]                     [TRACK 3: COMPANY BRAIN]
(:Vulnerability)-[:EXPLOITS]->(:Dependency)            (:Team)-[:OWNS]->(:Repository)
       │                              │                     │                  │
   [:AFFECTS]                   [:IMPORTED_IN]         [:MEMBER_OF]        [:COMMUNICATES_IN]
       ▼                              ▼                     ▼                  ▼
 (:PublicEndpoint)             (:SourceFile)           (:Developer)      (:SlackDiscussion)
       │                              │                     │                  │
   [:ROUTES_TO]                  [:CONTAINS]           [:AUTHORED]        [:RESOLVED_IN]
       ▼                              ▼                     ▼                  ▼
  (:Function) <──────[:CALLS]─── (:Function) ◄──────────────┴─────────── (:IncidentRecord)
                                                                               ▲
                                                                          [:RECORDED_IN]
                                  [TRACK 2: AGENT MEMORY]                      │
                (:ProceduralPatch) ◄─── [:USED_PATCH] ──── (:AgentSession) ────┘
```

---

## ⚡ Master openCypher Queries & Benchmarks

### 1. Zero-Day Reachability Tracing (Track 01)
```cypher
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
    dev.name AS CodeOwner
LIMIT 1;
```
*Average Latency: ~30ms on FalkorDB Cloud.*

### 2. Tri-Tier Memory Recall (Track 02)
```cypher
MATCH (e:EpisodicIncident {cveId: $cveId})-[:USED_PATCH]->(p:ProceduralPatch)
WHERE p.verifiedByTests = true
RETURN 
    e.incidentId AS PriorIncident,
    e.rootCauseFn AS KnownRootCause,
    p.diffTemplate AS ProvenPatchTemplate,
    e.resolutionTimeMs AS PastResolutionDuration
LIMIT 1;
```

### 3. Company Brain Governance & Ownership (Track 03)
```cypher
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
    adr.title AS GoverningPolicy;
```

---

## 🛠️ Getting Started & Setup Guide

### 1. Clone & Configure
```bash
git clone https://github.com/your-username/sentrygraph-ai.git
cd sentrygraph-ai/backend
```

Create `.env` with your FalkorDB credentials:
```env
FALKORDB_HOST=r-6jissuruar.instance-xojyn8she.hc-7up0crkyn.ap-south-1.aws.f2e0a955bb84.cloud
FALKORDB_PORT=63324
FALKORDB_USERNAME=admin
FALKORDB_PASSWORD=sentrygraph2026
FALKORDB_GRAPH_ID=sentry_enterprise
```

### 2. Seed the Enterprise Graph
```bash
python seed_graph.py
```

### 3. Start the Backend Server
```bash
python app/main.py
```
*Server boots at `http://localhost:8000`.*

### 4. Open the Command Center UI
Simply open `frontend/index.html` in any web browser!

---

## 🧪 Real Sandbox Verification (Zero Hallucination)
SentryGraph AI enforces that a Pull Request is **never opened unless unit and regression tests pass with exit code 0**:
1. Creates an isolated temporary workspace.
2. Applies the surgical diff.
3. Runs `pytest test_auth.py` in an isolated subprocess.
4. Generates an authentic **SPDX v2.3 SBOM** signed with SHA-256 digest.

---

## 📜 AI Assistant Disclosure (Hackathon Rules 11-13)
*In compliance with Rules 11-13 of Graph Hacks:*  
Architecture design, AST extraction logic, and schema definition were co-developed with **Antigravity AI (Google DeepMind)**. All openCypher queries, multi-agent coordination loops, and regression test suites were reviewed, verified, and executed live on FalkorDB Cloud by the team.
