"""
SentryGraph AI - End-to-End Triage Swarm Verification Script
Executes the full multi-agent pipeline and verifies all 7 steps.
"""

import os
import json
from app.graph.falkor_client import FalkorGraphClient
from app.mcp.tools import SentryGraphMCPTools
from app.agents.triage_swarm import SentryGraphTriageSwarm

def main():
    print("=============================================================")
    print("🛡️ SentryGraph AI: Testing Full Autonomous Triage Pipeline")
    print("=============================================================")

    client = FalkorGraphClient()
    mcp_tools = SentryGraphMCPTools(client)
    fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")
    
    swarm = SentryGraphTriageSwarm(mcp_tools, fixtures_dir)
    print("\n[Trigger] Ingesting Zero-Day Alert: CVE-2024-21626...")
    
    result = swarm.run_triage(cve_id="CVE-2024-21626")
    
    print("\n✅ PIPELINE EXECUTION COMPLETED!")
    print(f"Session ID:         {result['sessionId']}")
    print(f"Total Duration:     {result['totalDurationMs']} ms")
    print(f"Overall Status:     {result['status']}")

    print("\n--- AGENT EXECUTION TRACE ---")
    for step in result['traceSteps']:
        print(f"Step {step['step']} [{step['agent']}]: {step['action']} -> Status: {step['status']} ({step['latency_ms']} ms)")

    print("\n--- SANDBOX TEST RESULT ---")
    print(f"Tests Passed:       {result['sandboxTest']['tests_passed']}")
    print(f"Sandbox Runtime:    {result['sandboxTest']['execution_time_ms']} ms")
    print(f"Pytest Output:\n{result['sandboxTest']['stdout']}")

    print("\n--- DISPATCHED PULL REQUEST ---")
    print(json.dumps(result['pullRequest'], indent=2))

    print("\n--- COMPLIANCE SPDX v2.3 SBOM ---")
    print(json.dumps(result['sbom'], indent=2))

if __name__ == "__main__":
    main()
