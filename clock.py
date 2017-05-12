
class Clock:
    """
    Class that acts like a clock.

    For doctest -

    >>> c = Clock(23, 59, 59)
    >>> print c
    23:59:59
    >>> c.setTime(0, 0, 0)
    >>> print c
    00:00:00

    # However, the print will fail
    >>> c.setTime(-1, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Hours not in range or null: -1

    # Tick with seconds overflow
    >>> c.setTime(23, 58, 59)
    >>> c.tick()
    >>> print c
    23:59:00

    # Tick with seconds + hours overflow
    >>> c.setTime(23, 59, 59)
    >>> c.tick()
    >>> print c
    00:00:00

    # Check time policies
    >>> c.setTime(23, 0, 0)
    >>> c.isEnergySavingsTime()
    True
    >>> c.setTime(5, 0, 0)
    >>> c.isEnergySavingsTime()
    True
    >>> c.setTime(6, 59, 59)
    >>> c.isEnergySavingsTime()
    True
    >>> c.setTime(7, 0, 0)
    >>> c.isEnergySavingsTime()
    False
    >>> c.setTime(22, 0, 0)
    >>> c.isEnergySavingsTime()
    True
    >>> c.setTime(21, 59, 59)
    >>> c.isEnergySavingsTime()
    False


    """

    def __init__(self, hours = None, minutes = None, seconds=None):
        self.energySavingsMode = False

        if seconds != None and 0 <= seconds < 60:
            self.seconds = seconds
        else:
            raise ValueError("Seconds not in range or null: {}".format(seconds))

        if minutes != None and 0 <= minutes < 60:
            self.minutes = minutes
        else:
            raise ValueError("Minutes not in range or null: {}".format(minutes))

        if hours != None and 0 <= hours < 24:
            self.hours = hours
        else:
            raise ValueError("Hours not in range or null: {}".format(hours))


    def tick(self):
        secondsCarry = False
        minutesCarry = False

        if self.seconds == 59:
            secondsCarry = True

        if self.minutes == 59:
            minutesCarry = True

        self.seconds = (self.seconds + 1) % 60

        if secondsCarry:
            self.minutes = (self.minutes + 1) % 60

        if minutesCarry:
            self.hours =  (self.hours + 1) % 24


    def tickMinutes(self):
        minutesCarry = False

        if self.minutes == 59:
            minutesCarry = True

        self.minutes = (self.minutes + 1) % 60

        if minutesCarry:
            FIRST_CHANGE = False
            self.hours = (self.hours + 1) % 24


    def isEnergySavingsTime(self):
        self.energySavingsMode = self.hours >= 22 or self.hours < 7
        return self.energySavingsMode


    def isEnergySavingsTimeForDemo(self):
        if self.hours % 3 == 0 and self.minutes == 0:
            self.energySavingsMode = not self.energySavingsMode
        return self.energySavingsMode


    def setTime(self, hours, minutes, seconds):
        if seconds != None and 0 <= seconds < 60:
            self.seconds = seconds
        else:
            raise ValueError("Seconds not in range or null: {}".format(seconds))

        if minutes != None and 0 <= minutes < 60:
            self.minutes = minutes
        else:
            raise ValueError("Minutes not in range or null: {}".format(minutes))

        if hours != None and 0 <= hours < 24:
            self.hours = hours
        else:
            raise ValueError("Hours not in range or null: {}".format(hours))


    def __str__(self):
        hours, minutes, seconds = str(self.hours), str(self.minutes), str(self.seconds)
        hours = hours if len(hours) > 1 else "0" + hours
        minutes = minutes if len(minutes) > 1 else "0" + minutes
        seconds = seconds if len(seconds) > 1 else "0" + seconds

        return str(hours) + ":" + str(minutes) + ":" + str(seconds)


    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        return self.seconds == other.seconds and self.minutes == other.minutes \
            and self.hours == other.hours


if __name__ == '__main__':
    import doctest
    doctest.testmod()
