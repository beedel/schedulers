from des import SchedulerDES
from process import ProcessStates
from event import EventTypes, Event


# Algorithm implementation of the First Come, First Serve scheduler 
class FCFS(SchedulerDES):

    # Pick the first process in the queue (it has already been picked by des.py, so just return a process using the event's id)
    def scheduler_func(self, cur_event):
        return self.processes[cur_event.process_id]


    # Run the process until it's done, return event of type PROC_CPU_DONE
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        # Run the process 
        cur_process.run_for(cur_process.service_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        # Return event of type PROC_CPU_DONE
        return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE, event_time = cur_process.departure_time)


# Algorithm implementation of the Shortest Job First scheduler 
class SJF(SchedulerDES):

    # Select the shortest job from ones that are READY
    def scheduler_func(self, cur_event):
        chosen_process = None

        for process in self.processes:
            # Only examine ones that are READY
            if (process.process_state == ProcessStates.READY):
                # Select the one with the shortest service time
                if (chosen_process is None) or (process.service_time < chosen_process.service_time):
                    chosen_process = process

        return chosen_process


    # Run the process until it's done
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        # Run the process 
        cur_process.run_for(cur_process.service_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        # Return event of type PROC_CPU_DONE
        return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE, event_time = cur_process.departure_time)


# Algorithm implementation of the Round Robin scheduler
class RR(SchedulerDES):

    # Pick the first process in the queue
    def scheduler_func(self, cur_event):
        return self.processes[cur_event.process_id]


    # Run the process for quantum (already set) time, it is then added to the end of the queue by des.py
    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        # Run the process 
        cur_process.run_for(self.quantum, self.time)

        # Check if the process has finished, return an event accordingly
        if cur_process.remaining_time > 0:
            cur_process.process_state = ProcessStates.READY
            # Return event of type PROC_CPU_REQ
            return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_REQ, event_time = self.time + self.quantum)
        else:
            cur_process.process_state = ProcessStates.TERMINATED
            # Return event of type PROC_CPU_DONE
            return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE, event_time = cur_process.departure_time)


# Algorithm implementation of the Shortest Remaining Time First scheduler 
class SRTF(SchedulerDES):

    # Select the process with the shortest remaining time from ones that are READY
    def scheduler_func(self, cur_event):
        chosen_process = None

        for process in self.processes:
            # Only examine ones that are READY
            if (process.process_state == ProcessStates.READY):
                # Select the one with the shortest remaining time
                # BUT keep the currently running process if its remaining time is smaller that the context switch time
                if (chosen_process is None) or ((process.remaining_time < chosen_process.remaining_time) and (chosen_process.remaining_time > self.context_switch_time)):
                    chosen_process = process

        return chosen_process


    # Run it till the time of the next event
    def dispatcher_func(self, cur_process):

        # Calculate the time till next event
        run_for = self.next_event_time() - self.time

        cur_process.process_state = ProcessStates.RUNNING
        # Run the process 
        cur_process.run_for(run_for, self.time)

        # Check if the process has finished, return an event accordingly
        if cur_process.remaining_time > 0:
            cur_process.process_state = ProcessStates.READY
            # Return event of type PROC_CPU_REQ
            return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_REQ, event_time = self.time + run_for)
        else:
            cur_process.process_state = ProcessStates.TERMINATED
            # Return event of type PROC_CPU_DONE
            return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE, event_time = cur_process.departure_time)
    

