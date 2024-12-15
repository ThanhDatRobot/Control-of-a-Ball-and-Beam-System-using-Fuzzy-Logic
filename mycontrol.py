import tkinter as tk
from tkinter import messagebox, scrolledtext
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading
import time

# Cấu hình cổng COM và tốc độ baud
COM_PORT = "COM6"
BAUD_RATE = 115200

# Các biến toàn cục
setpoints = []  # Mảng lưu giá trị setpoint
time_interval = 1  # Khoảng thời gian giữa các lần gửi (giây)
is_running = False  # Cờ kiểm soát trạng thái gửi
received_values = []  # Lưu giá trị nhận được để vẽ đồ thị
timestamps = []  # Lưu thời điểm nhận giá trị để vẽ đồ thị

# Kết nối đến cổng COM
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
except serial.SerialException:
    messagebox.showerror("Error", f"Không thể kết nối tới {COM_PORT}")
    exit()

# Hàm gửi lần lượt các giá trị setpoint
# Trong hàm send_setpoints:
def send_setpoints():
    global is_running
    is_running = True
    while is_running and setpoints:
        for value in setpoints:
            if not is_running:  # Kiểm tra nếu dừng
                break
            message = f"{value}y"  # Chuỗi gửi đi
            ser.write(message.encode())  # Gửi qua cổng COM
            log_message(f"MyControl: {value}", "blue")  # Hiển thị giá trị
            update_plot(value, setpoint_value=value)  # Truyền giá trị setpoint vào update_plot
            time.sleep(time_interval)  # Dừng theo khoảng thời gian
    stop_control()


# Hàm khởi động quá trình gửi
def start_sending():
    global setpoints, time_interval, is_running
    if is_running:
        messagebox.showwarning("Warning", "Đang chạy, hãy dừng trước khi khởi động lại.")
        return

    # Lấy giá trị setpoint và khoảng thời gian từ giao diện
    try:
        setpoints = list(map(int, setpoints_entry.get().split()))
        time_interval = float(interval_entry.get())
        if time_interval <= 0:
            raise ValueError("Khoảng thời gian phải lớn hơn 0.")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập giá trị hợp lệ.")
        return

    # Khởi động luồng gửi setpoint
    threading.Thread(target=send_setpoints).start()

# Hàm dừng quá trình gửi
def stop_control():
    global is_running
    is_running = False
    stop_message = "nnn"  # Chuỗi thông báo dừng
    ser.write(stop_message.encode())  # Gửi qua cổng COM
    log_message("MyControl: Stop Control", "red")

# Hàm ghi thông báo vào hộp văn bản
def log_message(message, color="black"):
    output_textbox.config(state=tk.NORMAL)
    output_textbox.insert(tk.END, message + "\n")
    output_textbox.tag_add("color", "end-2l", "end-1l")
    output_textbox.tag_config("color", foreground=color)
    output_textbox.see(tk.END)  # Cuộn xuống cuối
    output_textbox.config(state=tk.DISABLED)

# Hàm cập nhật đồ thị
# Biến toàn cục để lưu giá trị setpoint
global_setpoint = None

def update_plot(value, setpoint_value=None):
    global received_values, timestamps, global_setpoint
    received_values.append(value)
    timestamps.append(time.time() - start_time)
    ax.clear()

    # Cập nhật giá trị setpoint toàn cục nếu có
    if setpoint_value is not None:
        global_setpoint = setpoint_value

    # Vẽ giá trị distance theo thời gian
    ax.plot(timestamps, received_values, color="blue", label="Dis")

    # Vẽ đường màu đỏ thể hiện giá trị setpoint (nếu có setpoint đã lưu)
    if global_setpoint is not None:
        ax.axhline(global_setpoint, color="red", linestyle="--", label=f"Setpoint: {global_setpoint}")

    # Xác định phạm vi trục x (dịch chuyển khi thời gian > 100 giây)
    current_time = timestamps[-1]
    if current_time > 50:
        ax.set_xlim(current_time - 50, current_time)  # Hiển thị cửa sổ 50 giây gần nhất
    else:
        ax.set_xlim(0, 50)  # Ban đầu hiển thị từ 0 đến 50 giây

    # Cấu hình các trục và chú thích
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance")
    ax.legend()
    ax.set_ylim(0, 50)  # Giới hạn trục y từ 0 đến 50
    canvas.draw()

# Hàm đọc dữ liệu từ cổng COM
def read_from_com():
    global start_time
    start_time = time.time()
    while True:
        if ser.in_waiting:
            try:
                received_message = ser.readline().decode().strip()  # Đọc và giải mã dữ liệu
                if received_message.startswith("Dis:"):
                    value = float(received_message.split(":")[1])
                    log_message(f"STM32F4: {received_message}", "green")
                    update_plot(value)  # Cập nhật đồ thị với giá trị mới
            except ValueError:
                pass  # Bỏ qua lỗi nếu dữ liệu không hợp lệ

# Tạo giao diện GUI
root = tk.Tk()
root.title("Setpoint Sender")
root.configure(bg="#f0f0f0")

# Trường nhập setpoint
tk.Label(root, text="Setpoints:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
setpoints_entry = tk.Entry(root, width=30)
setpoints_entry.grid(row=0, column=1, padx=10, pady=5)
setpoints_entry.insert(0, "")

# Trường nhập khoảng thời gian
tk.Label(root, text="Khoảng thời gian giữa các lần gửi (T giây):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
interval_entry = tk.Entry(root, width=10)
interval_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
interval_entry.insert(0, "")  # Mặc định là 1 giây

# Nút bắt đầu
start_button = tk.Button(root, text="Start", command=start_sending, bg="#4CAF50", fg="white", width=10)
start_button.grid(row=2, column=0, padx=10, pady=10)

# Nút dừng
stop_button = tk.Button(root, text="Stop", command=stop_control, bg="#f44336", fg="white", width=10)
stop_button.grid(row=2, column=1, padx=10, pady=10)

# Hộp văn bản hiển thị thông báo
output_textbox = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED, wrap=tk.WORD, font=("Arial", 10))
output_textbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Khu vực vẽ đồ thị
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("Khoảng cách theo thời gian")
ax.set_xlabel("Thời gian (s)")
ax.set_ylabel("Khoảng cách")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Khởi động luồng đọc dữ liệu từ cổng COM
threading.Thread(target=read_from_com, daemon=True).start()

# Hiển thị GUI
root.mainloop()

# Đóng cổng COM khi thoát
ser.close()