#
# linter.py
# Linter for SublimeLinter 3, a code checking framework for Sublime Text 3
#
# Written by ckaznocha
# Copyright (c) 2014 ckaznocha
#
# License: MIT
#

"""This module exports the CFLint plugin class."""
from SublimeLinter.lint import Linter, util


class CFLint(Linter):
    """Provides an interface to CFLint."""

    syntax = ('coldfusioncfc', 'html+cfml', 'cfml')
    executable = 'java'
    cmd = None
    regex = r'''(?xi)
        # Severity
        ^\s*Severity:(?:(?P<warning>(WARNING|CAUTION|INFO|COSMETIC))|(?P<error>(FATAL|CRITICAL|ERROR)))\s*$\r?\n

        # Message code
        ^.*$\r?\n

        # File name
        ^.*$\r?\n

        # Column number
        ^\s*Column:(?P<col>\d+)\s*$\r?\n

        # Line number
        ^\s*Line:(?P<line>\d+)\s*$\r?\n

        # Message
        ^\s*Message:(?P<message>.+)$\r?\n

        # Variable
        ^.*$\r?\n

        # Expression
        ^.*$\r?\n
    '''
    multiline = True
    error_stream = util.STREAM_STDOUT
    word_re = r'^<?(#?[-\w]+#?)'
    tempfile_suffix = '-'
    defaults = {
        'jar_file': '',
        'config_file_name': '.cflintrc',
        'aux_config_dirs': []
    }

    def cmd(self):
        """Return the command line to execute."""

        jar_file = self.get_jarfile_path()
        config_file = self.get_config_path()

        return [self.executable_path, '-jar', jar_file, '-configfile', config_file, '-file', '@', '-q', '-text']

    def get_jarfile_path(self):
        """Return the absolute path to the CFLint jar file."""

        settings = self.get_view_settings()
        jar_file = settings.get('jar_file')

        return jar_file

    def get_config_path(self):
        settings = self.get_view_settings()
        config_file_name = settings.get('config_file_name')
        aux_config_dirs = settings.get('aux_config_dirs')
        config_file_tuple = (config_file_name)

        for conf in aux_config_dirs:
            config_file_tuple += (conf,)

        return config_file_tuple