class AppConfig:
    PLANNING_PROMPT='config/planning_prompt.txt'
    QUESTIONS_JSON_PATH='db/questions.json'
    AGENT_VERBOSE=False
    IBM_CLOUD_API_KEY=""
    WX_PROJECT_ID=""
    WX_ENDPOINT="https://us-south.ml.cloud.ibm.com"
    WX_MODEL_ID="meta-llama/llama-3-70b-instruct"
    WX_PARAMS={"max_new_tokens": 500, "min_new_tokens": 10}
