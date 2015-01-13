"""
blackbird chrony module

get information of time synchronization by using 'chronyc'
"""

__VERSION__ = '0.1.0'

import subprocess

from blackbird.plugins import base


class ConcreteJob(base.JobBase):
    """
    This class is Called by "Executor".
    Get chrony information and send to backend.
    """

    def __init__(self, options, queue=None, logger=None):
        super(ConcreteJob, self).__init__(options, queue, logger)

    def build_items(self):
        """
        main loop
        """

        # ping item
        self.ping()

        # chronyc tracking
        self.chrony_tracking()

    def _enqueue(self, key, value):
        """
        set queue item
        """

        item = ChronyItem(
            key=key,
            value=value,
            host=self.options['hostname']
        )
        self.queue.put(item, block=False)
        self.logger.debug(
            'Inserted to queue {key}:{value}'
            ''.format(key=key, value=value)
        )

    def ping(self):
        """
        send ping item
        """

        self._enqueue('blackbird.chrony.ping', 1)
        self._enqueue('blackbird.chrony.version', __VERSION__)

    # pylint: disable=too-many-locals
    def chrony_tracking(self):
        """
        execute chronyc tracking
        """

        _cmd = [
            self.options['path'],
            '-h', self.options['host'],
            '-m', 'retries {rt}'.format(rt=self.options['retry']),
            'timeout {to}'.format(to=self.options['timeout']),
            'tracking'
        ]

        try:
            output, _ = subprocess.Popen(
                _cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            ).communicate()
        except OSError:
            self._enqueue('chrony.synchronized', 0)
            raise base.BlackbirdPluginError(
                'can not exec "{cmd}", failed to get chrony information'
                ''.format(cmd=' '.join(_cmd))
            )

        if 'Cannot talk to daemon' in output:
            self._enqueue('chrony.synchronized', 0)
            raise base.BlackbirdPluginError(
                'chronyc error [{err}]'.format(err=output.strip())
            )

        _chny_output = dict()

        for line in output.rstrip().splitlines():

            _key, _value = line.split(' : ')
            _chny_output[_key.rstrip()] = _value

        # Reference ID
        _refid = _chny_output['Reference ID'].split()[0]
        self._enqueue('chrony.reference_id', _refid)

        # Stratum
        self._enqueue('chrony.stratum', _chny_output['Stratum'])

        # Ref time (UTC)
        self._enqueue('chrony.reference_time', _chny_output['Ref time (UTC)'])

        # System time
        _stime, _desc = _chny_output['System time'].split(' ', 1)
        if 'slow' in _desc:
            _stime = float(_stime) * -1
        self._enqueue('chrony.system_time', _stime)

        # Last offset
        _loffset = _chny_output['Last offset'].split()[0]
        self._enqueue('chrony.last_offset', _loffset)

        # RMS offset
        _roffset = _chny_output['RMS offset'].split()[0]
        self._enqueue('chrony.rms_offset', _roffset)

        # Frequency
        _freq, _desc = _chny_output['Frequency'].split(' ', 1)
        if 'slow' in _desc:
            _freq = float(_freq) * -1
        self._enqueue('chrony.frequency', _freq)

        # Residual freq
        _residual = _chny_output['Residual freq'].split()[0]
        self._enqueue('chrony.residual_frequency', _residual)

        # Skew
        _skew = _chny_output['Skew'].split()[0]
        self._enqueue('chrony.skew', _skew)

        # Root delay
        _rdelay = _chny_output['Root delay'].split()[0]
        self._enqueue('chrony.root_delay', _rdelay)

        # Root dispersion
        _rdisp = _chny_output['Root dispersion'].split()[0]
        self._enqueue('chrony.root_dispersion', _rdisp)

        # Update interval
        _upd_int = _chny_output['Update interval'].split()[0]
        self._enqueue('chrony.update_interval', _upd_int)

        # Leap status
        _leap = _chny_output['Leap status']
        self._enqueue('chrony.leap_status', _chny_output['Leap status'])

        if _leap == 'Not synchronised':
            self._enqueue('chrony.synchronized', 0)
        else:
            self._enqueue('chrony.synchronized', 1)


# pylint: disable=too-few-public-methods
class ChronyItem(base.ItemBase):
    """
    Enqued item.
    """

    def __init__(self, key, value, host):
        super(ChronyItem, self).__init__(key, value, host)

        self._data = {}
        self._generate()

    @property
    def data(self):
        return self._data

    def _generate(self):
        self._data['key'] = self.key
        self._data['value'] = self.value
        self._data['host'] = self.host
        self._data['clock'] = self.clock


class Validator(base.ValidatorBase):
    """
    Validate configuration.
    """

    def __init__(self):
        self.__spec = None

    @property
    def spec(self):
        self.__spec = (
            "[{0}]".format(__name__),
            "path=string(default='/usr/bin/chronyc')",
            "host=string(default='127.0.0.1')",
            "timeout=integer(100, 10000, default=1000)",
            "retry=integer(1, 100, default=1)",
            "hostname=string(default={0})".format(self.detect_hostname()),
        )
        return self.__spec
