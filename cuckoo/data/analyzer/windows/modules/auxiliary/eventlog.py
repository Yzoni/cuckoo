# Copyright (C) 2019 - Y. de Boer

import os.path

from lib.common.abstracts import Auxiliary
from lib.common.exceptions import CuckooDisableModule, CuckooPackageError
from lib.common.results import upload_to_host


class Eventlog(Auxiliary):
    def start(self):
        self.key = "eventlog"

        self.eventlog_path = "C:/Windows/System32/Winevt/Logs/System.evtx"
        #
        # if not os.path.exists(self.eventlog_path):
        #     raise CuckooPackageError(
        #         "{} could not be found.".format(self.eventlog_path)
        #     )

    def stop(self):
        contentsb = os.listdir("/")
        contentsa = os.listdir("/Windows/System32/Winevt/Logs/")
        if not os.path.exists(self.eventlog_path):
            raise CuckooPackageError(
                "{} could not be found. {}. {}.".format(self.eventlog_path, contentsa, contentsb)
            )
        # Upload the EVTX file to the host.
        upload_to_host(self.eventlog_path, os.path.join("files", "System.evtx"))
