import requests

from config import Config
import json
import dingtalk_stream
from loguru import logger
from dify_client import CompletionClient, ChatClient


class Connector(dingtalk_stream.GraphHandler):
    MARKDOWN_TEMPLATE_ID = 'd28e2ac5-fb34-4d93-94bc-cf5c580c2d4f.schema'
    # 区块卡片：d28e2ac5-fb34-4d93-94bc-cf5c580c2d4f.schema
    # 普通卡片：1e6c3d7e-01b4-41fa-a5fb-793a45deb2ac.schema
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        request = dingtalk_stream.GraphRequest.from_dict(callback.data)
        self.logger.info('incoming request, method={}, uri={}, body={}',
                         request.request_line.method, request.request_line.uri,
                         request.body)
        payload = json.loads(request.body)

        reply = self.get_dify_reply(payload['rawInput'], payload['unionId'])

        self.reply_markdown(payload['sessionWebhook'], reply['answer'])

        response = self.get_success_response()
        return dingtalk_stream.AckMessage.STATUS_OK, response.to_dict()

    def get_success_response(self):
        response = dingtalk_stream.GraphResponse()
        response.status_line.code = 200
        response.status_line.reason_phrase = 'OK'
        response.headers['Content-Type'] = 'application/json'
        response.body = json.dumps({}, ensure_ascii=False)
        return response

    def reply_markdown(self, webhook, content):
        payload = {
            'contentType': 'ai_card',
            'content': {
                'templateId': self.MARKDOWN_TEMPLATE_ID,
                'cardData': {
                    'content': content,
                }
            }
        }
        response = requests.post(webhook, json=payload)
        self.logger.info('agent reply, webhook={}, response={}, response.body={}', webhook, response, response.json())

    def get_dify_reply(self, query, user_id):
        client = ChatClient(self.config.dify_api_key)
        client.base_url = self.config.dify_base_url
        reply = client.create_chat_message(inputs={},
                                           query=query,
                                           response_mode='blocking',
                                           user=user_id)
        reply.raise_for_status()
        return reply.json()


class AgentLoop(object):
    def __init__(self):
        self.config = Config()

    def run_forever(self):
        credential = dingtalk_stream.Credential(self.config.dingtalk_client_id, self.config.dingtalk_client_secret)
        client = dingtalk_stream.DingTalkStreamClient(credential)
        client.register_callback_handler(dingtalk_stream.graph.GraphMessage.TOPIC, Connector())
        client.start_forever()