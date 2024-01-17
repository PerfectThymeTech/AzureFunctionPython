# Azure Function Baseline for Python

This repository provides a scalable baseline for Azure Functions written in Python. It demonstrates:

1. A compliant infrastructure baseline written in Terraform,
2. A Python code baseline that follows best practices and
3. A safe rollout mechanism of code artifacts.

## Infrastructure

The infrastructure as code (IaC) is written in Terraform and uses all the latest and greatest Azure Function features to ensure high security standards and the lowest attack surface possible. The code can be found in the [`/code/infra` folder](/code/infra/) and creates the following resources:

* App Service Plan,
* Azure Function,
* Azure Storage Account,
* Azure Key Vault,
* Azure Application Insights and
* Azure Log Analytics Workspace.

The Azure Function is configured in a way to fulfill highest compliance standards. In addition, the end-to-end setup takes care of wiring up all services to ensure a productive experience on day one. For instance, the Azure Function is automatically being connected to Azure Application Insights and the Application Insights service is being connected to the Azure Log Analytics Workspace.

### Network configuration

The deployed services ensure a compliant network setup using the following features:

* Public network access is denied for all services.
* All deployed services rely on Azure Private Endpoints for all network flows including deployments and usage of the services.

### Authentication & Authorization

The deployed services ensure a compliant authentication & authorization setup using the following features:

* No key-based or local/basic authentication flows.
* Azure AD-only authentication.
* All authorization is controlled by Azure RBAC.
* This includes the interaction of the Azure Function with the Azure Storage Account and the Azure Key Vault.

### Encryption

The deployed services ensure a compliant encryption setup using the following features:

* Encryption at rest using 256-bit AES (FIPS 140-2).
* HTTPS traffic only.
* All traffic is encrypted using TLS 1.2.
* Note: Customer-manaed keys are not used at this point in time but can be added easily.
* Note: Cypher suites are set to default and can further be limited.

## Azure Function Code

The Azure Function code is written in Python and leverages the new [Web Framework integration](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-decorators#web-frameworks) supported by the v2 Python programming model. This allows to rely on proven frameworks such as FastAPI and Flask. The Azure Function application code can be found in the [`/code/function` folder](/code/function/).

### FastAPI

This sample uses FastAPI as a baseline which is a scalable, modern, fast and proven web framework for APIs built in Python. More details about FastAPI can be found [here](https://fastapi.tiangolo.com/).

### Open Telemetry

This sample uses Open Telemetry and the FastAPI and Azure Application Insights integration for end to end tracking of API calls using logs and metrics and dependency calls. More information about Open Telemetry can be found [here](https://opentelemetry.io/).

### Health Endpoint

This sample exposes a health endpoint that includes header validation (Header `x-ms-auth-internal-token`) to ensure that only the health check feature of the Azure Function it self is allowed to call this endpoint. When trying to reach this endpoint from outside, the request will be blocked with a 400 response.

### Testing

Testing of the Azure Functon application code. The testing is done using `pytest`. Tests are stored in the [`/tests` folder](/tests/) and should be extended for new functionality that is being implemented over time. The `pytest.ini` is used to reference the Azure Functon project for imports. This file makes sure that the respective python objects from the Azrue Function application code can be imported into the tests and validated accordingly.
