blackbird-chrony
===============

[![Build Status](https://travis-ci.org/Vagrants/blackbird-chrony.png?branch=development)](https://travis-ci.org/Vagrants/blackbird-chrony)

Get information of time synchronization by using 'chronyc'

```
Reference ID    : 10.0.0.1 (ntp.local)
Stratum         : 3
Ref time (UTC)  : Tue Jan 13 06:47:26 2015
System time     : 0.000110986 seconds fast of NTP time
Last offset     : +0.000061137 seconds
RMS offset      : 0.000078883 seconds
Frequency       : 18.793 ppm slow
Residual freq   : +0.001 ppm
Skew            : 0.020 ppm
Root delay      : 0.002852 seconds
Root dispersion : 0.002294 seconds
Update interval : 1036.2 seconds
Leap status     : Normal
```

Data to be sent is as follows

* Reference ID
* Stratum
* Ref time
* System time
* Last offset
* RMS offset
* Frequency
* Residual freq
* Skew
* Root delay
* Root dispersion
* Update interval
* Leap status

## Install

You can install by pip.

```
$ pip install git+https://github.com/Vagrants/blackbird-chrony.git
```

Or you can also install rpm package from [blackbird repository](https://github.com/Vagrants/blackbird/blob/master/README.md).

```
$ sudo yum install blackbird-chrony --enablerepo=blackbird
```
