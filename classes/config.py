import json
from typing import Dict

class Config:

    DEFAULT_MINUTES_PER_COUNT = 60
    DEFAULT_COUNT_ENABLED = True
    DEFAULT_COUNT_FORMAT = "{count}."
    DEFAULT_LESSON_TITLE_ENABLED = True
    DEFAULT_LESSON_INDEX_FORMAT = '{section}.{number}'
    DEFAULT_RANGE_SEPARATOR = '~'
    DEFAULT_DURATION_ENABLED = True
    DEFAULT_DURATION_FORMAT = '({hh}:{mm}:{ss})'

    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.init()

    def load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def init(self):
        self.minutes_per_count = self.config.get('average_minutes_per_count', self.DEFAULT_MINUTES_PER_COUNT)

        self.enable_count = self.get_value('count_settings', 'include_count', self.DEFAULT_COUNT_ENABLED)
        self.count_format_str = self.get_value('count_settings', 'format', self.DEFAULT_COUNT_FORMAT)

        self.enable_start_title = self.get_value('range_settings', 'include_start_lesson_title', self.DEFAULT_LESSON_TITLE_ENABLED)
        self.enable_end_title = self.get_value('range_settings', 'include_end_lesson_title', self.DEFAULT_LESSON_TITLE_ENABLED)
        self.index_format_str = self.get_value('range_settings', 'lesson_index_format', self.DEFAULT_LESSON_INDEX_FORMAT)

        self.range_separator = self.get_value('range_settings', 'range_separator_format', self.DEFAULT_RANGE_SEPARATOR)

        self.enable_duration = self.get_value('duration_settings', 'include_duration', self.DEFAULT_DURATION_ENABLED)
        self.duration_format_str = self.get_value('duration_settings', 'format', self.DEFAULT_DURATION_FORMAT)

    def get_value(self, key1: str, key2: str, default=None):
        return self.config.get(key1).get(key2, default)

    def get(self, key: str, default=None):
        return self.config.get(key, default)
