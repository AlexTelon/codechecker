# -------------------------------------------------------------------------
#                     The CodeChecker Infrastructure
#   This file is distributed under the University of Illinois Open Source
#   License. See LICENSE.TXT for details.
# -------------------------------------------------------------------------
"""
"""

import re
import fnmatch
from codechecker_lib import logger

LOG = logger.get_new_logger('SKIPLIST_HANDLER')

class SkipListHandler(object):
    """
    Skiplist file format:

    -/skip/all/source/in/directory*
    -/do/not/check/this.file
    +/dir/check.this.file
    -/dir/*

    """

    def __init__(self, skip_file):
        """
        read up the skip file
        """
        self.__skip = []

        skip_file_content = []

        with open(skip_file, 'r') as skip_file:
            skip_file_content = [line.strip() for line in skip_file if line != '']

        for line in skip_file_content:
            if len(line) < 2 or line[0] not in ['-', '+']:
                LOG.warning("Skipping malformed skipfile pattern: " + line)
                continue
            rexpr = re.compile(fnmatch.translate(line[1:].strip() + '*'))
            self.__skip.append((line[0], rexpr))

    def should_skip(self, source):
        """
        check if the given source sourld be skipped
        Should the analyzer skip the given source file?
        """

        for sign, rexpr in self.__skip:
            if rexpr.match(source):
                return sign == '-'
        return False

    def get_skiplist(self, file_name):
        """
        Read skip file and return with its content in a list.
        """

        skiplist_with_comment = {}
        for line in self.__skip:
            skiplist_with_comment[line] = ''

        return skiplist_with_comment