import tkinter as tk
from tkinter import messagebox, scrolledtext
import serial
import threading
import time

# COM port and baud rate configuration
COM_PORT = "COM6"
BAUD_RATE = 115200

# Global variables
setpoints = []
time_interval = 1  # Time interval in seconds
is_running = False  # Control flag to manage sending process

# Connect to COM port
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
except serial.SerialException:
    messagebox.showerror("Error", f"Cannot connect to {COM_PORT}")
    exit()

# Function to send setpoints sequentially
def send_setpoints():
    global is_running
    is_running = True
    while is_running and setpoints:
        for value in setpoints:
            if not is_running:  # Check if stopped
                break
            message = f"{value}y"
            ser.write(message.encode())
            log_message(f"MyControl: {value}", "blue")  # Display only the value
            time.sleep(time_interval)
    stop_control()

# Function to update setpoints array and time interval
def start_sending():
    global setpoints, time_interval, is_running
    if is_running:
        messagebox.showwarning("Warning", "Already running, please stop before restarting.")
        return

    # Retrieve setpoints and time interval from the GUI
    try:
        setpoints = list(map(int, setpoints_entry.get().split()))
        time_interval = float(interval_entry.get())
        if time_interval <= 0:
            raise ValueError("Time interval must be greater than 0.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid values for setpoints and time interval.")
        return

    # Start sending setpoints in a new thread
    threading.Thread(target=send_setpoints).start()

# Function to stop sending setpoints
def stop_control():
    global is_running
    is_running = False
    stop_message = "nnn"
    ser.write(stop_message.encode())
    log_message("MyControl: Stop Control", "red")

# Function to log messages in the Text box
def log_message(message, color="black"):
    output_textbox.config(state=tk.NORMAL)
    output_textbox.insert(tk.END, message + "\n")
    output_textbox.tag_add("color", "end-2l", "end-1l")
    output_textbox.tag_config("color", foreground=color)
    output_textbox.see(tk.END)  # Scroll to the end
    output_textbox.config(state=tk.DISABLED)

# Function to read data from COM port and display
def read_from_com():
    while True:
        if ser.in_waiting:
            received_message = ser.readline().decode().strip()
            log_message(f"STM32F4: {received_message}", "green")

# Create GUI
root = tk.Tk()
root.title("Setpoint Sender")
root.configure(bg="#f0f0f0")

# Setpoints entry field
tk.Label(root, text="Setpoints:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
setpoints_entry = tk.Entry(root, width=30)
setpoints_entry.grid(row=0, column=1, padx=10, pady=5)
setpoints_entry.insert(0, "")

# Time interval entry field
tk.Label(root, text="Time interval between sends (T seconds):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
interval_entry = tk.Entry(root, width=10)
interval_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
interval_entry.insert(0, "")  # Default is 1 second

# Start button
start_button = tk.Button(root, text="Start", command=start_sending, bg="#4CAF50", fg="white", width=10)
start_button.grid(row=2, column=0, padx=10, pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_control, bg="#f44336", fg="white", width=10)
stop_button.grid(row=2, column=1, padx=10, pady=10)

# Text box to display sent and received messages
output_textbox = scrolledtext.ScrolledText(root, width=50, height=15, state=tk.DISABLED, wrap=tk.WORD, font=("Arial", 10))
output_textbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start a thread to read data from COM
threading.Thread(target=read_from_com, daemon=True).start()

# Display the GUI
root.mainloop()

# Close the COM port on exit
ser.close()
