"""Logging"""

import datetime

SEVERITY_LEVELS_STR = ("emerg", "alert", "crit", "error", "warning", "notice", "info", "debug")

class SeverityLevels:
    emerg = 0
    alert = 1
    crit = 2
    err = 3
    warning = 4
    notice = 5
    info = 6
    debug = 7

class Logger:
    def __init__(self, min_severity=SeverityLevels.info, output_file=None, print_to_stdout=False):
        self.min_severity = min_severity
        self.output_file = output_file
        self.print_to_stdout = print_to_stdout

    def emerg(self, message=False):
        self._log_event(SeverityLevels.emerg, message)

    def alert(self, message=False):
        self._log_event(SeverityLevels.alert, message)

    def crit(self, message=False):
        self._log_event(SeverityLevels.crit, message)

    def err(self, message=False):
        self._log_event(SeverityLevels.err, message)

    def warning(self, message=False):
        self._log_event(SeverityLevels.warning, message)

    def notice(self, message=False):
        self._log_event(SeverityLevels.notice, message)

    def info(self, message=False):
        self._log_event(SeverityLevels.info, message)

    def debug(self, message=False):
        self._log_event(SeverityLevels.debug, message)

    def _log_event(self, severity_level, message):
        log_output = self._get_log_output(severity_level, message)
        if self.output_file:
            with open(self.output_file, 'a') as outfile:
                outfile.write("{0}\n".format(log_output))
        if self.print_to_stdout:
            print log_output

    def _get_log_output(self, severity_level, message):
        timestamp = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        severity_level_str = SEVERITY_LEVELS_STR[severity_level]
        output = "{0} {1}: {2}".format(timestamp, severity_level_str, message)
        return output
