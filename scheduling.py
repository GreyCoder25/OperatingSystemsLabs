import process as pr
import random as rnd


TIME = 50                            # need to be a multiple of one hundred
PACKAGE_TIME = 2
INTERACTIVE_TIME = 8
NEW_PROCESS_PROBABILITY = 0.2
NEW_PACKAGE_PROCESS_PROBABILITY = 0.3
NEW_INTERACTIVE_PROCESS_PROBABILITY = 1 - NEW_PACKAGE_PROCESS_PROBABILITY
QUANTUM = 2

package_processes_queue = []
interactive_processes_queue = []

current_time = 0
proc_time = 0
current_package_time = 0
current_interactive_time = 0
current_queue = 'i'

current_interactive_process = 0
current_package_process = 0
new_package_process = False
interactive_process_finished = False
package_process_finished = False

completed_processes = []


def print_info(current_iteration, package_queue, interactive_queue):

    print("------------------------------------------------")
    print("Iteration: %d" % current_iteration)
    print("------------------------------------------------")
    print("Interactive processes:")
    for index, proc in enumerate(interactive_queue):
        print("Process %d, time to finish: %d, waiting: %d" % (index, proc.time_to_finish, proc.wait_time))

    print("Package processes:")
    for index, proc in enumerate(package_queue):
        print("Process %d, time to finish: %d, waiting: %d" % (index, proc.time_to_finish, proc.wait_time))

    print("------------------------------------------------\n")


def print_table(completed, package, interactive):       # TODO fix ugly output

    print("Number | appear time | perf time | start time | finish time | wait time | full time")
    for index, proc in enumerate(completed + package + interactive):
        print("  %d    |   %d        |   %d            |   %d   |   %d   |   %d   |   %d   " % (index,
                                                                                 proc.appear_time, proc.perf_time,
                                                                                 proc.start_perf_time, proc.finish_time,
                                                                                 proc.wait_time,
                                                                                 proc.perf_time + proc.wait_time))


while True:
    if rnd.random() < NEW_PROCESS_PROBABILITY:
        if rnd.random() < NEW_PACKAGE_PROCESS_PROBABILITY:
            package_processes_queue.append(pr.Process(1 + rnd.randint(1, 5), current_time))
            new_package_process = True
            print("Package process %d added. Time to finish: %d" % (len(package_processes_queue) - 1,
                                                                    package_processes_queue[-1].time_to_finish))
        else:
            interactive_processes_queue.append(pr.Process(3 + rnd.randint(1, 5), current_time))
            print("Interactive process %d added. Time to finish: %d" % (len(interactive_processes_queue) - 1,
                                                                    interactive_processes_queue[-1].time_to_finish))
    finished_process_index = -1
    if current_queue == 'i':
        for index, proc in enumerate(interactive_processes_queue):
            if index == current_interactive_process:
                if proc.time_to_finish == proc.perf_time:
                    proc.start_perf_time = current_time
                proc.execute()
                if proc.time_to_finish == 0:
                    proc.finish_time = current_time
                    interactive_process_finished = True
                    finished_process_index = index
                    print("Interactive process %d finished." % index)
                    completed_processes.append(proc)
            else:
                proc.wait()
        for proc in package_processes_queue:
            proc.wait()
        proc_time += 1

        if interactive_process_finished:
            interactive_processes_queue.pop(finished_process_index)

        if proc_time == QUANTUM:
            if interactive_processes_queue and (not interactive_process_finished):
                current_interactive_process = (current_interactive_process + 1) % len(interactive_processes_queue)
            elif interactive_process_finished and current_interactive_process == len(interactive_processes_queue):
                current_interactive_process = 0
            proc_time = 0

        if interactive_process_finished:
            interactive_process_finished = False
            proc_time = 0

        current_interactive_time += 1
        if current_interactive_time == INTERACTIVE_TIME:
            current_interactive_time = 0
            current_queue = 'p'
    elif current_queue == 'p':
        if new_package_process:
            if package_processes_queue[-1].time_to_finish < package_processes_queue[current_package_process].time_to_finish:
                current_package_process = len(package_processes_queue) - 1
            new_package_process = False

        finished_process_index = -1
        for index, proc in enumerate(package_processes_queue):
            if index == current_package_process:
                if proc.time_to_finish == proc.perf_time:
                    proc.start_perf_time = current_time
                proc.execute()
                if proc.time_to_finish == 0:
                    proc.finish_time = current_time
                    package_process_finished = True
                    finished_process_index = index
                    print("Package process %d finished." % index)
                    completed_processes.append(proc)
            else:
                proc.wait()
        for proc in interactive_processes_queue:
            proc.wait()

        if package_process_finished:
            package_processes_queue.pop(finished_process_index)
            if package_processes_queue:
                current_package_process = package_processes_queue.index(min(package_processes_queue,
                                                                            key=lambda p: p.time_to_finish))

        current_package_time += 1
        if current_package_time >= PACKAGE_TIME and (package_process_finished or (not package_processes_queue)):
            current_package_time = 0
            package_process_finished = False
            current_queue = 'i'

    current_time += 1
    if current_time == TIME:
        break

    print_info(current_time, package_processes_queue, interactive_processes_queue)

print_table(completed_processes, package_processes_queue, interactive_processes_queue)




