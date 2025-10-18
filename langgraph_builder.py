#!/usr/bin/env python3
"""
LangGraph Executor — dynamically runs workflow-defined agents.
Supports modular agents under /agents and mock-ready testing.
"""
import os
import json
import importlib
import traceback
import argparse
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

# Default workflow path
WORKFLOW_FILE = os.path.join(os.path.dirname(__file__), "workflow.json")


class LangGraphExecutor:
    def __init__(self, workflow_path: str = WORKFLOW_FILE):
        """Initialize workflow and execution context."""
        if not os.path.exists(workflow_path):
            raise FileNotFoundError(f"Workflow file not found: {workflow_path}")

        with open(workflow_path, "r", encoding="utf-8") as f:
            self.workflow = json.load(f)

        self.context = {"config": self.workflow.get("config", {})}
        print(f"✅ Loaded workflow: {self.workflow.get('workflow_name', 'Unnamed Workflow')}")

    # ------------------------------
    # Utility: Resolve ${path.to.value}
    # ------------------------------
    def resolve(self, value):
        """Recursively resolve template strings like ${step.output.key} from context."""
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            path = value[2:-1].split(".")
            cur = self.context
            for p in path:
                if isinstance(cur, dict) and p in cur:
                    cur = cur[p]
                else:
                    print(f"⚠️  Could not resolve {value} — path not found in context.")
                    return None
            return cur
        elif isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.resolve(v) for v in value]
        return value

    # ------------------------------
    # Core: Run one workflow step
    # ------------------------------
    def run_step(self, step):
        sid = step["id"]
        agent_name = step["agent"]
        print(f"\n🚀 Running Step [{sid}] — Agent: {agent_name}")

        # Resolve inputs dynamically
        inputs = {k: self.resolve(v) for k, v in step.get("inputs", {}).items()}

        # Dynamically import the agent
        try:
            module_name = f"agents.{agent_name.lower()}"
            module = importlib.import_module(module_name)
            AgentClass = getattr(module, agent_name)
        except Exception as e:
            print(f"⚠️  Import failed for {agent_name}, using BaseAgent. Error: {e}")
            module = importlib.import_module("agents.base")
            AgentClass = getattr(module, "BaseAgent")

        # Instantiate and execute
        agent = AgentClass(step=step, env=os.environ)
        try:
            output = agent.run(inputs)
        except Exception as e:
            print(f"❌ Agent {agent_name} failed:\n{traceback.format_exc()}")
            output = {"error": str(e)}

        # Save output to context
        self.context.setdefault(sid, {})["output"] = output
        print(f"✅ Step {sid} completed. Output keys: {list(output.keys())}")

    # ------------------------------
    # Main: Run full workflow
    # ------------------------------
    def run(self):
        print("\n🧩 Starting LangGraph Workflow Execution")
        for step in self.workflow.get("steps", []):
            self.run_step(step)
        print("\n🏁 Workflow execution completed successfully!")


# ------------------------------
# CLI entrypoint
# ------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LangGraph workflow.")
    parser.add_argument("--workflow", type=str, default=WORKFLOW_FILE, help="Path to workflow.json")
    parser.add_argument("--dump", action="store_true", help="Print final context JSON")
    args = parser.parse_args()

    executor = LangGraphExecutor(args.workflow)
    executor.run()

    if args.dump:
        print("\n=== Final Workflow Context ===")
        print(json.dumps(executor.context, indent=2))
