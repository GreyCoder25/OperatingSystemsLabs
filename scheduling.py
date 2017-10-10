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

while True:
    if rnd.random() < NEW_PROCESS_PROBABILITY:
        if rnd.random() < NEW_PACKAGE_PROCESS_PROBABILITY:
            package_processes_queue.append(pr.Process(5 + rnd.randint(1, 5)))
            new_package_process = True
        else:
            interactive_processes_queue.append(pr.Process(10 + rnd.randint(1, 5)))

    if current_queue == 'i':
        for index, proc in enumerate(interactive_processes_queue):
            if index == current_interactive_process:
                proc.execute()
                if proc.time_to_finish == 0:
                    interactive_processes_queue.pop(index)
                    interactive_process_finished = True
            else:
                proc.wait()
        proc_time += 1

        if proc_time == QUANTUM:
            if interactive_processes_queue and (not interactive_process_finished):
                current_interactive_process = (current_interactive_process + 1) % len(interactive_processes_queue)
            elif interactive_process_finished and current_interactive_process == len(interactive_processes_queue):
                current_interactive_process = 0
            proc_time = 0

        if interactive_process_finished:
            interactive_process_finished = False

        current_interactive_time += 1
        if current_interactive_time == INTERACTIVE_TIME:
            current_interactive_time = 0
            current_queue = 'p'
    elif current_queue == 'p':
        if new_package_process:
            if package_processes_queue[-1].time_to_finish < package_processes_queue[current_package_process].time_to_finish:
                current_package_process = len(package_processes_queue) - 1
            new_package_process = False

        for index, proc in enumerate(package_processes_queue):
            if index == current_package_process:
                proc.execute()
                if proc.time_to_finish == 0:
                    package_processes_queue.pop(index)
                    package_process_finished = True
            else:
                proc.wait()
        if package_process_finished:
            if package_processes_queue:
                current_package_process = package_processes_queue.index(min(package_processes_queue,
                                                                            key=lambda p: p.time_to_finish))

        current_package_time += 1
        if current_package_time >= PACKAGE_TIME and package_process_finished:
            current_package_time = 0
            package_process_finished = False
            current_queue = 'i'

    current_time += 1
    if current_time == TIME:
        break



