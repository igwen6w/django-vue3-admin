import logging

class IgnoreSQLFilter(logging.Filter):
    def __init__(self, name=''):
        super().__init__(name)
        # 后续只要在这里添加关键字即可
        self.ignore_keywords = [
            'authtoken_token',
            '@@lower_case_table_names',
            'SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        ]

    def filter(self, record):
        sql = record.getMessage().strip().lower()
        # 如果包含任何一个关键字，则返回 False（不打印）
        for keyword in self.ignore_keywords:
            if keyword.lower() in sql:
                return False
        return True