import json
from typing import Dict, Any

class Config:

    DEFAULT_MINUTES_PER_COUNT = 60
    DEFAULT_COUNT_ENABLED = True
    DEFAULT_COUNT_FORMAT = "{count}."
    DEFAULT_LESSON_TITLE_ENABLED = True
    DEFAULT_LESSON_INDEX_FORMAT = '{section:02}.{number:02}'
    DEFAULT_RANGE_SEPARATOR = '~'
    DEFAULT_DURATION_ENABLED = True
    DEFAULT_DURATION_FORMAT = '({hh:02}:{mm:02}:{ss:02})'

    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.minutes_per_count = self.get_config_value('average_minutes_per_count', self.DEFAULT_MINUTES_PER_COUNT)

        self.enable_count = self.get_nested_value('count_settings', 'include_count', self.DEFAULT_COUNT_ENABLED)
        self.count_format_str = self.get_nested_value('count_settings', 'format', self.DEFAULT_COUNT_FORMAT)

        self.enable_start_title = self.get_nested_value('range_settings', 'include_start_lesson_title', self.DEFAULT_LESSON_TITLE_ENABLED)
        self.enable_end_title = self.get_nested_value('range_settings', 'include_end_lesson_title', self.DEFAULT_LESSON_TITLE_ENABLED)
        self.index_format_str = self.get_nested_value('range_settings', 'lesson_index_format', self.DEFAULT_LESSON_INDEX_FORMAT)

        self.range_separator = self.get_nested_value('range_settings', 'range_separator_format', self.DEFAULT_RANGE_SEPARATOR)

        self.enable_duration = self.get_nested_value('duration_settings', 'include_duration', self.DEFAULT_DURATION_ENABLED)
        self.duration_format_str = self.get_nested_value('duration_settings', 'format', self.DEFAULT_DURATION_FORMAT)

    def load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file not found: {config_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the configuration file: {config_path}")
            return {}

    def get_nested_value(self, key1: str, key2: str, default=None):
        return self.config.get(key1, {}).get(key2, default)

    def get_config_value(self, key: str, default=None):
        return self.config.get(key, default)
