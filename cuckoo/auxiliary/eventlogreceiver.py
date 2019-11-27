from cuckoo.common.abstracts import Auxiliary
from winlogbeatserver import winlogbeatserver
import logging
from cuckoo.misc import cwd
import os
import time

log = logging.getLogger(__name__)


class EventlogReceiver(Auxiliary):
    def __init__(self):
        Auxiliary.__init__(self)
        self.wlb = None

    def start(self):
        """
        Start the custom Winlogbeat receiver server
        """
        eventlogs_path = cwd("eventlogs", analysis=self.task.id)
        os.mkdir(eventlogs_path)
        
        self.wlb = winlogbeatserver.WinlogBeat(eventlogs_path)

        log.info('Starting Winlogbeat server')
        self.wlb.start()

    def stop(self):
        """
        Stop the custom Winlogbeat receiver server
        """
        logging.info('Current Winlogbeat processing queue still contains {} items to be processed.'.format(
            self.wlb.queue_size()))

        stop_counter = 0
        while self.wlb.queue_size() > 0 and stop_counter < 5:
            logging.info('Winlogbeat queue still not empty, {} items remaining.'.format(self.wlb.queue_size()))
            time.sleep(5)
            stop_counter += 1

        logging.info('Queue empty... {} items remaining'.format(self.wlb.queue_size()))
        self.wlb.stop(compress=True)
