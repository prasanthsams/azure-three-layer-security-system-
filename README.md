🌐 Three-Layer Security System for Database Hosting on Cloud (Microsoft Azure)

🔒 Overview

This project focuses on building a three-layer security system for cloud-hosted databases using Microsoft Azure.
It provides real-time protection against SQL injection, unauthorized access, and cyberattacks by using:

Azure Web Application Firewall (WAF)

Azure Monitor

Azure Notification Hub


The system ensures database security through multiple defense layers and continuous monitoring.


---

⚙️ Project Architecture

Layers:

1. Presentation Layer (User Interface) — Web dashboard for login and monitoring.


2. Business Logic Layer (Service Layer) — Handles authentication, validation, and security logic.


3. Data Layer (Persistence Layer) — Azure SQL Database and Blob Storage.


4. Security Layers: WAF + Firewall + Azure Monitor for alerting and traffic inspection.




---

🧩 Prerequisites

Before setting up, make sure you have the following installed:

🖥️ System Requirements

OS: Windows 10 / 11

RAM: 8 GB or above

Disk Space: 10 GB free

Internet Connection: Stable


🔧 Software Requirements

Visual Studio Code

Python 3.9+

Azure CLI

Git

PIP

A valid Microsoft Azure account with an active subscription.



---

🧱 Installation & Setup

Step 1 – Clone the Repository

git clone https://github.com/<your-username>/three-layer-azure-security.git
cd three-layer-azure-security

Step 2 – Install Dependencies

pip install -r requirements.txt

Step 3 – Login to Azure

az login

> This will open a browser window for your Microsoft account login.
After login, Azure CLI will automatically link to your active subscription.



Step 4 – Set Your Azure Subscription

To ensure you’re working with the right subscription:

az account list --output table
az account set --subscription "<your-subscription-id>"

> Replace <your-subscription-id> with the actual subscription identifier from your Azure account.



Step 5 – Deploy the Resources

Run your deployment script (for example deploy.py):

python deploy.py

This will:

Create the Resource Group

Configure WAF policies

Set up Azure Monitor alerts

Link to your Azure SQL Database



---

🔑 Configuration Files

File	Description

deploy.py	Main deployment script for Azure services
.env	Environment variables (Azure credentials, DB connection)
requirements.txt	Python dependencies
config.json	Configuration for security policies and resource group
README.md	Project documentation



---

📊 Usage

After deployment, open your local app or hosted dashboard to monitor:

Real-time security logs

Threat detection alerts

WAF activity insights

Database health status



---

🧠 Example Azure Subscription Info

Parameter	Example Value

Subscription Name	Azure for Students
Subscription ID	b2e9e440-2b5d-4a4b-8b35-d8a48ac84f47
Resource Group	SecureDB-Group
Location	East US



---

📈 Future Enhancements

Integration with Azure Sentinel for advanced threat detection

Add Machine Learning-based anomaly detection

Support for multi-tenant architecture



---

👨‍💻 Author

[Your Name]
Final Year Student | Department of Computer Science
📧 [your.email@example.com]
💻 GitHub – your-username
