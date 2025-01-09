import tkinter as tk
from tkinter import messagebox
import psutil
import sqlite3
import time
import threading

def create_database():
    conn = sqlite3.connect("system_metrics.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            ram_usage REAL,
            disk_usage REAL
        )
    """)
    conn.commit()
    conn.close()

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    return cpu_usage, ram_usage, disk_usage

def log_data():
    global logging_active
    conn = sqlite3.connect("system_metrics.db")
    cursor = conn.cursor()
    while logging_active:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cpu, ram, disk = get_system_metrics()
        cursor.execute("""
            INSERT INTO metrics (timestamp, cpu_usage, ram_usage, disk_usage)
            VALUES (?, ?, ?, ?)
        """, (timestamp, cpu, ram, disk))
        conn.commit()
        time.sleep(update_interval.get())
    conn.close()

def update_labels():
    cpu, ram, disk = get_system_metrics()
    cpu_label.config(text=f"CPU Usage: {cpu}%")
    ram_label.config(text=f"RAM Usage: {ram}%")
    disk_label.config(text=f"Disk Usage: {disk}%")
    if logging_active:
        elapsed_time = int(time.time() - start_time)
        timer_label.config(text=f"Recording time: {elapsed_time // 3600:02}:{(elapsed_time % 3600) // 60:02}:{elapsed_time % 60:02}")
    root.after(1000, update_labels)

def start_logging():
    global logging_active, start_time
    if not logging_active:
        logging_active = True
        start_time = time.time()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        threading.Thread(target=log_data, daemon=True).start()

def stop_logging():
    global logging_active
    logging_active = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def exit_program():
    if logging_active:
        stop_logging()
    root.destroy()

def main():
    global root, cpu_label, ram_label, disk_label, timer_label, interval_label, interval_entry, start_button, stop_button, logging_active, start_time, update_interval

    root = tk.Tk()
    root.title("System Monitor")
    root.geometry("300x250")

    logging_active = False
    start_time = 0
    update_interval = tk.IntVar(value=1)

    cpu_label = tk.Label(root, text="CPU Usage: N/A")
    cpu_label.pack()

    ram_label = tk.Label(root, text="RAM Usage: N/A")
    ram_label.pack()

    disk_label = tk.Label(root, text="Disk Usage: N/A")
    disk_label.pack()

    timer_label = tk.Label(root, text="Recording time: 00:00:00")
    timer_label.pack()

    interval_label = tk.Label(root, text="Update Interval (seconds):")
    interval_label.pack()

    interval_entry = tk.Entry(root, textvariable=update_interval)
    interval_entry.pack()

    start_button = tk.Button(root, text="Начать запись", command=start_logging)
    start_button.pack()

    stop_button = tk.Button(root, text="Остановить запись", command=stop_logging, state=tk.DISABLED)
    stop_button.pack()

    exit_button = tk.Button(root, text="Выход", command=exit_program)
    exit_button.pack()

    create_database()
    update_labels()
    root.mainloop()

if __name__ == '__main__':
    main()
