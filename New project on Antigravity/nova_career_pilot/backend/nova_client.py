import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class NovaClient:
    def __init__(self, region_name="us-east-1"):
        """
        Initialize the Bedrock runtime client.
        """
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        # Verify specific model ID for Nova 2 Lite in your region
        self.model_id = "amazon.nova-lite-v1:0" 

    def generate_response(self, prompt: str, system_prompt: str = "You are a helpful career assistant.") -> str:
        """
        Generate a response from Amazon Nova 2 Lite.
        """
        try:
            # Amazon Nova models often follow a specific payload structure.
            # Adjusting for generic Bedrock invocation or specific Nova schema.
            # This schema is a generalized placeholder for Nova/Titan-like models; 
            # Check official docs for exact 'amazon.nova' specs if different from standard.
            
            body = json.dumps({
                "inferenceConfig": {
                    "max_new_tokens": 1000
                },
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"text": prompt}
                        ]
                    }
                ],
                 "system": [{"text": system_prompt}]
            })

            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )

            response_body = json.loads(response.get("body").read())
            # Extracting content based on typical Nova response structure
            output_text = response_body.get("output", {}).get("message", {}).get("content", [])[0].get("text", "")
            return output_text

        except Exception as e:
            print(f"Error invoking Nova 2 Lite: {e}")
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Simple test
    nova = NovaClient()
    # print(nova.generate_response("Hello, Nova!"))
