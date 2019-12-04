# Copyright (C) 2019 - Y. de Boer
import logging

import time
import os
import os.path

from lib.common.abstracts import Auxiliary
from lib.common.exceptions import CuckooDisableModule, CuckooPackageError
from lib.common.results import upload_to_host

log = logging.getLogger(__name__)


class Eventlog(Auxiliary):
    def start(self):
        self.key = "eventlog"

        self.eventlog_path = os.path.abspath("/Windows/Sysnative/winevt/Logs/System.evtx")

        if not os.path.exists(self.eventlog_path):
            raise CuckooPackageError(
                "{} could not be found.".format("/Windows/System32/")
            )
        else:
            log.info('Eventlog file found in System32!')

    def humaninfy_filesize(self, nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    def list_system_evtx_filepaths(self):
        """Get all paths including archived ones of system.evtx"""
        eventlog_root = os.path.abspath("/Windows/Sysnative/winevt/Logs/")

        system_logs = {}
        for filename in os.listdir(eventlog_root):
            if filename.startswith('Archive-System') or filename.startswith('System'):
                new_path = os.path.join(eventlog_root, filename)
                system_logs[new_path] = self.humaninfy_filesize(os.path.getsize(new_path))

        log.info('Found event logs: {}'.format(system_logs))

        return system_logs

    def stop(self):
        # Upload the EVTX file to the host.
        eventlog_paths = self.list_system_evtx_filepaths()
        
        log.info('Make sure eventlog is flushed to file by waiting 2 minutes')
        time.sleep(120)
        log.info('Waiting for eventlog flush is over')
        
        for path, size in eventlog_paths.items():
            log.info('Uploading eventlog {} of size {} to host.'.format(path, size))
            upload_to_host(self.eventlog_path, os.path.join("files", "System.evtx"))
            log.info('Finished uploading {} to host'.format(path))
