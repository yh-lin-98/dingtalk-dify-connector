import os


class Config(object):
    def __init__(self):
        self.dingtalk_client_id = os.getenv('dingiypkldq51edhn67v')
        self.dingtalk_client_secret = os.getenv('lxP0YOZu6I92zPYBje0Z0I3jugK1GHLXz1PJHx8TCJPmlnjIKFWgr42IZOJQsuIi')
        self.dify_api_key = os.getenv('DIFY_API_KEY')
        self.dify_base_url = os.getenv('DIFY_BASE_URL', 'https://api.dify.ai/v1')