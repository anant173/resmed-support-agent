from langchain_core.tools import tool
from src.agent.device_data_model import DeviceData, DeviceMetrics
from traceloop.sdk.decorators import tool as traceloop_tool

# Simulated live data for the user's devices
USER_DEVICES = DeviceData(
    device_metrics=[
        DeviceMetrics(model_name="AirSense 10", usage_hours_last_week=32.5, avg_mask_leak_rate=15.2, last_service_date="2025-01-15"),
        DeviceMetrics(model_name="AirMini", usage_hours_last_week=4.0, avg_mask_leak_rate=30.1, last_service_date="2024-11-01"),
    ]
)

@tool
@traceloop_tool()
async def list_available_devices() -> str:
    """List all connected device model names for which data is available."""
    return await USER_DEVICES.get_all_device_models()

@tool
@traceloop_tool()
async def check_device_compliance(model_name: str) -> str:
    """
    Checks the user's therapy compliance metrics (usage hours and mask leak rate) 
    for a specific device model. Use the exact model name.
    """
    try:
        compliance_data = await USER_DEVICES.check_compliance(model_name)
        
        response = f"Compliance Status: {'COMPLIANT' if compliance_data['compliant'] else 'NON-COMPLIANT'}."
        response += f" Usage: {compliance_data['usage']}."
        response += f" Leak Rate: {compliance_data['leak_rate']}."
        response += f" Recommendation: {compliance_data['recommendation']}"
        return response
    except ValueError as error:
        return f"{error}"

@tool
@traceloop_tool()
async def find_troubleshooting_manual(device_model: str, issue_keywords: str) -> str:
    """
    Simulates searching a manual for specific issues (e.g., 'AirSense 10' and 'clicking sound').
    Returns a link or text snippet from the manual.
    """
    if "clicking" in issue_keywords.lower() and "airsense 10" in device_model.lower():
        return "Manual Page 52: Clicking sounds can be a symptom of filter blockage or water in the tubing. Please check and dry the tubing."
    
    return f"I found no specific manual page for '{issue_keywords}' on the {device_model}. Try simplifying your query."


tools = [list_available_devices, check_device_compliance, find_troubleshooting_manual]