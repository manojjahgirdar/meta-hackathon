def get_Bedrock_llm():
    from langchain_aws import BedrockLLM

    llm = BedrockLLM(
        credentials_profile_name="default",
        provider="meta",
        model_id="arn:aws:bedrock:us-east-1:367328181879:inference-profile/us.meta.llama3-2-90b-instruct-v1:0",
        model_kwargs={"temperature": 0}, # Greedy Mode 
        streaming=False,
    )

    return llm

def get_Watsonx_llm():
    from langchain_ibm import WatsonxLLM
    from config.app_config import AppConfig
    
    app_config = AppConfig()

    watsonx_llm = WatsonxLLM(
        url=app_config.WX_ENDPOINT,
        apikey=app_config.IBM_CLOUD_API_KEY,
        project_id=app_config.WX_PROJECT_ID,
        model_id=app_config.WX_MODEL_ID,
        params=app_config.WX_PARAMS
    )

    return watsonx_llm
