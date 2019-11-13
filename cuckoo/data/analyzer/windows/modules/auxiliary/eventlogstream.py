# Copyright (C) 2019 - Y. de Boer
import logging

import os
import os.path
import subprocess

from lib.common.abstracts import Auxiliary
from lib.common.exceptions import CuckooDisableModule, CuckooPackageError

log = logging.getLogger(__name__)


class EventlogStream(Auxiliary):
    def start(self):
        self.key = "eventlogstream"

        bin_path = os.path.abspath("/winlogbeat/")

        self.winlogbeat_exe = os.path.join(bin_path, "winlogbeat.exe")
        self.winlogbeat_config = os.path.join(bin_path, "winlogbeat.yml")
        
        if not os.path.exists(self.winlogbeat_exe):
            raise CuckooPackageError(
               "Could not find winlogbeat.exe at {}".format(self.winlogbeat_exe)
            )

        log.info("Winlogbeat starting...")
        self.p = subprocess.Popen([
            self.winlogbeat_exe,
            "-c", self.winlogbeat_config
        ])

    def stop(self):
        log.info("Terminating winlogbeat...")
        self.p.terminate()
        log.info("Winlogbeat terminated.")

