import json
import os
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""
    list_json = {}

    def __init__(self, channel_id: str):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.youtube = None
        self.__channel_id = channel_id

        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']["default"]['url']
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.views_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
            return f'{self.title}, {self.url}'

    def __add__(self, other):
            return int(self.subscriber_count) + int(other.subscriberCount)

    def __sub__(self, other):
            return int(self.subscriber_count) - int(other.subscriberCount)

    def __gt__(self, other):
            return int(self.subscriber_count) > int(other.subscriberCount)

    def __ge__(self, other):
            return int(self.subscriber_count) >= int(other.subscriberCount)

    def __lt__(self, other):
            return int(self.subscriber_count) < int(other.subscriberCount)

    def __le__(self, other):
            return int(self.subscriber_count) <= int(other.subscriberCount)

    def __eq__(self, other):
            return int(self.subscriber_count) == int(other.subscriberCount)

    @property
    def channel_id(self):
        return self.channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(
            json.dumps(self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2,
                       ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        object_get = build('youtube', 'v3', developerKey=api_key)
        return object_get

    def to_json(self, filename):
        list_json = self.list_json
        list_json['id'] = self.__channel_id
        list_json['title'] = self.title
        list_json['description'] = self.description
        list_json['url'] = self.url
        list_json['subscriber_count'] = self.subscriber_count
        list_json['video_count'] = self.video_count
        list_json['views_count'] = self.views_count

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.list_json, f, indent=2, ensure_ascii=False)
