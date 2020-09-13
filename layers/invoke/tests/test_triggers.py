from triggers.functiontrigger import FunctionTrigger
from triggers.timertrigger import TimerTrigger
import datetime
import time


val = None


def sub(v):
    global val
    val = v


def test_function_trigger():
    global val

    t = FunctionTrigger()
    t.subscribe(sub)

    assert val != 45

    t.invoke(45)

    assert val == 45

    t.close()


def test_timer_trigger():
    global val

    delay = 0.5
    max_error = 0.1

    trigger = TimerTrigger(datetime.timedelta(seconds=delay), True, False)
    trigger.subscribe(sub)

    try:
        start = datetime.datetime.utcnow()
        trigger.prime()
        time.sleep(0.2)
        assert (val - start).total_seconds() < 1

        time.sleep(0.2)
        assert (val - start).total_seconds() < 1

        time.sleep(0.2)
        delta = (val - start).total_seconds()
        assert delay + max_error > delta > delay - max_error

    finally:
        trigger.close()
