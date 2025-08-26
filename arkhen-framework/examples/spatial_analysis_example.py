import sys
import os
import asyncio

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from zai_integration import ZAIIntegration

# Mock classes for the dependencies of ZAIIntegration
class MockMeshNetwork:
    def __init__(self):
        self.nodes = ["node1", "node2", "node3"]

    def get_nodes(self):
        return self.nodes

class MockConsensus:
    def __init__(self):
        self.agreements = 0

    def reach_consensus(self, data):
        self.agreements += 1
        return {"status": "agreement", "data": data}

class MockLedger:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        return len(self.records) - 1

async def run_spatial_analysis_example():
    """
    Runs an example of using the ZAIIntegration class.
    """
    print("--- Running Spatial Analysis Example ---")

    # 1. Create mock dependencies
    mesh_network = MockMeshNetwork()
    consensus = MockConsensus()
    ledger = MockLedger()

    # 2. Instantiate ZAIIntegration
    print("\nInstantiating ZAIIntegration...")
    zai_analyzer = ZAIIntegration(mesh_network, consensus, ledger)

    # 3. Analyze telemetry data
    print("\n--- Analyzing Telemetry Data ---")
    satellite_id = "SAT-42"
    telemetry_data = {
        'battery_level': 25,
        'temperature': 85,
        'solar_panel_efficiency': 0.9,
        'position': [123.45, -67.89, 10.11],
        'velocity': [7.5, -1.2, 0.5],
        'timestamp': '2025-08-26T12:00:00Z'
    }
    print(f"Analyzing telemetry for {satellite_id}...")
    analysis_result = await zai_analyzer.analyze_telemetry_with_zai(satellite_id, telemetry_data)
    print("Analysis Result:")
    print(analysis_result)

    # 4. Generate a mission plan
    print("\n--- Generating Mission Plan ---")
    mission_objective = {
        "name": "Lunar South Pole Resource Mapping",
        "target": "Lunar South Pole",
        "objective": "Map water ice deposits in permanently shadowed regions."
    }
    constraints = {
        "max_duration_days": 90,
        "max_budget_usd": 100000000
    }
    print("Generating mission plan...")
    mission_plan = await zai_analyzer.generate_mission_plan(mission_objective, constraints)
    print("Mission Plan:")
    import json
    print(json.dumps(mission_plan, indent=2))

    # 5. Print usage metrics
    print("\n--- Usage Metrics ---")
    print(zai_analyzer.usage_metrics)

if __name__ == "__main__":
    asyncio.run(run_spatial_analysis_example())
