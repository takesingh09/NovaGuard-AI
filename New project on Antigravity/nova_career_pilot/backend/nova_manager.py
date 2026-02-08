import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

class NovaManager:
    """
    Manages interactions with AWS Bedrock for Nova 2 Lite (Analysis) and simulates Nova Act (Agents).
    """
    def __init__(self, region_name=None):
        region = region_name or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        session = boto3.Session(region_name=region)
        creds = session.get_credentials()

        if creds is None:
            self.credentials_ok = False
            self.bedrock_runtime = None
        else:
            self.credentials_ok = True
            self.bedrock_runtime = session.client(
                service_name="bedrock-runtime",
                region_name=region
            )
        # Using Nova Lite/Micro or similar lightweight model ID. 
        # Adjust 'amazon.nova-lite-v1:0' to the exact available ID in your region/account.
        self.model_id = os.getenv("NOVA_MODEL_ID", "amazon.nova-lite-v1:0")

    def analyze_career_gap(self, resume_text: str, job_description: str) -> dict:
        """
        Analyzes the gap between the resume and the job description.
        Returns a structured dictionary with match score, gap analysis, and roadmap.
        """
        
        system_prompt = """
        You are an expert Career Mentor and Technical Recruiter. 
        Your goal is to help students bridge the gap between their current skills and a target job role.
        Analyze the provided Resume and Job Description (JD).
        
        Output MUST be valid JSON with the following structure:
        {
            "match_score": <int 0-100>,
            "missing_skills": [<list of strings>],
            "matching_skills": [<list of strings>],
            "roadmap": [
                {"day": "1-3", "topic": "<topic>", "activity": "<activity>"},
                ... (create a 15-day plan)
            ],
            "advice": "<brief mentorship advice>"
        }
        Do not include markdown formatting (like ```json) in the response, just the raw JSON string.
        """
        
        user_prompt = f"""
        RESUME:
        {resume_text[:4000]} 

        JOB DESCRIPTION:
        {job_description[:4000]}
        """

        if not self.credentials_ok:
            return {
                "error": "Missing AWS credentials. Set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY in .env or configure an AWS profile.",
                "match_score": 0,
                "missing_skills": [],
                "matching_skills": [],
                "roadmap": [],
                "advice": "Add credentials and retry."
            }

        try:
            # Bedrock 'converse' API or 'invoke_model' depending on model support.
            # Using standard invoke_model with the Nova/Titan schema.
            body = json.dumps({
                "inferenceConfig": {"max_new_tokens": 4096, "temperature": 0.7},
                "messages": [
                    {"role": "user", "content": [{"text": user_prompt}]}
                ],
                "system": [{"text": system_prompt}]
            })

            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=body
            )

            response_body = json.loads(response.get("body").read())
            # Handling Nova response structure
            output_content = response_body.get("output", {}).get("message", {}).get("content", [])[0].get("text", "")
            
            # Clean formatting if key exists
            if output_content.startswith("```json"):
                output_content = output_content[7:]
            if output_content.endswith("```"):
                output_content = output_content[:-3]
                
            return json.loads(output_content.strip())

        except Exception as e:
            print(f"Error in Nova analysis: {e}")
            # Fallback mock response for testing/failure
            return {
                "match_score": 0,
                "missing_skills": ["Error analyzing"],
                "matching_skills": [],
                "roadmap": [],
                "advice": f"Could not generate analysis. Error: {str(e)}"
            }

    def fetch_learning_resources(self, skills: list) -> list:
        """
        Simulates an Agent (Nova Act) that searches for resources.
        In a full implementation, this might call a Bedrock Agent alias.
        """
        resources = []
        for skill in skills[:5]: # Limit to top 5 missing skills to save time
            # Placeholder for actual search logic or Bedrock Agent invocation
            resources.append({
                "title": f"Learn {skill} - Official Docs",
                "url": f"https://www.google.com/search?q={skill}+documentation",
                "type": "Documentation"
            })
            resources.append({
                "title": f"{skill} Crash Course",
                "url": f"https://www.youtube.com/results?search_query={skill}+tutorial",
                "type": "Video"
            })
        return resources
