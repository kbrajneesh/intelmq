# -*- coding: utf-8 -*-
"""
Collector Bot to collect data from a given redis queue

Parameters:
    queue_name: string

"""

import redis
from intelmq.lib.bot import CollectorBot


class RedisCollectorBot(CollectorBot):

    def init(self):

        self.queue_name = getattr(self.parameters, 'queue_name', None)
        self.redis_server = getattr(self.parameters, 'redis_server',
                                    "localhost")
        self.redis_port = getattr(self.parameters, 'redis_port', 6379)
        self.redis_db = getattr(self.parameters, 'redis_db', 0)
        if not self.queue_name:
            self.logger.error("Redis Queue Name parameter not provided")
            self.stop()
        self.redis = redis.Redis(host=self.redis_server, port=self.redis_port,
                                 db=self.redis_db)

    def process(self):
        self.logger.debug("Looking for data in queue: %s" % self.queue_name)
        data_size = self.redis.llen(self.queue_name)
        self.logger.debug("Available items in queue: %s" % data_size)
        if not data_size or data_size == 0:
            self.stop()
        data = []
        for i in range(0, data_size):
            item = self.redis.rpop(self.queue_name)
            item_data = (str(item, "utf-8")).replace('True', 'true')
            report = self.new_report()
            report.add("raw", item_data)
            self.send_message(report)


BOT = RedisCollectorBot
