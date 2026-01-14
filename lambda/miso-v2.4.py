import json
import boto3

client = boto3.client("bedrock-agent-runtime")

KB_ID = "KB_ID"
MODEL_ARN = (
    "x:"
    "y"
)

def lambda_handler(event, context):
    try:
        # Log once for observability
        print("EVENT:", json.dumps(event))

        # --- Parse body safely ---
        body = event.get("body", {})
        if isinstance(body, str) and body.strip():
            body = json.loads(body)
        elif not isinstance(body, dict):
            body = {}

        query = body.get("query", "").strip()

        if not query:
            return _response(
                400,
                {"error": "Query missing"}
            )

        # --- Bedrock Knowledge Base call ---
        bedrock_response = client.retrieve_and_generate(
            input={"text": query},
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": KB_ID,
                    "modelArn": MODEL_ARN
                }
            }
        )

        answer = (
            bedrock_response
            .get("output", {})
            .get("text", "")
        )

        if not answer:
            answer = "No relevant information found."

        return _response(
            200,
            {"answer": answer}
        )

    except Exception as e:
        print("ERROR:", str(e))
        return _response(
            500,
            {"error": "Internal server error"}
        )

def _response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body_dict)
    }

