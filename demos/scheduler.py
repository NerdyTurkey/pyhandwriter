import time as time


def now():
    # returns time now in milliseconds
    return int(time.time() * 1000)


class Scheduler:
    """
    A class that manages the timing of user events in a loop, e.g a game loop.
    Example:
    ==========================================================================
    s = Scheduler()
    #....

    # loop
    while True:
        #....
        s.update(conditional,
            (delay1, user_func1, args1, kwargs1),
            (delay2, user_func2, args2, kwargs2),
            ......
        )
        #... other code that also include break out of while at some point
    ==========================================================================
    where nothing happens until conditional becomes true
        then after delay1, user_func1 is run with args1 and kwargs1 passed
        then after delay2, user_func2 is run with args2 and kwargs2 passed
        then after delay3, user_func3 is run with args3 and kwargs3 passed
        etc

    Note:
        delays are in milliseconds
        argsi must be a tuple of arguments relating to user_funci, e.g. (player_health, score)
            if none, use ()
            if only one, use (single_arg,)
        kwargsi must be a dict of keyword arguments corresponding to user_funci,
            e.g. {"volume": 20} or dict(volume=20)
            if none, use {} or dict()
        the latest values of args and kwargs will be used, ie. at last update
            before delay times out
    """

    def __init__(self):
        self._started = False  # becomes true when start_condition met
        self._event_num = -1  # number of current event
        self._delay = None  # current delay
        self._is_last = False  # becomes true when on last event
        self._all_finished = False  # becomes true when finished all events

    def update(self, start_condition, *params):
        """
        Public method to update schedule.
        Keeps track of whether event delay has time-out and if so
        runs the user function for that event, passing the 'current' value
        of the args and kwargs for that function.
        Here 'current' means as of last update call.
        """
        if not params or self._all_finished:
            return
        if not self._started and start_condition:
            self._started = True
        if self._started:
            self._update(*params)

    def _update(self, *params):
        if self._delay is None:
            self._start_time = now()
            self._delay, self._func = self._get_next(*params)
        if now() - self._start_time >= self._delay:
            # current delay has time-out
            # refresh args
            args, kwargs = self._get_args_kwargs(*params)
            self._func(*args, **kwargs)  # call user function
            if self._is_last:
                self._all_finished = True
                return
            # start processing next event
            self._start_time = now()
            self._delay, self._func = self._get_next(*params)

    def _get_args_kwargs(self, *params):
        """
        Returns as a tuple the arg and kwargs for the current function
        """
        event_info = params[self._event_num]
        return event_info[2], event_info[3]

    def _get_next(self, *params):
        """
        Returns as a tuple the delay and function for the next event
        and increments the event number.
        """
        self._event_num += 1
        event_info = params[self._event_num]
        if self._event_num == len(params) - 1:
            self._is_last = True
        return event_info[0], event_info[1]


def example1():
    def my_func(x, y, m=1):
        """
        This is just a pointless test function"""
        print((x - y) * m)

    start_time = now()
    run_time = 7000  # ms
    scheduler = Scheduler()
    i = 0
    while now() - start_time < run_time:
        # If i==200, this Scheduler instance
        # will wait 1000ms and then call my_func(now(), start_time)
        # then wait 2000ms and call my_func(now(), start_time)
        # then wait 3000ms and call my_func(now(), start_time).
        # my_func is set up to print the elapsed time
        scheduler.update(i == 200,  # nothing starts until this condition is met
                 (1000, my_func, (now(), start_time,), dict()),
                 (2000, my_func, (now(), start_time,), dict()),
                 (3000, my_func, (now(), start_time,), dict()),
                 )
        i += 1


def example2():
    run_time = 5000  # ms
    start_time = now()
    scheduler = Scheduler()
    while now() - start_time < run_time:
        scheduler.update(True, # start on first call
                  (1000, print, (f"Elapsed time = {now() - start_time}ms, Example of scheduler",), {}),
                  (1000, print, (f"Elapsed time = {now() - start_time}ms",  "Written", "by "), dict(sep="...", end="")),
                  (1000, print, ("NerdyTurkey, ", f"Elapsed time = {now() - start_time}ms"), {}),
                  (1000, print, (f"Elapsed time = {now() - start_time}ms,  Goodbye!",), {}),
                  )

def main():
    example1()
    example2()


if __name__ == "__main__":
    main()
