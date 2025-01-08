import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import logging
import json
import os

app = func.FunctionApp()


@app.function_name(name="WebsiteCounter")
@app.route(route="count", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request to increment count.")

    CosmosDbConnectionSetting = os.environ.get("CosmosDbConnectionSetting")

    # Retrieve the 'id' from the query parameters
    doc_id = req.params.get("id")
    if not doc_id:
        return func.HttpResponse(
            "Please pass an 'id' in the query string", status_code=400
        )

    try:
        # Initialize Cosmos client
        client = CosmosClient.from_connection_string(CosmosDbConnectionSetting)
        database = client.get_database_client("website")
        container = database.get_container_client("counter")

        # Get the document with the specified id
        document = container.read_item(item=doc_id, partition_key=doc_id)

        # Increment the count
        current_count = document.get("count", 0)
        new_count = current_count + 1

        # Update the document with the new count
        document["count"] = new_count
        container.replace_item(item=document, body=document)

        # Filter non-relevant Cosmos keys
        filtered_data = {
            key: value for key, value in document.items() if not key.startswith("_")
        }

        return func.HttpResponse(
            json.dumps(filtered_data, indent=True), status_code=200
        )

    except Exception as e:
        logging.error(f"Error accessing Cosmos DB: {e}")
        return func.HttpResponse("Internal server error", status_code=500)
