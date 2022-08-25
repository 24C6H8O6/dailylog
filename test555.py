from multiprocessing import Process
import time

def cnt_number(data):
    for i in range(data):
        print(i)
        time.sleep(0.5)
        


pro1 = Process(args=(1,10), target=cnt_number)
#pro2 = Process(args=(100, 110), target=cnt_number)

pro1.start()
#pro2.start()

pro1.join()
#pro2.join()