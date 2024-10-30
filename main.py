import math
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# x' = x/a, k'n = n, E'n  = En/E1 = n^2, t' = (E1/h_bar) t

root = tk.Tk()
root.state('zoomed')
root.attributes('-topmost', True)
root.bind("<Escape>", lambda e: root.destroy())


eigen_functions_count = 100
Cn = []
En = []
frequencies = [i for i in range(1, 100+1)]
input_x = np.arange(start=-1 / 2, stop=1 / 2, step=1e-3, dtype=float).tolist()
time = np.arange(start=0, stop=2 * math.pi + 0.5, step=1e-2, dtype=float).tolist()
x_ticks = np.arange(start=-0.5, stop=0.5 + 1e-3, step=0.1).tolist()

max_psi_value = 0

for i in range(20):
    time.insert(0, 0)


def func0(x, number: int):
    if number % 2 == 0:
        return math.sqrt(2) * math.sin((number * math.pi) * x)
    else:
        return math.sqrt(2) * math.cos((number * math.pi) * x)


def func1(x):
    if x < 0:
        return math.sqrt(3) + (2 * math.sqrt(3) * x)
    else:
        return math.sqrt(3) - (2 * math.sqrt(3) * x)


def func2(x):
    if x < 0:
        return math.sqrt(3) + (2 * math.sqrt(3) * x)
    else:
        return -math.sqrt(3) + (2 * math.sqrt(3) * x)


def func3(x, a, b):
    if a <= x <= b:
        return math.sqrt(1 / (b - a))
    else:
        return 0


def integrate(input_value: list, output_value: list, mode: int, delta):
    result = 0
    for i in range(len(input_value)):
        if mode % 2 == 0:  # sin eigen
            result += math.sqrt(2) * math.sin((mode * math.pi) * input_value[i]) * output_value[i]
        else:  # cosine eigen
            result += math.sqrt(2) * math.cos((mode * math.pi) * input_value[i]) * output_value[i]

    return result * delta


def normalize_coefs():
    summation = 0
    for c in Cn:
        summation += c ** 2

    summation = math.sqrt(summation)
    if summation == 0:
        return

    for j in range(len(Cn)):
        Cn[j] = Cn[j] / summation


def Psi_n(x: float, t: float, mode: int) -> np.complex64:
    if mode % 2 == 0:
        return Cn[mode - 1] * math.sqrt(2) * math.sin((math.pi * mode) * x) * np.exp((-1j) * (t * En[mode - 1]))
    else:
        return Cn[mode - 1] * math.sqrt(2) * math.cos((math.pi * mode) * x) * np.exp((-1j) * (t * En[mode - 1]))


def animate_1(index):
    current_time = time[index]
    psi_t = np.empty(len(input_x), dtype=np.complex64)
    for j in range(len(input_x)):
        temp = 0 + 0j
        for mode in range(1, len(Cn) + 1):
            temp += Psi_n(input_x[j], current_time, mode)

        psi_t[j] = temp

    line_real.set_ydata(psi_t.real.tolist())
    line_img.set_ydata(psi_t.imag.tolist())
    line_conj.set_ydata((psi_t * psi_t.conj()).real.tolist())

    ax5.set_title(fr"$\Psi*(x, t)\Psi(x, t)$  t = {current_time:.2f}")
    return line_real, line_img, line_conj


def animate_0(index):
    global zero_count

    if index == 0 and zero_count == 0:
        zero_count += 1
    elif index == 0 and zero_count == 1:
        zero_count += 1
        return line_real
    elif index == 0 and zero_count == 2:  # we don't need the program to run for more than 100 iterations
        exit(0)

    current_freq = frequencies[index]
    Cn.append(integrate(input_x, initial_psi, current_freq, 1.0 / len(input_x)))
    En.append(index * index)
    psi_t = np.empty(len(input_x), dtype=np.float64)
    for j in range(len(input_x)):
        temp = 0 + 0j
        for mode in range(1, len(Cn) + 1):
            temp += Psi_n(input_x[j], 0, mode)

        psi_t[j] = temp.real

    ax1.stem(range(1, len(Cn) + 1), Cn)
    line_real.set_ydata(psi_t.tolist())
    ax3.set_title(r"$\Psi_{app}(x, t)$"+f"  n = {current_freq}")
    return line_real


number = int(input("Enter the application mode you want (1 for time evolution, 0 for frequency evolution): "))
func = int(input("Enter the mode you want: "))
initial_psi = None
if func == 0:
    n = int(input("Enter the stationary number (has to be an integer): "))
    initial_psi = [func0(i, n) for i in input_x]
    max_psi_value = np.max(np.array(initial_psi))
elif func == 1:
    initial_psi = [func1(i) for i in input_x]
    max_psi_value = np.max(np.array(initial_psi))
elif func == 2:
    initial_psi = [func2(i) for i in input_x]
    max_psi_value = np.max(np.array(initial_psi))
elif func == 3:
    a = float(input("Enter a (should be between -1/2 to 1/2): "))
    b = float(input("Enter b (should be between -1/2 to 1/2 and more than a): "))
    initial_psi = [func3(i, a, b) for i in input_x]
    max_psi_value = np.max(np.array(initial_psi))

if number == 1:
    for i in range(1, eigen_functions_count + 1):
        Cn.append(integrate(input_x, initial_psi, i, 1.0 / len(input_x)))
        En.append(i * i)

    print(Cn)
    normalize_coefs()
    fig = plt.figure()
    gs = GridSpec(3, 2)
    ax1 = fig.add_subplot(gs[0, 0])  # Top left
    ax2 = fig.add_subplot(gs[0, 1])  # Top right
    ax3 = fig.add_subplot(gs[1, 0])  # Middle left
    ax4 = fig.add_subplot(gs[1, 1])  # Middle right
    ax5 = fig.add_subplot(gs[2, :])  # Bottom center (spanning both columns)

    # Cn
    ax1.stem(range(1, len(Cn) + 1), Cn)
    ax1.set_title("Cn Coefficients")
    ax1.set_ylabel("Cn")
    ax1.set_xlabel("n")

    # initial psi
    ax2.plot(input_x, initial_psi, color="red")
    ax2.set_xlim(-0.5, 0.5)
    ax2.set_ylim(-max_psi_value - 1, max_psi_value + 1)
    ax2.set_title(r"Initial $\Psi$")
    ax2.set_ylabel(r"$\Psi(x, 0)$")
    ax2.set_xticks(x_ticks)
    ax2.grid(True)

    # real part
    line_real, = ax3.plot(input_x, initial_psi, color='green')
    ax3.set_xlim(-0.5, 0.5)
    ax3.set_ylim(-max_psi_value - 1, max_psi_value + 1)
    ax3.set_title(r"$Re\{\Psi(x, t)\}$")
    ax3.set_ylabel(r"$\Psi(x, t)$")
    ax3.set_xticks(x_ticks)
    ax3.grid(True)

    # imaginary part
    line_img, = ax4.plot(input_x, [0 for i in input_x], color='orange')
    ax4.set_xlim(-0.5, 0.5)
    ax4.set_ylim(-max_psi_value - 1, max_psi_value + 1)
    ax4.set_title(r"$Img\{\Psi(x, t)\}$")
    ax4.set_ylabel(r"$\Psi(x, t)$")
    ax4.set_xticks(x_ticks)
    ax4.grid(True)

    line_conj, = ax5.plot(input_x, [0 for i in range(len(input_x))], color='blue')
    ax5.set_xlim(-0.5, 0.5)
    ax5.set_ylim(0, max_psi_value ** 2 + 1)
    ax5.set_title(r"$\Psi*(x, t)\Psi(x, t)$  t = 0.0")
    ax5.set_ylabel(r"$\Psi*(x, t)\Psi(x, t)$")
    ax5.set_xticks(x_ticks)
    ax5.grid(True)

    print(Cn[0])
    ani = FuncAnimation(fig, animate_1, frames=len(time), interval=20)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

else:
    zero_count = 0  # because the FuncAnimation calls the animate_0 with two zero input values :/
    fig = plt.figure()
    gs = GridSpec(3, 1)
    ax1 = fig.add_subplot(gs[0, 0])  # Top left
    ax2 = fig.add_subplot(gs[1, 0])  # Top right
    ax3 = fig.add_subplot(gs[2, 0])  # Middle left

    # Cn
    ax1.stem(range(1), [0])
    ax1.set_xlim(0, 100)
    ax1.set_title("Cn Coefficients")
    ax1.set_ylabel("Cn")
    ax1.set_xlabel("n")

    # initial psi
    ax2.plot(input_x, initial_psi, color="red")
    ax2.set_xlim(-0.5, 0.5)
    ax2.set_ylim(-max_psi_value - 1, max_psi_value + 1)
    ax2.set_title(r"Initial $\Psi$")
    ax2.set_ylabel(r"$\Psi(x, 0)$")
    ax2.set_xticks(x_ticks)
    ax2.grid(True)

    # real part
    line_real, = ax3.plot(input_x, initial_psi, color='green')
    ax3.set_xlim(-0.5, 0.5)
    ax3.set_ylim(-max_psi_value - 1, max_psi_value + 1)
    ax3.set_title(r"$\Psi_{app}(x, t)$")
    ax3.set_ylabel(r"$\Psi_{app}(x, t)$")
    ax3.set_xticks(x_ticks)
    ax3.grid(True)

    ani = FuncAnimation(fig, animate_0, frames=len(frequencies), interval=0)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

