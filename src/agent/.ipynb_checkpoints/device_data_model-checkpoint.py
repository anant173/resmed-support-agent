from pydantic import BaseModel
from traceloop.sdk.decorators import task
from typing import List, Dict, Any, Optional

class DeviceMetrics(BaseModel):
    """Represents real-time metrics for a CPAP device."""
    model_name: str
    usage_hours_last_week: float
    avg_mask_leak_rate: float
    last_service_date: str

class DeviceData(BaseModel):
    """Simulates a user's cloud-connected device data."""
    device_metrics: List[DeviceMetrics]

    @task()
    async def get_all_device_models(self) -> list[str]:
        """Returns a list of all connected device model names."""
        return [m.model_name for m in self.device_metrics]

    @task()
    async def get_metrics_by_model(self, model_name: str) -> DeviceMetrics:
        """Returns the specific metrics for a given device model.

        Raises:
            ValueError: If the device model name is not found.
        """
        for metrics in self.device_metrics:
            if model_name.lower() == metrics.model_name.lower():
                return metrics
        
        valid_models = await self.get_all_device_models()
        error_message = (
            f"Device model '{model_name}' not found. Valid models are: {', '.join(valid_models)}"
        )
        raise ValueError(error_message)

    @task()
    async def check_compliance(self, model_name: str) -> Dict[str, Any]:
        """Calculates compliance based on 7-day usage."""
        metrics = await self.get_metrics_by_model(model_name)
        
        # Compliance requires 4 hours per night, 70% of nights (4/7 nights)
        is_compliant = metrics.usage_hours_last_week >= (4 * 7 * 0.7)
        
        return {
            "compliant": is_compliant,
            "usage": f"{metrics.usage_hours_last_week:.1f} hours last week",
            "leak_rate": f"{metrics.avg_mask_leak_rate} L/min",
            "recommendation": "High leak rate may require mask refitting." if metrics.avg_mask_leak_rate > 24 else "Usage looks stable."
        }