# Copyright (C) 2019 - Y. de Boer

import os.path

from lib.common.abstracts import Auxiliary
from lib.common.exceptions import CuckooDisableModule, CuckooPackageError
from lib.common.results import upload_to_host


class Eventlog(Auxiliary):
    """Allow procmon to be run on the side."""
    def start(self):
        self.log_path = 'C:/System32/Winevt/Logs/System.evtx'

        if not os.path.exists(self.log_path):
            raise CuckooPackageError(
                "System.evtx could not be found."
            )

    def stop(self):
        # Upload the XML file to the host.
        upload_to_host(self.log_path, os.path.join("logs", "System.evtx"))
