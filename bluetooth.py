import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np


def serial_readline(ser):
    ser_bytes = ser.readline()
    return ser_bytes

def serial_readloop(ser):
    # serial read loop
    # the data from serial need to be converted from unicode to float or other format

    # clear the serial queue
    print('start')
    ser.flushInput()
    while True:
        try:
            ser_bytes = serial_readline(ser)
            decoded_bytes = ser_bytes.decode("utf-8")
            print(decoded_bytes)
        except:
            print('Keyboard Interrupt')
            break

def serbytes2csv(ser):
    # write serbytes to csv file
    ser.flushInput()
    while True:
        try:
            ser_bytes = serial_readline(ser)
            decoded_bytes = float(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
            print(decoded_bytes)
            with open("heart_wuxin3.csv", "a") as f:
                # 'a' means append data, not erase it
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.time(), decoded_bytes])
        except:
            print("Keyboard Interrupt")
            break

def live_plot_serial(ser):
    ser.flushInput()

    plot_window = 20
    y_var = np.array(np.zeros([plot_window]))

    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(y_var)

    while True:
        try:
            ser_bytes = serial_readline(ser)
            print(ser_bytes)
            decoded_bytes = ser_bytes.decode("utf-8")
            print(decoded_bytes)
            decoded_bytes = decoded_bytes[:-2]
            if decoded_bytes[0] == '(' and decoded_bytes[-1] == ')':
                num_str = decoded_bytes[1:-1]
                heart, tmp = num_str.split(',')
                heart = float(heart)
                tmp = float(tmp)
                print(heart, tmp)
            with open("heart_wuxin3.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([time.time(), heart])
            y_var = np.append(y_var, heart)
            y_var = y_var[1:plot_window+1]
            line.set_ydata(y_var)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
        except:
            print("Keyboard Interrupt")
            break


def serbytes2csv_by500(ser):
    # write serbytes to csv file
    ser.flushInput()
    cnt = 0
    decode_list = []
    while True:
        try:
            ser_bytes = serial_readline(ser)
            cnt = cnt + 1
            print(cnt)
            decoded_bytes = float(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
            print(decoded_bytes)
            decode_list.append(decoded_bytes)
            if cnt%500 == 0:
                with open("heart_wuxin3.csv", "a") as f:
                    # 'a' means append data, not erase it
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow(decode_list)
                    decode_list.clear()
            if cnt == 6000:
                f.close()
                break
        except:
            print("Keyboard Interrupt")
            break


def heart_tmp2csv(ser, heart_path, tmp_path, label):
    ser.flushInput()
    print("start")
    cnt = 0
    heart_list = []
    tmp_list = []
    while cnt <= 90000:
        ser_bytes = serial_readline(ser)
        decoded_bytes = ser_bytes.decode("utf-8")
        decoded_bytes =decoded_bytes[:-2]
        try:
            if decoded_bytes[0] == '(' and decoded_bytes[-1] == ')':
                cnt = cnt + 1
                num_str = decoded_bytes[1:-1]
                heart, tmp = num_str.split(',')
                heart = float(heart)
                tmp = float(tmp)
                print(heart, tmp)
                heart_list.append(heart)
                tmp_list.append(tmp)
                if cnt % 500 == 0:
                    heart_list.append(label)
                    tmp_list.append(label)
                    with open(heart_path, "a") as f1:
                        # 'a' means append data, not erase it
                        writer1 = csv.writer(f1, dialect='excel')
                        writer1.writerow(heart_list)
                        heart_list = []
                    with open(tmp_path, "a") as f2:
                        # 'a' means append data, not erase it
                        writer2 = csv.writer(f2, dialect='excel')
                        writer2.writerow(tmp_list)
                        tmp_list = []
        except:
            print(decoded_bytes, len(decoded_bytes))


def create():
    heart = 'heart_lin.csv'
    f1 = open(heart, 'w')
    f1.close()
    tmp = 'tmp_lin.csv'
    f2 = open(tmp, 'w')
    f2.close()
    return heart, tmp

# heart_path, tmp_path = create()


heart_path = 'heart_wuxin5.csv'
tmp_path = 'tmp_lin.csv'


ser_read = serial.Serial('com5', 9600)  # name must be the same as the bluetooth port  # 9600 波特率
print("if serial is open:", ser_read.is_open)
heart_tmp2csv(ser_read, heart_path, tmp_path, 1)

# ser_write = serial.Serial('com4', 9600)  # name must be the same as the bluetooth port  # 9600 波特率
# print("if serial is open:", ser_write.is_open)
# heart_tmp2csv(ser, heart_path, tmp_path, 1)
'''
while True:
    ser_bytes = serial_readline(ser_read)
    decoded_bytes = ser_bytes.decode("utf-8")
    print(decoded_bytes)
'''