import os, time 
from multiprocessing import Process
 
def doubler(number):
    while(1):
        result = number * 2
        proc = os.getpid()
        print('{0} doubled to {1} by process id: {2}'.format(number, result, proc))
        time.sleep(1)
 
if __name__ == '__main__':
    proc = Process(target=doubler, args=(5,))
    proc.start()

    # Terminate processes
    time.sleep(3)
    proc.terminate() 
    #proc.join()

    time.sleep(1)
    proc = Process(target=doubler, args=(5,))
    proc.start()
    time.sleep(3)
    proc.terminate()
