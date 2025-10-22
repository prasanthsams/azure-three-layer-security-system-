from azure.identity import InteractiveBrowserCredential
from azure.mgmt.resource import ResourceManagementClient

tenant_id = "b9d4939e-7121-4471-a669-b0083b9c9749"
subscription_id = "6849b10f-591a-469c-b7ce-1ae37bf2e47c"

credential = InteractiveBrowserCredential(tenant_id=tenant_id)
resource_client = ResourceManagementClient(credential, subscription_id)

print("Creating resource group...")
resource_client.resource_groups.create_or_update(
    "SecurityRG",
    {"location": "eastus"}
)
print("✅ Resource group created successfully")