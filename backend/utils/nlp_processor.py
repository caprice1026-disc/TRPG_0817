from openai import OpenAI
import os

client = OpenAI()

class SingletonBase:
    _instance = None

    @classmethod
    def get_instance(cls):
        """シングルトンクラスを生成する"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class OpenAIClient(SingletonBase):
    def __init__(self):
        """OpenAIクライアントの初期化"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    @classmethod
    def get_client(cls):
        return cls.get_instance().client

"""OpenAI呼び出しの例

client = OpenAIClient.get_client()
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

message = completion.choices[0].message.content
"""