# Evaluation Metrics for the ResMed CPAP Troubleshooting Agent

Defining success for an AI agent requires measuring more than just general accuracy. For a sensitive domain like respiratory care, we must ensure safety, compliance, and utility.

## 1. Domain-Specific Success Metrics

These metrics verify that the agent adheres to its primary safety and clinical mission.

### A. Safety and Compliance Adherence (Critical)
| Metric | Definition | Success Criteria |
| :--- | :--- | :--- |
| **Safety Evasion Rate** | The percentage of times the agent provides therapeutic advice (e.g., changing pressure settings) without explicit tool-based data or a clear clinical trigger. | Must be **0%**. Any violation is a failure. |
| **Compliance Diagnosis Accuracy** | The accuracy of the agent's diagnosis (e.g., COMPLIANT vs. NON-COMPLIANT) compared to the actual deterministic output of the `check_device_compliance` tool. | Must be **100%** on validation sets. |
| **Tool Utility Rate** | The percentage of queries where the agent correctly identified the need for and successfully called a relevant tool (e.g., using `find_troubleshooting_manual` for a device complaint). | Should be **high (>90%)** for troubleshooting queries, ensuring it uses data before responding. |

### B. Functional Utility
| Metric | Definition | Success Criteria |
| :--- | :--- | :--- |
| **Troubleshooting Specificity** | Measures if the final answer incorporates specific keywords or references from the tool's output (e.g., citing "Manual Page 52" or "mask refitting"). | Final response must explicitly reference tool output 95% of the time when a tool is called. |

---

## 2. General Agent Performance Metrics

These metrics cover the technical performance, efficiency, and faithfulness of the model's reasoning.

### A. Observability Metrics (MLOps)
| Metric | Definition | Impact |
| :--- | :--- | :--- |
| **End-to-End Latency** | Total time elapsed from user input to receiving the final response. | Critical for user experience (e.g., P95 latency < 3 seconds). |
| **Tool Execution Latency** | Time spent running the external tools (e.g., `check_device_compliance`). | Helps identify bottlenecks in the external data system (`device_data_model.py`). |
| **Cost Per Query** | The total cost of LLM tokens used per interaction (including intermediate reasoning steps). | Essential for managing operational expenses. |

### B. Reasoning Quality Metrics
| Metric | Definition | Role in Agent |
| :--- | :--- | :--- |
| **Faithfulness** | Measures if the LLM's final generated answer is consistent with and supported by the information it received from the tool outputs. | Ensures the agent doesn't hallucinate conclusions based on tool data. |
| **Completeness** | Measures if the agent addresses all parts of a complex query (e.g., if a user asks for compliance and troubleshooting, were both addressed?). | Verifies the prompt handling and state management. |

---

### Running Evaluation Workflows

To implement these metrics systematically (Module 11.6), you would create an evaluation pipeline (e.g., using LangChain's evaluation tools or a custom script) that runs against a pre-defined **test set of scenarios** (e.g., 50 prompts covering compliance checks, troubleshooting, and tricky, non-tool-related queries).

This setup ensures that any change you make to the prompt, the LLM model, or the tool logic is systematically validated against these critical safety and accuracy benchmarks before deployment.
