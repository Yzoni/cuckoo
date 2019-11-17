from cuckoo.common.abstracts import Auxiliary
# from winlogbeatserver import winlogbeatserver
import logging
from cuckoo.misc import cwd
import os
import time
import subprocess
import sys
from cuckoo.common.exceptions import CuckooOperationalError

log = logging.getLogger(__name__)


class EventlogReceiver(Auxiliary):
    def __init__(self):
        Auxiliary.__init__(self)
        self.proc = None

    def start(self):
        """
        Start the custom Winlogbeat receiver server
        """
        eventlogs_path = cwd("eventlogs", analysis=self.task.id)
        os.mkdir(eventlogs_path)


        pargs = [sys.executable,
                 "/root/winlogbeatserver/winlogbeatserver/winlogbeatserver.py",
                 eventlogs_path,
                 '--logfile', os.path.join(eventlogs_path, 'eventlogserver.log'),
                 '--debug']
        self.proc = subprocess.Popen(
            pargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True
        )

        time.sleep(3)
        if not self.proc.poll():
            log.info('Eventlog server started')
        
        # self.wlb = winlogbeatserver.WinlogBeat(eventlogs_path)
        # 
        # log.info('Starting Winlogbeat server')
        # self.wlb.start()

    def stop(self):
        """
        Stop the custom Winlogbeat receiver server
        """
        # logging.info('Current Winlogbeat processing queue still contains {} items to be processed.'.format(
        #     self.wlb.queue_size()))
        #
        # while self.wlb.queue_size() > 0:
        #     logging.info('Winlogbeat queue still not empty, {} items remaining.'.format(self.wlb.queue_size()))
        #     time.sleep(5)
        #
        # logging.info('Queue empty... {} items remaining'.format(self.wlb.queue_size()))
        # self.wlb.stop()

        if self.proc.poll():
            out, err = self.proc.communicate()
            raise CuckooOperationalError(
                "Wineventlog server already dead... {}; {}".format(out, err))

        try:
            self.proc.kill()
            time.sleep(2)
        except:
            try:
                if not self.proc.poll():
                    log.debug("Killing Wineventlog")
                    self.proc.kill()
            except OSError as e:
                log.debug("Error killing Wineventlog: %s. Continue", e)
            except Exception as e:
                log.exception("Unable to stop the Wineventlog with pid %d: %s",
                              self.proc.pid, e)
