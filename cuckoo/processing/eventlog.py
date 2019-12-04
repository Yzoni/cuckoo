# Copyright (C) 2019 Y. de Boer

import os.path
import subprocess
import logging
import distutils

from cuckoo.misc import cwd
from cuckoo.common.abstracts import Processing

log = logging.getLogger(__name__)

class Eventlog(Processing):
    """Extract events from syscalldrv output."""

    key = "eventlog"

    def list_system_evtx_filepaths(self):
        """Get all paths including archived ones of system.evtx"""
        eventlog_root = self.file_path

        system_logs = []
        for filename in os.listdir(eventlog_root):
            if filename.startswith('Archive-System') or filename.startswith('System'):
                new_path = os.path.join(eventlog_root, filename)
                system_logs.append(new_path)

        log.info('Found event logs: {}'.format(system_logs))

        return system_logs

    @staticmethod
    def compress(filename):
        xz_bin = distutils.spawn.find_executable("xz")
        if xz_bin:
            status = subprocess.check_call([xz_bin, filename])
            if status != 0:
                log.error('Eventlog compressions of {} failed'.format(filename))
        else:
            log.warning('Cannot compress eventlog file, unable to find xz binary utility.')

    def run(self):
        eventlogs_extracted_path = cwd("eventlogs", analysis=self.task.id)
        if not os.path.exists(eventlogs_extracted_path):
            os.mkdir(eventlogs_extracted_path)
        
        # Run extraction to csv
        syscall_file = os.path.join(eventlogs_extracted_path, 'syscall.csv')
        process_file = os.path.join(eventlogs_extracted_path, 'process.csv')
        thread_file = os.path.join(eventlogs_extracted_path, 'thread.csv')
        status_file = os.path.join(eventlogs_extracted_path, 'status.csv')
        for eventlog in self.list_system_evtx_filepaths():
            current_extraction_path = os.path.join(eventlogs_extracted_path, os.path.split(eventlog)[-1])

            log.info('Going to extract {} to {}'.format(eventlog, current_extraction_path))
            subprocess.run(["evtx_extract", eventlog,
                            "-f", current_extraction_path])

            # Merge all extracted files together
            for partial_extracted in os.path.listdir(current_extraction_path):
                partial_path = os.path.join(current_extraction_path, partial_extracted)
                log.info('Opening partial event log: {}'.format(partial_path))
                with open(partial_path) as f_partial:
                    if partial_extracted.startswith('syscall'):
                        with open(syscall_file, 'wa') as f:
                            f.write(f_partial.read())
                    if partial_extracted.startswith('process'):
                        with open(process_file, 'wa') as f:
                            f.write(f_partial.read())
                    if partial_extracted.startswith('thread'):
                        with open(thread_file, 'wa') as f:
                            f.write(f_partial.read())
                    if partial_extracted.startswith('status'):
                        with open(status_file, 'wa') as f:
                            f.write(f_partial.read())

        log.info('Compressing merged event log files...')
        # Compress the created csv files
        self.compress(syscall_file)
        self.compress(process_file)
        self.compress(thread_file)
        self.compress(status_file)

        return
