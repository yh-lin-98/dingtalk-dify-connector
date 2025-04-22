import os


class Config(object):
    def __init__(self):
        self.dingtalk_client_id = os.getenv('DINGTALK_CLIENT_ID')
        self.dingtalk_client_secret = os.getenv('DINGTALK_CLIENT_SECRET')
        self.dify_api_key = os.getenv('DIFY_API_KEY')
        self.dify_base_url = os.getenv('DIFY_BASE_URL', 'https://api.dify.ai/v1')