import os
from azure.identity import InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.monitor import MonitorManagementClient

# -----------------------------
# STEP 1: Azure Authentication & Setup
# -----------------------------
tenant_id = "your_tenant_id"
subscription_id = "your_subscription_id"
resource_group_name = "SecurityRG"
location = "eastasia"

# --- IMPORTANT: Placeholder for the resource you are protecting ---
# A WAF Policy must be attached to an Application Gateway or Azure Front Door.
# The METRICS  from THAT resource, not the policy itself.
# You must replace this with the actual Resource ID of your Application Gateway.
# For example: "/scomeubscriptions/.../providers/Microsoft.Network/applicationGateways/myAppGateway"
PROTECTED_RESOURCE_ID = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/applicationGateways/"give_your_applicationgateway_name"

credential = InteractiveBrowserCredential(tenant_id=tenant_id)

# Clients
resource_client = ResourceManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
monitor_client = MonitorManagementClient(credential, subscription_id)

# -----------------------------
# STEP 2: Create Resource Group
# -----------------------------
print("Creating resource group...")
resource_client.resource_groups.create_or_update(
    resource_group_name,
    {"location": location}
)
print(f"Resource group '{resource_group_name}' created.")

# -----------------------------
# STEP 3: Create WAF Policy
# -----------------------------
print("Creating Azure WAF policy...")
waf_policy = network_client.web_application_firewall_policies.create_or_update(
    resource_group_name,
    "MyWAFPolicy",
    {
        "location": location,
        "sku": {
            "name": "WAF_v2" # SKU is required for WAF policy
        },
        "policy_settings": {
            "enabled_state": "Enabled",
            "mode": "Prevention"
        },
        "managed_rules": {
            "managed_rule_sets": [
                {
                    "rule_set_type": "OWASP",
                    "rule_set_version": "3.2"
                }
            ]
        }
    }
)
print(f"WAF Policy created: {waf_policy.id}")

# -----------------------------
# STEP 4: Response Layer (Create Action Group FIRST)
# -----------------------------
print("Creating action group (email notification)...")
action_group = monitor_client.action_groups.create_or_update(
    resource_group_name,
    "SecurityAlertsGroup",
    {
        "location": "Global", # Action Groups are global resources
        "group_short_name": "SecGrp",
        "enabled": True,
        "email_receivers": [
            {
                "name": "AdminEmail",
                "email_address": "prasanth25sam@gmail.com",
                "use_common_alert_schema": True
            }
        ]
    }
)
print(f"Action group created: {action_group.id}")

# -----------------------------
# STEP 5: Detection Layer (Create Alert with correct criteria and scope)
# -----------------------------
from azure.mgmt.monitor.models import (
    MetricAlertResource,
    MetricAlertSingleResourceMultipleMetricCriteria,
    MetricCriteria
)

print("Creating Azure Monitor alert...")

# Define the alert criteria
criteria = MetricAlertSingleResourceMultipleMetricCriteria(
    all_of=[
        MetricCriteria(
            name="WAFRequestsExceeded",
            metric_name="TotalRequests",
            metric_namespace="Microsoft.Network/applicationGateways",
            operator="GreaterThan",
            threshold=100,          # your threshold
            time_aggregation="Total"
        )
    ]
)

# Create the metric alert
alert_rule = monitor_client.metric_alerts.create_or_update(
    resource_group_name,
    "SecurityAlertRule",
    MetricAlertResource(
        location="global",
        description="Alert when WAF policy triggers requests exceeding threshold",
        severity=2,
        enabled=True,
        scopes=[PROTECTED_RESOURCE_ID],  # Resource emitting metrics (App Gateway)
        evaluation_frequency="PT1M",
        window_size="PT5M",
        criteria=criteria,
        actions=[
            {
                "action_group_id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/microsoft.insights/actionGroups/SecurityAlertsGroup"
            }
        ]
    )
)

print("✅ Azure Monitor Alert created successfully.")
