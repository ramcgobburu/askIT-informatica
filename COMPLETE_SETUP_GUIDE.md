# Complete Informatica Agent Setup Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Azure Function App Setup](#azure-function-app-setup)
4. [Azure AI Search Setup](#azure-ai-search-setup)
5. [Blob Storage Setup](#blob-storage-setup)
6. [Function Code Implementation](#function-code-implementation)
7. [Environment Variables Configuration](#environment-variables-configuration)
8. [XML Processing and Upload](#xml-processing-and-upload)
9. [Power Apps Custom Connector](#power-apps-custom-connector)
10. [Copilot Studio Integration](#copilot-studio-integration)
11. [Testing and Validation](#testing-and-validation)
12. [Troubleshooting](#troubleshooting)

## Overview

This guide walks you through creating a complete Informatica workflow analysis agent using Azure services. The agent can:
- Search for workflow details by name
- Debug table loading issues
- Retrieve comprehensive workflow information
- Process XML metadata files from Informatica PowerCenter

## Prerequisites

- Azure subscription with appropriate permissions
- Access to Copilot Studio (Microsoft 365 license)
- XML metadata files from Informatica PowerCenter
- Basic understanding of Azure services

## Azure Function App Setup

### Step 1: Create Function App

1. **Navigate to Azure Portal**
   - Go to [portal.azure.com](https://portal.azure.com)
   - Sign in with your Azure account

2. **Create Function App**
   - Click "Create a resource"
   - Search for "Function App"
   - Click "Create"

3. **Configure Function App Settings**
   ```
   Subscription: [Your subscription]
   Resource Group: [Create new or use existing]
   Function App name: askit-informatica-[unique-suffix]
   Runtime stack: Python
   Version: 3.11
   Region: [Choose allowed region - e.g., Canada Central]
   Operating System: Linux
   Plan type: Consumption (Serverless)
   ```

4. **Create the Function App**
   - Click "Review + create"
   - Click "Create"
   - Wait for deployment to complete

### Step 2: Configure Function App

1. **Go to Function App**
   - Navigate to your created Function App
   - Click on "Configuration" in the left menu

2. **Add Application Settings**
   ```
   AZURE_SEARCH_ENDPOINT: [Will be added later]
   AZURE_SEARCH_API_KEY: [Will be added later]
   AZURE_SEARCH_INDEX_NAME: informatica-workflows
   AZURE_STORAGE_CONNECTION_STRING: [Will be added later]
   BLOB_CONTAINER_NAME: xml-metadata
   ```

## Azure AI Search Setup

### Step 1: Create Azure AI Search Service

1. **Create Search Service**
   - Go to Azure Portal
   - Click "Create a resource"
   - Search for "Azure AI Search"
   - Click "Create"

2. **Configure Search Service**
   ```
   Subscription: [Your subscription]
   Resource Group: [Same as Function App]
   Service name: informatica-search-services
   Location: [Same region as Function App]
   Pricing tier: Free (for development) or Basic
   ```

3. **Create the Service**
   - Click "Review + create"
   - Click "Create"
   - Wait for deployment to complete

### Step 2: Get Search Service Credentials

1. **Navigate to Search Service**
   - Go to your created Azure AI Search service
   - Click on "Keys" in the left menu

2. **Copy Credentials**
   - Copy the "URL" (this is your AZURE_SEARCH_ENDPOINT)
   - Copy either "Primary admin key" or "Secondary admin key" (this is your AZURE_SEARCH_API_KEY)

3. **Update Function App Configuration**
   - Go back to your Function App
   - Navigate to "Configuration" > "Application settings"
   - Update the values:
     ```
     AZURE_SEARCH_ENDPOINT: [Your search service URL]
     AZURE_SEARCH_API_KEY: [Your admin key]
     ```

## Blob Storage Setup

### Step 1: Create Storage Account

1. **Create Storage Account**
   - Go to Azure Portal
   - Click "Create a resource"
   - Search for "Storage account"
   - Click "Create"

2. **Configure Storage Account**
   ```
   Subscription: [Your subscription]
   Resource Group: [Same as Function App]
   Storage account name: [unique-name]-storage
   Location: [Same region as Function App]
   Performance: Standard
   Redundancy: LRS (Locally-redundant storage)
   ```

3. **Create the Storage Account**
   - Click "Review + create"
   - Click "Create"
   - Wait for deployment to complete

### Step 2: Create Container and Upload XML Files

1. **Create Container**
   - Navigate to your Storage Account
   - Click on "Containers" in the left menu
   - Click "+ Container"
   - Name: `xml-metadata`
   - Public access level: Private

2. **Upload XML Files**
   - Click on the `xml-metadata` container
   - Click "Upload"
   - Select your Informatica XML files (set1.XML, set2.XML, set3.XML, etc.)
   - Click "Upload"

3. **Get Connection String**
   - Go to "Access keys" in the left menu
   - Copy the "Connection string" (either key1 or key2)

4. **Update Function App Configuration**
   - Go back to your Function App
   - Navigate to "Configuration" > "Application settings"
   - Update:
     ```
     AZURE_STORAGE_CONNECTION_STRING: [Your connection string]
     ```

## Function Code Implementation

### Step 1: Create Function App Code

Create a file called `function_app.py` with the following content:

```python
import os
import json
import logging
import xml.etree.ElementTree as ET
from azure.functions import HttpRequest, HttpResponse, FunctionApp
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField

# Initialize Azure Functions app
app = FunctionApp()

# Environment variables
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

def get_search_client():
    """Initialize and return Azure Search client."""
    if not all([AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY, AZURE_SEARCH_INDEX_NAME]):
        raise ValueError("Missing Azure Search environment variables. Please check AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY, and AZURE_SEARCH_INDEX_NAME.")
    
    return SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_API_KEY)
    )

@app.route(route="health", methods=["GET"])
def health_check(req: HttpRequest) -> HttpResponse:
    """Simple health check endpoint."""
    return HttpResponse(
        json.dumps({
            "status": "healthy",
            "message": "Function app is running",
            "timestamp": "2025-01-03T00:00:00Z"
        }),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="search-workflow", methods=["POST"])
def search_workflow(req: HttpRequest) -> HttpResponse:
    """Search for workflows by name."""
    try:
        data = req.get_json()
        workflow_name = data.get("workflow_name")
        if not workflow_name:
            return HttpResponse(json.dumps({"error": "Missing 'workflow_name' in request."}), status_code=400)
        
        client = get_search_client()
        results = client.search(search_text=workflow_name)
        workflows = [doc for doc in results]
        return HttpResponse(json.dumps({"workflows": workflows}, default=str), mimetype="application/json")
    except Exception as e:
        logging.exception("Error in search-workflow")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="debug-table", methods=["POST"])
def debug_table(req: HttpRequest) -> HttpResponse:
    """Debug table loading issues by searching for workflows that use the table."""
    try:
        data = req.get_json()
        table_name = data.get("table_name")
        if not table_name:
            return HttpResponse(json.dumps({"error": "Missing 'table_name' in request."}), status_code=400)
        
        client = get_search_client()
        results = client.search(search_text=table_name)
        tables = [doc for doc in results]
        return HttpResponse(json.dumps({"tables": tables}, default=str), mimetype="application/json")
    except Exception as e:
        logging.exception("Error in debug-table")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="get-workflow-details", methods=["POST"])
def get_workflow_details(req: HttpRequest) -> HttpResponse:
    """Get detailed information about a specific workflow."""
    try:
        data = req.get_json()
        workflow_id = data.get("workflow_id")
        if not workflow_id:
            return HttpResponse(json.dumps({"error": "Missing 'workflow_id' in request."}), status_code=400)
        
        client = get_search_client()
        results = client.search(search_text=workflow_id, filter=f"id eq '{workflow_id}'")
        details = [doc for doc in results]
        return HttpResponse(json.dumps({"workflow_details": details}, default=str), mimetype="application/json")
    except Exception as e:
        logging.exception("Error in get-workflow-details")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="test-blob", methods=["GET"])
def test_blob_storage(req: HttpRequest) -> HttpResponse:
    """Test blob storage connection and list XML files."""
    try:
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_CONTAINER_NAME", "xml-metadata")
        
        if not connection_string:
            return HttpResponse(json.dumps({"error": "AZURE_STORAGE_CONNECTION_STRING not configured"}), status_code=500)
        
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        blobs = list(container_client.list_blobs())
        
        result = {
            "container_name": container_name,
            "total_files": len(blobs),
            "xml_files": []
        }
        
        for blob in blobs:
            blob_info = {
                "name": blob.name,
                "size": blob.size,
                "last_modified": blob.last_modified.isoformat() if blob.last_modified else None
            }
            
            if blob.name.lower().endswith('.xml'):
                blob_info["type"] = "XML"
                result["xml_files"].append(blob_info)
            else:
                blob_info["type"] = "Other"
        
        return HttpResponse(json.dumps(result, indent=2), mimetype="application/json")
        
    except Exception as e:
        logging.exception("Error in test-blob")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="create-index", methods=["POST"])
def create_search_index(req: HttpRequest) -> HttpResponse:
    """Create Azure AI Search index for workflow metadata."""
    try:
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "informatica-workflows")
        
        if not search_endpoint or not search_key:
            return HttpResponse(json.dumps({"error": "Azure Search credentials not configured"}), status_code=500)
        
        client = SearchIndexClient(
            endpoint=search_endpoint,
            credential=AzureKeyCredential(search_key)
        )
        
        index = SearchIndex(
            name=index_name,
            fields=[
                SimpleField(name="id", type="Edm.String", key=True),
                SearchableField(name="name", type="Edm.String", filterable=True, sortable=True),
                SearchableField(name="type", type="Edm.String", filterable=True),
                SearchableField(name="description", type="Edm.String", searchable=True)
            ]
        )
        
        client.create_index(index)
        
        result = {
            "status": "success",
            "message": f"Search index '{index_name}' created successfully",
            "index_name": index_name,
            "endpoint": search_endpoint
        }
        
        return HttpResponse(json.dumps(result, indent=2), mimetype="application/json")
        
    except Exception as e:
        logging.exception("Error in create-index")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="process-xml", methods=["POST"])
def process_xml_files(req: HttpRequest) -> HttpResponse:
    """Process XML files from blob storage and upload to Azure AI Search."""
    try:
        blob_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_CONTAINER_NAME", "xml-metadata")
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "informatica-workflows")
        
        if not all([blob_connection_string, search_endpoint, search_key]):
            return HttpResponse(json.dumps({"error": "Missing required configuration"}), status_code=500)
        
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key)
        )
        
        blobs = list(container_client.list_blobs())
        xml_files = [blob for blob in blobs if blob.name.lower().endswith('.xml')]
        
        if not xml_files:
            return HttpResponse(json.dumps({"error": "No XML files found in container"}), status_code=404)
        
        all_workflows = []
        processed_files = 0
        
        for blob in xml_files:
            try:
                blob_client = container_client.get_blob_client(blob.name)
                xml_content = blob_client.download_blob().readall().decode('utf-8')
                
                workflows = extract_workflows_from_xml(xml_content, blob.name)
                all_workflows.extend(workflows)
                processed_files += 1
                
                logging.info(f"Processed {blob.name}: {len(workflows)} workflows")
                
            except Exception as e:
                logging.error(f"Error processing {blob.name}: {str(e)}")
                continue
        
        if not all_workflows:
            return HttpResponse(json.dumps({"error": "No workflows extracted from XML files"}), status_code=500)
        
        batch_size = 10
        uploaded_count = 0
        
        for i in range(0, len(all_workflows), batch_size):
            batch = all_workflows[i:i + batch_size]
            try:
                result = search_client.upload_documents(batch)
                successful = sum(1 for r in result if r.succeeded)
                uploaded_count += successful
            except Exception as e:
                logging.error(f"Error uploading batch {i//batch_size + 1}: {str(e)}")
        
        result = {
            "status": "success",
            "message": "XML processing completed",
            "xml_files_processed": processed_files,
            "workflows_extracted": len(all_workflows),
            "workflows_uploaded": uploaded_count,
            "index_name": index_name
        }
        
        return HttpResponse(json.dumps(result, indent=2), mimetype="application/json")
        
    except Exception as e:
        logging.exception("Error in process-xml")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

def extract_workflows_from_xml(xml_content, xml_filename):
    """Extract workflow information from XML content."""
    try:
        root = ET.fromstring(xml_content)
        workflows = []
        
        for workflow in root.findall('.//WORKFLOW'):
            workflow_name = workflow.get('NAME', 'Unknown')
            mapping_name = workflow.get('MAPPINGNAME', 'Unknown')
            session_name = workflow.get('SESSIONNAME', 'Unknown')
            
            source_tables = []
            for source in workflow.findall('.//SOURCE'):
                table_name = source.get('NAME', '')
                if table_name:
                    source_tables.append(table_name)
            
            target_tables = []
            for target in workflow.findall('.//TARGET'):
                table_name = target.get('NAME', '')
                if table_name:
                    target_tables.append(table_name)
            
            transformations = []
            for transform in workflow.findall('.//TRANSFORMATION'):
                transform_name = transform.get('NAME', '')
                transform_type = transform.get('TYPE', '')
                if transform_name and transform_type:
                    transformations.append(f"{transform_name} ({transform_type})")
            
            workflow_doc = {
                "id": f"{xml_filename}_{workflow_name}_{mapping_name}".replace(" ", "_").replace(".", "_")[:100],
                "name": workflow_name[:100] if workflow_name else "Unknown",
                "type": "workflow",
                "description": f"Mapping: {mapping_name}, Session: {session_name}, XML: {xml_filename}, Sources: {len(source_tables)}, Targets: {len(target_tables)}, Transformations: {len(transformations)}"
            }
            
            workflows.append(workflow_doc)
        
        return workflows
        
    except ET.ParseError as e:
        logging.error(f"XML parsing error in {xml_filename}: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Error processing {xml_filename}: {str(e)}")
        return []
```

### Step 2: Create Requirements File

Create a file called `requirements.txt`:

```txt
# Azure Functions Python dependencies
azure-functions>=1.0.0

# Azure Search dependencies
azure-search-documents>=11.0.0
azure-core>=1.0.0

# XML processing for Informatica metadata
lxml>=4.9.0

# HTTP requests
requests>=2.28.0

# Azure Storage for blob operations
azure-storage-blob>=12.0.0

# Environment variable management
python-dotenv>=0.19.0

# Additional utilities
urllib3>=1.26.0
```

### Step 3: Deploy Function Code

1. **Deploy via Azure Portal**
   - Go to your Function App
   - Click "Deployment Center"
   - Choose "Local Git" or "OneDrive" or "GitHub"
   - Follow the deployment instructions

2. **Alternative: Deploy via VS Code**
   - Install Azure Functions extension in VS Code
   - Open your function folder
   - Use Command Palette: "Azure Functions: Deploy to Function App"

## Environment Variables Configuration

### Complete Environment Variables List

Add these to your Function App Configuration:

```bash
# Azure AI Search Configuration
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-admin-key-here
AZURE_SEARCH_INDEX_NAME=informatica-workflows

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your-storage;AccountKey=your-key;EndpointSuffix=core.windows.net
BLOB_CONTAINER_NAME=xml-metadata

# Azure Functions Configuration
AzureWebJobsStorage=DefaultEndpointsProtocol=https;AccountName=your-storage;AccountKey=your-key;EndpointSuffix=core.windows.net
FUNCTIONS_WORKER_RUNTIME=python
```

## XML Processing and Upload

### Step 1: Create Search Index

1. **Test the create-index function**
   - Go to Azure Portal > Function App > Functions
   - Click on "create-index" function
   - Click "Test/Run"
   - Click "Run" (POST request, empty body)

### Step 2: Process XML Files

1. **Test blob storage connection**
   - Go to "test-blob" function
   - Click "Test/Run"
   - Click "Run" (GET request)
   - Verify your XML files are listed

2. **Process XML files**
   - Go to "process-xml" function
   - Click "Test/Run"
   - Click "Run" (POST request, empty body)
   - This will extract and upload all workflows to Azure AI Search

### Step 3: Verify Upload

1. **Test search functionality**
   - Go to "search-workflow" function
   - Click "Test/Run"
   - Use this JSON body:
   ```json
   {
     "workflow_name": "your-workflow-name"
   }
   ```

## Power Apps Custom Connector

### Step 1: Create Custom Connector

1. **Navigate to Power Apps**
   - Go to [make.powerapps.com](https://make.powerapps.com)
   - Sign in with your Microsoft account

2. **Create Custom Connector**
   - Click "Data" > "Custom connectors"
   - Click "New custom connector"
   - Choose "Create from blank"

### Step 2: Configure General Information

```
Connector name: SearchWorkflowDetails
Description: Searches and retrieves Informatica workflow details by workflow name from Azure Functions
Scheme: HTTPS
Host: your-function-app-name.azurewebsites.net
Base URL: /
```

### Step 3: Configure Security

- **Authentication:** No authentication
- Leave other settings as default

### Step 4: Configure Definition

```
Summary: Search Workflow Details
Description: Searches for Informatica workflow details by workflow name. Returns workflow information including mapping name, session name, source tables, target tables, and transformations from Azure AI Search.
Operation ID: SearchWorkflow
Method: POST
URL: /api/search-workflow
```

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "workflow_name": "{{workflow_name}}"
}
```

**Parameters:**
- `workflow_name` (Text, Required): The name of the Informatica workflow to search for

**Response Schema:**
```json
{
  "workflows": [
    {
      "id": "string",
      "name": "string",
      "type": "string",
      "description": "string",
      "@search.score": "number",
      "@search.reranker_score": "null",
      "@search.highlights": "null",
      "@search.captions": "null"
    }
  ]
}
```

### Step 5: Test the Connector

1. **Go to Test tab**
2. **Create new connection**
3. **Configure test:**
   - Content-Type: `application/json`
   - Raw Body: ON
   - JSON Body:
   ```json
   {
     "workflow_name": "your-test-workflow-name"
   }
   ```
4. **Click "Test operation"**

## Copilot Studio Integration

### Step 1: Create Copilot Studio Agent

1. **Navigate to Copilot Studio**
   - Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)
   - Sign in with your Microsoft account

2. **Create New Agent**
   - Click "Create" > "New copilot"
   - Name: `AskIt-Informatica-Agent`
   - Description: `AI agent for Informatica workflow analysis and debugging`

### Step 2: Add Custom Connector as Tool

1. **Navigate to Tools**
   - In your Copilot Studio agent, click "Tools"
   - Click "+ Add a tool"

2. **Add Custom Connector**
   - Select "Connector"
   - Choose your "SearchWorkflowDetails" connector
   - Select "SearchWorkflow" action

3. **Configure Tool**
   - Tool Name: `Search Workflow Details`
   - Description: `Searches for Informatica workflow details by workflow name`
   - Input Parameter: `workflow_name` (filled dynamically by AI)

### Step 3: Create Topics (Optional)

1. **Create Topics for Common Queries**
   - Go to "Topics" in Copilot Studio
   - Create topics for:
     - "Search Workflow"
     - "Debug Table Issues"
     - "Get Workflow Details"

2. **Configure Topic Actions**
   - Add actions to call your custom connector
   - Configure input parameters
   - Set up response handling

### Step 4: Test the Agent

1. **Use Test Panel**
   - Click "Test" in Copilot Studio
   - Try these test prompts:
   ```
   "What are the details of workflow [workflow-name]?"
   "Search for workflow [workflow-name]"
   "Tell me about workflow [workflow-name]"
   "Debug table [table-name] loading issues"
   ```

## Testing and Validation

### Function Testing Checklist

- [ ] Health check endpoint returns 200 OK
- [ ] Blob storage connection lists XML files
- [ ] Search index creation succeeds
- [ ] XML processing extracts workflows
- [ ] Workflow upload to search index succeeds
- [ ] Search workflow returns correct results
- [ ] Debug table returns relevant workflows
- [ ] Get workflow details returns specific workflow

### Custom Connector Testing Checklist

- [ ] Connector creation completes successfully
- [ ] Test operation returns expected JSON response
- [ ] Connection can be established
- [ ] Parameters are correctly mapped

### Copilot Studio Testing Checklist

- [ ] Agent can be created and published
- [ ] Custom connector tool is available
- [ ] Agent can extract workflow names from user queries
- [ ] Agent returns meaningful responses
- [ ] Agent handles errors gracefully

## Troubleshooting

### Common Issues and Solutions

#### 1. Function App Deployment Issues

**Problem:** Functions not appearing or deployment failing
**Solution:**
- Check Python version compatibility (use 3.11)
- Verify requirements.txt includes all dependencies
- Check function timeout settings in host.json
- Ensure proper file structure (function_app.py in root)

#### 2. Azure AI Search Connection Issues

**Problem:** Search client initialization fails
**Solution:**
- Verify AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_API_KEY are set
- Check if search service is in the same region
- Verify API key has admin permissions
- Test search service connectivity from Azure Portal

#### 3. Blob Storage Access Issues

**Problem:** Cannot access XML files from blob storage
**Solution:**
- Verify AZURE_STORAGE_CONNECTION_STRING is correct
- Check container name matches BLOB_CONTAINER_NAME
- Ensure XML files are uploaded to correct container
- Verify storage account access permissions

#### 4. XML Processing Issues

**Problem:** No workflows extracted from XML files
**Solution:**
- Check XML file format and structure
- Verify XML files are valid and not corrupted
- Check for XML namespace issues
- Review XML parsing logic for specific PowerCenter format

#### 5. Custom Connector Issues

**Problem:** Connector test fails or returns errors
**Solution:**
- Verify Function App URL is accessible
- Check CORS settings in Function App
- Ensure function key is included if required
- Test function directly in Azure Portal first

#### 6. Copilot Studio Integration Issues

**Problem:** Agent cannot call custom connector
**Solution:**
- Verify connector is properly configured
- Check parameter mapping in Copilot Studio
- Ensure agent has access to the connector
- Test connector independently in Power Apps

### Debugging Steps

1. **Check Function Logs**
   - Go to Function App > Monitor > Logs
   - Look for error messages and exceptions
   - Check application insights for detailed traces

2. **Test Each Component Independently**
   - Test Azure Functions individually
   - Test Azure AI Search directly
   - Test Blob Storage access
   - Test Custom Connector in isolation

3. **Verify Environment Variables**
   - Double-check all environment variables are set
   - Ensure no typos in variable names or values
   - Test with sample data

4. **Check Network Connectivity**
   - Verify all Azure services are accessible
   - Check firewall and network security group settings
   - Test from different networks if needed

## Security Considerations

### Best Practices

1. **API Key Management**
   - Use Azure Key Vault for sensitive credentials
   - Rotate API keys regularly
   - Use least privilege access

2. **Network Security**
   - Configure proper CORS settings
   - Use Azure Private Endpoints for sensitive data
   - Implement IP restrictions where appropriate

3. **Data Protection**
   - Encrypt data at rest and in transit
   - Implement proper access controls
   - Regular security audits and monitoring

## Cost Optimization

### Azure Services Cost Management

1. **Function App**
   - Use Consumption plan for development
   - Monitor execution time and memory usage
   - Implement proper error handling to avoid unnecessary executions

2. **Azure AI Search**
   - Use Free tier for development (up to 50MB, 3 indexes)
   - Monitor query volume and storage usage
   - Optimize index size and query performance

3. **Blob Storage**
   - Use appropriate storage tier (Hot, Cool, Archive)
   - Implement lifecycle management policies
   - Monitor storage usage and costs

## Monitoring and Maintenance

### Setup Monitoring

1. **Application Insights**
   - Enable Application Insights for Function App
   - Set up custom metrics and alerts
   - Monitor performance and errors

2. **Azure Monitor**
   - Configure log analytics workspace
   - Set up dashboards for key metrics
   - Implement automated alerting

### Regular Maintenance

1. **Data Updates**
   - Schedule regular XML file processing
   - Update search index with new workflows
   - Archive old or obsolete workflows

2. **Performance Optimization**
   - Monitor and optimize search queries
   - Review and update function code
   - Scale resources as needed

3. **Security Updates**
   - Keep Azure services updated
   - Review and rotate credentials
   - Audit access logs regularly

## Conclusion

This guide provides a complete end-to-end setup for creating an Informatica workflow analysis agent using Azure services and Copilot Studio. The solution addresses the original problem of "RAG bleed" by implementing a structured search approach with Azure AI Search instead of relying on generic vector databases.

The agent can now:
- Accurately search for workflow details
- Debug table loading issues
- Provide specific workflow information
- Process XML metadata files from Informatica PowerCenter

For additional support or questions, refer to the Azure documentation and Copilot Studio help resources.
