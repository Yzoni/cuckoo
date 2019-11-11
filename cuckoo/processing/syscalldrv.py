# Copyright (C) 2019 Y. de Boer

import os.path
import subprocess

from cuckoo.common.abstracts import Processing

class Syscalldrv(Processing):
    """Extract events from syscalldrv output."""

    key = "syscalldrv"

    def run(self):
        system_evtx = os.path.join(self.logs_path, "System.evtx")
        if not os.path.exists(system_evtx):
            return

        # Run extraction to csv
        #subprocess.run(["evtx_extract", ""])

        # Compress the created csv files


        return
