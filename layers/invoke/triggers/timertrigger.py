from trigger import Trigger
from threading import Thread
import time
from datetime import datetime, timedelta
from threading import Event


class TimerTrigger(Trigger):
    def __init__(self, duration, run_on_start=True, quantize=True, offset=timedelta(0)):
        super().__init__()

        self.duration = duration
        self.offset = offset
        self.run_on_start = run_on_start
        self.quantized = quantize

        self.timer = Thread(target=self.tick)
        self.next_trigger = None

        self.tform = "%Y/%m/%d %H:%M:%S %f %Z%z"

        self._closing = Event()

    def tick(self):

        if self.quantized:
            secs = time.time()

            o = self.offset.seconds
            d = self.duration.seconds

            secs = int((secs - o) / d) * d + o  # quantize
            secs += d  # get next occurrence

            self.next_trigger = datetime.fromtimestamp(secs)
        else:
            self.next_trigger = datetime.utcnow() + self.duration

        if self.run_on_start:
            self.trigger(datetime.utcnow())

        while True:
            sleep_time = (self.next_trigger - datetime.utcnow()).total_seconds()
            self._closing.wait(sleep_time)

            if self._closing.is_set():
                break

            self.trigger(self.next_trigger)

        print("TRIGGER: Timer thread closed")

    def trigger(self, trigger_time):
        # next_trigger is actually current_trigger at this point
        self._invoke(trigger_time)
        print("TRIGGER: Invoked with time @ " + datetime.strftime(trigger_time, self.tform))

        # while loop prevents things from getting backed up if there are problems
        while self.next_trigger <= datetime.utcnow():
            self.next_trigger += self.duration

        print("TRIGGER: Next trigger scheduled for " + datetime.strftime(self.next_trigger, self.tform))

    def prime(self):
        self.timer.start()

    def close(self):
        self._closing.set()
        print("TRIGGER: Closing")
        self.timer.join()
