# Copyright (C) 2019 - Y. de Boer
import logging

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

    def stop(self):
        # Upload the EVTX file to the host.
        upload_to_host(self.eventlog_path, os.path.join("files", "System.evtx"))
