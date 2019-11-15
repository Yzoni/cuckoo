from cuckoo.common.abstracts import Auxiliary
from winlogbeatserver import winlogbeatserver
import logging
from cuckoo.misc import cwd
import os

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
        logging.info('Current Winlogbeat processing queue still contained #{} to be processed items.'.format(
            self.wlb.queue_size()))
        logging.info('Stopping Winlogbeat server anyway...')
        self.wlb.stop()
