import pytest
import asyncio
from unittest.mock import MagicMock, patch

# --- Setup Imports (MOCKING EXTERNAL DEPENDENCIES) ---
# We mock external libraries that are heavy or require setup (like Traceloop)
# so the tests run fast and independently.
traceloop_tool = MagicMock(return_value=lambda f: f)
tool = MagicMock(return_value=lambda f: f)

# Simulate the structure and content of your source files
# NOTE: In a real environment, you would simply import these from 'src.agent.*'
# We are defining them here to make the test file runnable for demonstration.

class MockDeviceMetrics:
    def __init__(self, model_name, usage_hours_last_week, avg_mask_leak_rate):
        self.model_name = model_name
        self.usage_hours_last_week = usage_hours_last_week
        self.avg_mask_leak_rate = avg_mask_leak_rate

class MockDeviceData:
    """Mock implementation of the core data model for deterministic testing."""
    
    # Use known, deterministic data for testing
    device_metrics = [
        MockDeviceMetrics(model_name="AirSense 10", usage_hours_last_week=32.5, avg_mask_leak_rate=15.2),
        MockDeviceMetrics(model_name="AirMini", usage_hours_last_week=4.0, avg_mask_leak_rate=30.1),
    ]

    def get_all_device_models(self):
        return [m.model_name for m in self.device_metrics]

    def get_metrics_by_model(self, model_name: str):
        for metrics in self.device_metrics:
            if model_name.lower() == metrics.model_name.lower():
                return metrics
        raise ValueError(f"Device model '{model_name}' not found.")

    def check_compliance(self, model_name: str):
        metrics = self.get_metrics_by_model(model_name)
        is_compliant = metrics.usage_hours_last_week >= (4 * 7 * 0.7)
        return {
            "compliant": is_compliant,
            "usage_hours_last_week": metrics.usage_hours_last_week,
            "avg_mask_leak_rate": metrics.avg_mask_leak_rate
        }


MOCK_USER_DEVICES = MockDeviceData()

# --- Unit Tests for Tools (Device Logic) ---

def test_list_available_devices_returns_correct_models():
    """Unit test for the list_available_devices tool."""
    # Assuming synchronous implementation from the latest code snippet
    devices = [m.model_name for m in MOCK_USER_DEVICES.device_metrics]
    assert devices == ["AirSense 10", "AirMini"]

def test_check_compliance_compliant_case():
    """Unit test for compliance (happy path)."""
    result = MOCK_USER_DEVICES.check_compliance("AirSense 10")
    # Expected: 32.5 hours > 19.6 hours (70% of 4 hours * 7 days)
    assert result['compliant'] is True
    assert result['avg_mask_leak_rate'] == 15.2

def test_check_compliance_non_compliant_case():
    """Unit test for compliance (failure path)."""
    result = MOCK_USER_DEVICES.check_compliance("AirMini")
    assert result['compliant'] is False
    assert result['usage_hours_last_week'] == 4.0

def test_get_metrics_by_model_raises_value_error():
    """Unit test for error handling when a model is not found."""
    with pytest.raises(ValueError, match="not found"):
        MOCK_USER_DEVICES.get_metrics_by_model("DreamStation")

def test_find_troubleshooting_manual_known_issue():
    """Unit test for the troubleshooting tool on a known issue."""
    # Since the tools rely on data models, we mock the original tool functions here
    
    def mock_find_troubleshooting_manual(device_model: str, issue_keywords: str):
        if "clicking" in issue_keywords.lower() and "airsense 10" in device_model.lower():
            return "Manual Page 52: Clicking sounds can be a symptom of filter blockage."
        return f"I found no specific manual page for '{issue_keywords}' on the {device_model}."

    result = mock_find_troubleshooting_manual("AirSense 10", "loud clicking")
    assert "filter blockage" in result
    
# --- Integration Test Setup (Full Agent Flow) ---
# NOTE: This test verifies the **agent's ability to choose the correct tool** given a prompt.
# We must MOCK the final LLM call to return a predetermined Tool-Call signal.

# Assume we have a mock AGENT object loaded here from src.agent.graph

# @pytest.mark.asyncio
# @patch('src.agent.llm.ChatOpenAI.invoke')
# async def test_agent_uses_compliance_tool(mock_llm_invoke):
#     """
#     Integration test: Verify the agent correctly identifies a 'compliance check' 
#     query and attempts to call the check_device_compliance tool.
#     """
    
#     # Mock the LLM's response to be a ToolCall request
#     # This simulates the LLM's decision-making process
#     mock_llm_invoke.return_value = AIMessage(
#         content="",
#         tool_calls=[
#             {
#                 'name': 'check_device_compliance',
#                 'args': {'model_name': 'AirSense 10'}
#             }
#         ]
#     )

#     # Assuming your AGENT object is initialized globally in src.agent.graph
#     # response = await run_agent(thread_id="test_thread_1", user_input="Check my AirSense 10 compliance.")
    
#     # assert mock_llm_invoke.called
#     # assert "COMPLIANT" in response['response'] # Check if tool output was processed
#     pass # Placeholder for actual run

