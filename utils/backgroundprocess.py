
"""
    A BackgroundProcess is a long-running, cancellable thread that can
    report progress and done events.

    This object can be used by:
    1) subclassing and overriding 'doWork' method
    2) passing a callable as the "work" parameter to the constructor
    
"""

__author__ = "Phillip Piper"
__date__ = "19 April 2008"
__version__ = "0.1"

import threading

class BackgroundProcess(object):

    def __init__(self, work=None, progress=None, done=None):
        """
        Initialize a background process.

        Parameters:
            work
                A callable that accepts a single parameter: the process itself. This
                callable executes the long running process. This should periodically check
                to see if the process has been cancelled (using the isCancelled method),
                as well as reporting its progress (using the notifyProgress method). If
                this is None, the process will do nothing. Subclasses that override the
                "doWork" method should not use this parameter
            progress
                A callable that accepts two parameters: the process itself, and a value
                given to the notifyProgress method (often an int representing percentage done).
            done
                A callable that accepts a single parameter: the process itself. If not None,
                this is called when the process finishes.
        """
        self.thread = None
        self.abortEvent = threading.Event()
        self.workCallback = work
        self.progressCallback = progress
        self.doneCallback = done

    #----------------------------------------------------------------------------
    # Commands

    def run(self):
        """
        Run the process synchronously
        """
        self.runAsync()
        self.wait()

    def runAsync(self):
        """
        Start a process to run asynchronously
        """
        if self.isRunning():
            return

        self.abortEvent.clear()
        self.thread = threading.Thread(target=self._worker)
        self.thread.setDaemon(True)
        self.thread.start()

    def wait(self):
        """
        Wait until the process is finished
        """
        self.thread.join()

    def cancel(self):
        """
        Cancel the process
        """
        self.abortEvent.set()

    def isCancelled(self):
        """
        Has this process been cancelled?
        """
        return self.abortEvent.isSet()

    def isRunning(self):
        """
        Return true if the process is still running
        """
        return self.thread is not None and self.thread.isAlive()

    #----------------------------------------------------------------------------
    # Implementation

    def _worker(self):
        """
        This is the actual thread process
        """
        self.doWork()
        self.reportDone()

    def doWork(self):
        """
        Do the real work of the thread.

        Subclasses should override this method to perform the long-running task.
        That task should call "isCancelled" regularly and "reportProgress" periodically.
        """
        if self.workCallback:
            self.workCallback(self)

    def reportProgress(self, value):
        """
        Report that some progress has been made
        """
        time.sleep(0.001) # Force a switch to other threads
        if self.progressCallback and not self.isCancelled():
            self.progressCallback(self, value)

    def reportDone(self):
        """
        Report that the thread has finished
        """
        if self.doneCallback:
            self.doneCallback(self)
