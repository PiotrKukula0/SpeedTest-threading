import tkinter as tk
from tkinter import ttk
from threading import Thread
import speedtest
from queue import Queue
import time


def test_internet_speed(speed_queue):
    while True:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1000000
        upload_speed = st.upload() / 1000000
        ping_latency = st.results.ping
        speed_queue.put((download_speed, upload_speed, ping_latency))
        time.sleep(2)


def start_speed_test():
    global speed_thread
    speed_thread = Thread(target=test_internet_speed,
                          args=(speed_queue,), daemon=True)
    speed_thread.start()


def update_labels():
    if not speed_queue.empty():
        download_speed, upload_speed, ping_latency = speed_queue.get()
        download_speed_label.config(text=f"{download_speed:.2f} Mbps")
        download_speed_progress["value"] = download_speed
        upload_speed_label.config(text=f"{upload_speed:.2f} Mbps")
        upload_speed_progress["value"] = upload_speed
        ping_latency_label.config(text=f"{ping_latency:.2f} ms")
    root.after(100, update_labels)


root = tk.Tk()
root.title("Test prędkości internetu")

speed_queue = Queue()

download_speed_label = tk.Label(root, text="0.00 Mbps")
download_speed_label.pack()

download_speed_progress = ttk.Progressbar(
    root, orient="horizontal", length=200, mode="determinate")
download_speed_progress.pack()

upload_speed_label = tk.Label(root, text="0.00 Mbps")
upload_speed_label.pack()

upload_speed_progress = ttk.Progressbar(
    root, orient="horizontal", length=200, mode="determinate")
upload_speed_progress.pack()

ping_latency_label = tk.Label(root, text="0.00 ms")
ping_latency_label.pack()

start_button = tk.Button(root, text="Rozpocznij test",
                         command=start_speed_test)
start_button.pack()

root.after(100, update_labels)
root.mainloop()
