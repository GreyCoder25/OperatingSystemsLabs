
class Process:

    def __init__(self, perf_time, appear_time):

        self.perf_time = perf_time
        self.wait_time = 0
        self.time_to_finish = perf_time
        self.appear_time = appear_time
        self.start_perf_time = -1
        self.finish_time = -1

    def wait(self):

        self.wait_time += 1

    def execute(self):

        self.time_to_finish -= 1

