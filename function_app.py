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

app = FunctionApp()

@app.route(route="health", methods=["GET"])
def health_check(req: HttpRequest) -> HttpResponse:
    """Simple health check endpoint."""
    return HttpResponse(
        json.dumps({
            "status": "healthy",
            "message": "Function app is running"
        }),
        status_code=200,
        mimetype="application/json"
    )

def get_search_client():
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    if not (endpoint and api_key and index_name):
        raise ValueError("Missing Azure Search environment variables.")
    return SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(api_key)
    )

@app.route(route="search-workflow", methods=["POST"])
def search_workflow(req: HttpRequest) -> HttpResponse:
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
    try:
        data = req.get_json()
        table_name = data.get("table_name")
        if not table_name:
            return HttpResponse(json.dumps({"error": "Missing 'table_name' in request."}), status_code=400)
        client = get_search_client()
        results = client.search(search_text=table_name, filter="type eq 'table'")
        tables = [doc for doc in results]
        return HttpResponse(json.dumps({"tables": tables}, default=str), mimetype="application/json")
    except Exception as e:
        logging.exception("Error in debug-table")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="get-workflow-details", methods=["POST"])
def get_workflow_details(req: HttpRequest) -> HttpResponse:
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
        # Get blob storage configuration
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_CONTAINER_NAME", "xml-metadata")
        
        if not connection_string:
            return HttpResponse(json.dumps({"error": "AZURE_STORAGE_CONNECTION_STRING not configured"}), status_code=500)
        
        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        # List blobs
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
        # Get search configuration
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "informatica-workflows")
        
        if not search_endpoint or not search_key:
            return HttpResponse(json.dumps({"error": "Azure Search credentials not configured"}), status_code=500)
        
        # Create search index client
        client = SearchIndexClient(
            endpoint=search_endpoint,
            credential=AzureKeyCredential(search_key)
        )
        
        # Define the index schema
        index = SearchIndex(
            name=index_name,
            fields=[
                SimpleField(name="id", type="Edm.String", key=True),
                SearchableField(name="workflow_name", type="Edm.String", filterable=True, sortable=True),
                SearchableField(name="source_tables", type="Collection(Edm.String)"),
                SearchableField(name="target_tables", type="Collection(Edm.String)"),
                SearchableField(name="transformations", type="Collection(Edm.String)"),
                SearchableField(name="mapping_name", type="Edm.String", filterable=True),
                SearchableField(name="session_name", type="Edm.String", filterable=True),
                SearchableField(name="xml_file", type="Edm.String", filterable=True),
                SearchableField(name="full_content", type="Edm.String", searchable=True),
                SearchableField(name="metadata", type="Edm.String")
            ]
        )
        
        # Create the index
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
        # Get configuration
        blob_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_CONTAINER_NAME", "xml-metadata")
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "informatica-workflows")
        
        if not all([blob_connection_string, search_endpoint, search_key]):
            return HttpResponse(json.dumps({"error": "Missing required configuration"}), status_code=500)
        
        # Get blob service client
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        # Get search client
        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key)
        )
        
        # List XML files
        blobs = list(container_client.list_blobs())
        xml_files = [blob for blob in blobs if blob.name.lower().endswith('.xml')]
        
        if not xml_files:
            return HttpResponse(json.dumps({"error": "No XML files found in container"}), status_code=404)
        
        all_workflows = []
        processed_files = 0
        
        # Process each XML file
        for blob in xml_files:
            try:
                # Download XML content
                blob_client = container_client.get_blob_client(blob.name)
                xml_content = blob_client.download_blob().readall().decode('utf-8')
                
                # Parse XML and extract workflows
                workflows = extract_workflows_from_xml(xml_content, blob.name)
                all_workflows.extend(workflows)
                processed_files += 1
                
                logging.info(f"Processed {blob.name}: {len(workflows)} workflows")
                
            except Exception as e:
                logging.error(f"Error processing {blob.name}: {str(e)}")
                continue
        
        if not all_workflows:
            return HttpResponse(json.dumps({"error": "No workflows extracted from XML files"}), status_code=500)
        
        # Upload to search index in batches
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
        
        # Find all workflow elements
        for workflow in root.findall('.//WORKFLOW'):
            workflow_name = workflow.get('NAME', 'Unknown')
            mapping_name = workflow.get('MAPPINGNAME', 'Unknown')
            session_name = workflow.get('SESSIONNAME', 'Unknown')
            
            # Extract source tables
            source_tables = []
            for source in workflow.findall('.//SOURCE'):
                table_name = source.get('NAME', '')
                if table_name:
                    source_tables.append(table_name)
            
            # Extract target tables
            target_tables = []
            for target in workflow.findall('.//TARGET'):
                table_name = target.get('NAME', '')
                if table_name:
                    target_tables.append(table_name)
            
            # Extract transformations
            transformations = []
            for transform in workflow.findall('.//TRANSFORMATION'):
                transform_name = transform.get('NAME', '')
                transform_type = transform.get('TYPE', '')
                if transform_name and transform_type:
                    transformations.append(f"{transform_name} ({transform_type})")
            
            # Create workflow document - map to existing index fields
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

@app.route(route="debug-upload", methods=["POST"])
def debug_upload_issues(req: HttpRequest) -> HttpResponse:
    """Debug upload issues by testing with a single workflow document."""
    try:
        # Get configuration
        blob_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("BLOB_CONTAINER_NAME", "xml-metadata")
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "informatica-workflows")
        
        if not all([blob_connection_string, search_endpoint, search_key]):
            return HttpResponse(json.dumps({"error": "Missing required configuration"}), status_code=500)
        
        # Get blob service client
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        # Get search client
        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key)
        )
        
        # Get the first XML file
        blobs = list(container_client.list_blobs())
        xml_files = [blob for blob in blobs if blob.name.lower().endswith('.xml')]
        
        if not xml_files:
            return HttpResponse(json.dumps({"error": "No XML files found"}), status_code=404)
        
        # Process first XML file
        blob = xml_files[0]
        blob_client = container_client.get_blob_client(blob.name)
        xml_content = blob_client.download_blob().readall().decode('utf-8')
        
        # Extract workflows
        workflows = extract_workflows_from_xml(xml_content, blob.name)
        
        if not workflows:
            return HttpResponse(json.dumps({"error": "No workflows extracted"}), status_code=500)
        
        # Take first workflow and clean it
        test_workflow = workflows[0]
        
        # Use the workflow document as-is since extract_workflows_from_xml already maps to correct fields
        cleaned_workflow = {
            "id": test_workflow["id"][:100],  # Limit ID length
            "name": test_workflow["name"][:100] if test_workflow["name"] else "Unknown",
            "type": test_workflow["type"],
            "description": test_workflow["description"][:1000] if len(test_workflow["description"]) > 1000 else test_workflow["description"]
        }
        
        # Try to upload single document
        try:
            result = search_client.upload_documents([cleaned_workflow])
            upload_result = result[0]
            
            if upload_result.succeeded:
                response = {
                    "status": "success",
                    "message": "Single workflow uploaded successfully",
                    "workflow_id": cleaned_workflow["id"],
                    "workflow_name": cleaned_workflow["name"],
                    "workflow_type": cleaned_workflow["type"],
                    "description_length": len(cleaned_workflow["description"])
                }
            else:
                response = {
                    "status": "failed",
                    "error": str(upload_result.error),
                    "workflow_id": cleaned_workflow["id"],
                    "debug_info": {
                        "id_length": len(cleaned_workflow["id"]),
                        "name_length": len(cleaned_workflow["name"]),
                        "type": cleaned_workflow["type"],
                        "description_length": len(cleaned_workflow["description"])
                    }
                }
            
            return HttpResponse(json.dumps(response, indent=2), mimetype="application/json")
            
        except Exception as upload_error:
            response = {
                "status": "failed",
                "error": str(upload_error),
                "workflow_id": cleaned_workflow["id"],
                "debug_info": {
                    "id_length": len(cleaned_workflow["id"]),
                    "name_length": len(cleaned_workflow["name"]),
                    "type": cleaned_workflow["type"],
                    "description_length": len(cleaned_workflow["description"])
                }
            }
            
            return HttpResponse(json.dumps(response, indent=2), mimetype="application/json")
        
    except Exception as e:
        logging.exception("Error in debug-upload")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)

@app.route(route="check-index", methods=["GET"])
def check_index_schema(req: HttpRequest) -> HttpResponse:
    """Check the schema of the existing Azure AI Search index."""
    try:
        # Get search configuration
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        search_key = os.getenv("AZURE_SEARCH_API_KEY")
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "informatica-workflows")
        
        if not search_endpoint or not search_key:
            return HttpResponse(json.dumps({"error": "Azure Search credentials not configured"}), status_code=500)
        
        # Create search index client
        index_client = SearchIndexClient(
            endpoint=search_endpoint,
            credential=AzureKeyCredential(search_key)
        )
        
        # Get the index
        index = index_client.get_index(index_name)
        
        # Extract field information
        fields_info = []
        for field in index.fields:
            field_info = {
                "name": field.name,
                "type": str(field.type),
                "is_key": field.key,
                "is_searchable": field.searchable,
                "is_filterable": field.filterable,
                "is_sortable": field.sortable
            }
            fields_info.append(field_info)
        
        result = {
            "index_name": index_name,
            "total_fields": len(fields_info),
            "fields": fields_info
        }
        
        return HttpResponse(json.dumps(result, indent=2), mimetype="application/json")
        
    except Exception as e:
        logging.exception("Error in check-index")
        return HttpResponse(json.dumps({"error": str(e)}), status_code=500)