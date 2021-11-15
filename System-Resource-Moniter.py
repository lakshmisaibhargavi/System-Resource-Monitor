import tkinter as tk
from tkinter import *
from tkinter import ttk
import psutil as ps
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import platform
#import wmi

window = tk.Tk()
window.title("System Monitor")
window.geometry("500x400")
tController = ttk.Notebook(window)
tab1 = ttk.Frame(tController)
tab3 = ttk.Frame(tController)
tab4 = ttk.Frame(tController)
tab5 = ttk.Frame(tController)
tab6 = ttk.Frame(tController)

frameChartMemory = ttk.Frame(tab3)
frameChartMemory.grid(column=0, row=5, sticky="nw")

frameChartDisk = tk.Frame(tab5)
frameChartDisk.grid(column=0, row=5)
tController.add(tab1, text="Info")
tController.add(tab3, text="Memory")
tController.add(tab4, text="Network")
tController.add(tab5, text="Disk")
tController.add(tab6, text="Process - PID")
tController.pack(fill="both")
ttk.Label(tab1, text="").grid(column=0, row=0)


def refresh():

    # User Details
    # User Name Starts
    ttk.Label(tab1, text="User Name : {}".format(ps.Process().username())).grid(
        column=0, row=1, sticky="nw")
    # OS Library
    ttk.Label(tab1, text="Computer Network Name : {}".format(platform.node())).grid(
        column=0, row=2, sticky="nw")
    ttk.Label(tab1, text="Machine Type : {}".format(platform.machine())).grid(
        column=0, row=3, sticky="nw")
    ttk.Label(tab1, text="Operating System : {}".format(platform.system())).grid(
        column=0, row=4, sticky="nw")
    ttk.Label(tab1, text="Operating System Version : {}".format(platform.version())).grid(
        column=0, row=5, sticky="nw")
    ttk.Label(tab1, text="Operating System Release : {}".format(platform.release())).grid(
        column=0, row=6, sticky="nw")
    ttk.Label(tab1, text="Processor Type : {}".format(platform.processor())).grid(
        column=0, row=7, sticky="nw")
    ttk.Label(tab1, text="Current Process Id : {}".format(os.getpid())).grid(
        column=0, row=8, sticky="nw")
    # USER INFO DONE
    totalMem = ps.virtual_memory()[0]
    availMem = ps.virtual_memory()[1]
    usedMem = ps.virtual_memory()[3]
    byteSent = ps.net_io_counters()[0]
    byteRec = ps.net_io_counters()[1]
    pacSent = ps.net_io_counters()[2]
    pacRec = ps.net_io_counters()[3]
    totalDisk = ps.disk_usage('/')[0]
    usedDisk = ps.disk_usage('/')[1]
    freeDisk = ps.disk_usage('/')[2]
    # Memory Start
    ttk.Label(tab3, text="Total: {} GB".format(
        round(totalMem/(1024*1024*1024), 2))).grid(column=0, row=0, sticky="nw")
    ttk.Label(tab3, text="Available: {} GB".format(
        round(availMem/(1024*1024*1024), 2))).grid(column=0, row=2, sticky="nw")
    ttk.Label(tab3, text="Used: {} GB".format(
        round(usedMem/(1024*1024*1024), 2))).grid(column=0, row=4, sticky="nw")
    # Memory end
    # Network Start
    ttk.Label(tab4, text="Bytes Sent: {} bytes".format(
        byteSent)).grid(column=0, row=0, sticky="nw")
    ttk.Label(tab4, text="Bytes Recieved: {} bytes".format(
        byteRec)).grid(column=0, row=2, sticky="nw")
    ttk.Label(tab4, text="Packets Sent: {} ".format(
        pacSent)).grid(column=0, row=3, sticky="nw")
    ttk.Label(tab4, text="Packets Recieved: {} ".format(
        pacRec)).grid(column=0, row=4, sticky="nw")
    # Network End
    # Disk Start
    ttk.Label(tab5, text="Total: {} GB".format(
        round(totalDisk/(1024*1024*1024), 2))).grid(column=0, row=0, sticky="nw")
    ttk.Label(tab5, text="Available: {} GB".format(
        round(freeDisk/(1024*1024*1024), 2))).grid(column=0, row=2, sticky="nw")
    ttk.Label(tab5, text="Used: {} GB".format(
        round(usedDisk/(1024*1024*1024), 2))).grid(column=0, row=4, sticky="nw")
    # Disk Ends
    # Calls the functions for every 1000 Milli-seconds so that the data would be realtime.
    window.after(1000, refresh)


# Processes Start
scrollbar = Scrollbar(tab6)
scrollbar.pack(side=RIGHT,
               fill=BOTH)
mylist = Listbox(tab6,
                 yscrollcommand=scrollbar.set)
#process = os.popen('wmic process get description, processid').read()

for process in ps.process_iter():
    mylist.insert(END, str(process.name()) + "      " + str(process.pid))
mylist.pack(side=LEFT, fill=BOTH, expand=2)
scrollbar.config(command=mylist.yview)
# Processes end

# pie chart for memory tab
fig = Figure()
ax = fig.add_subplot(111)
memoryChartLabels = ["Used", "Available"]
memoryChartValues = [ps.virtual_memory()[3], ps.virtual_memory()[1]]
ax.pie(memoryChartValues, radius=0.5,
       labels=memoryChartLabels, autopct='%0.2f%%')
chart1 = FigureCanvasTkAgg(fig, frameChartMemory)
chart1.get_tk_widget().grid(row=5, column=0, sticky="nw")
# pie chart for memory tab code ends here

# pie chart for disk tab
fig = Figure()
ax = fig.add_subplot(111)
diskChartLabels = ["Used", "Available"]
diskChartValues = [ps.disk_usage('/')[1], ps.disk_usage('/')[2]]
ax.pie(diskChartValues, radius=0.5, labels=diskChartLabels, autopct='%0.2f%%')
chart1 = FigureCanvasTkAgg(fig, frameChartDisk)
chart1.get_tk_widget().grid(row=5, column=0)
# pie chart for disk tab code ends here


refresh()
window.mainloop()
