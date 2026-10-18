import json
from app.ast_parser.extractor import ASTCodeGraphExtractor

extractor = ASTCodeGraphExtractor("enterprise-core", "./fixtures")
graph_data = extractor.extract()

print("--- AST EXTRACTION SUMMARY ---")
print(f"Total Files Extracted: {len(graph_data['files'])}")
print(f"Total Functions Extracted: {len(graph_data['functions'])}")
print(f"Total Internal Function Calls: {len(graph_data['calls'])}")
print(f"Total Public Endpoints Discovered: {len(graph_data['endpoints'])}")

print("\n--- DISCOVERED PUBLIC ENDPOINTS ---")
for ep in graph_data['endpoints']:
    print(f"[{ep['method']}] {ep['path']} -> Handler: {ep['handlerFunctionUid']}")

print("\n--- SAMPLE CALL RELATIONSHIPS ---")
for call in graph_data['calls'][:8]:
    print(f"{call['callerUid']} --CALLS--> {call['calleeName']}")
