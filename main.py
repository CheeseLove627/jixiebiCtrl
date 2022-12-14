import numpy as np
import cv2
##下面是GUI部分
from tkinter import *
from tkinter.ttk import *
import os
from PIL import Image, ImageTk
##电机部分
import serial
import time  # 延时使用
import binascii
import cv2
import easyocr

test = 1
if test == 1:
    s = 0
else:
    s = serial.Serial("COM3", 115200)  # 初始化串口
reader = easyocr.Reader(['en'])

# 主窗口类
class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("视觉导航系统——第6组作业机")
        self.geometry("1300x950")
        self.resizable(0, 0)
        self["bg"] = "skyblue"
        # 初始化变量
        self.stopflag = 0
        self.test = test
        # PC对机器人的命令
        self.Head = 'f628f628 '
        self.Tail = ' a5a5a5a5'
        # Tag name
        self.cmd_run = '00000001'
        self.cmd_pause = '00000002'
        self.cmd_continue = '00000003'
        self.cmd_stop = '00000004'
        self.cmd_settrack = '00000005'
        self.cmd_setmotorfreq = '00000006'
        self.cmd_getspot = '00000007'
        self.cmd_heartbeat = '00000008'
        self.cmd_down2paper = '00000009'
        self.cmd_reset = '00000010'
        self.cmd_printIO = '00000011'
        #
        self.step = 32
        self.bias = 9
        self.height = 10
        # 加载gui
        self.setup_UI()

    def setup_UI(self):
        # 设定Style
        self.Style01 = Style()
        self.Style01.configure("bottom.TPanedwindow", background="lightgray")
        self.Style01.configure("right.TPanedwindow", background="skyblue")
        self.Style01.configure("TButton", width=10, font=("华文黑体", 15, "bold"))
        # 下边：按钮区域,创建一个容器
        self.Pane_bottom = PanedWindow(width=1290, height=415, style="bottom.TPanedwindow")
        self.Pane_bottom.place(x=5, y=530)
        # 上边：图像区域,创建一个容器
        self.Pane_canvas = PanedWindow(width=1290, height=530, style="bottom.TPanedwindow")
        self.Pane_canvas.place(x=5, y=5)
        # 在窗口画布//
        self.canvas = Canvas(self.Pane_canvas, width=1280, height=520, bg="white")
        # self.Pane_canvas.canvas.place(x=5, y=5)
        self.canvas.pack()
        # LabelFrame
        self.LabelFrame_cmd = LabelFrame(self.Pane_bottom, text="操作栏", width=1270, height=80)
        self.LabelFrame_cmd.place(x=10, y=10)
        self.LabelFrame_info = LabelFrame(self.Pane_bottom, text="状态栏", width=730, height=310)
        self.LabelFrame_info.place(x=10, y=100)
        self.LabelFrame_ctrl = LabelFrame(self.Pane_bottom, text="机械臂控制栏", width=530, height=310)
        self.LabelFrame_ctrl.place(x=750, y=100)
        # 添加操作控件
        self.Button_show = Button(self.LabelFrame_cmd, text="启动相机", width=8, command=self.camara_open)
        self.Button_show.place(x=10, y=10)

        self.Button_getframe = Button(self.LabelFrame_cmd, text="截取图像", width=8, command=self.picture_save)
        self.Button_getframe.place(x=120, y=10)

        self.Button_show = Button(self.LabelFrame_cmd, text="批改", width=5, command=self.Correcting_Machines_2)
        self.Button_show.place(x=230, y=10)

        self.Button_show = Button(self.LabelFrame_cmd, text="计算", width=5, command=self.Compute_machine)
        self.Button_show.place(x=300, y=10)

        self.Button_show = Button(self.LabelFrame_cmd, text="预测", width=5, command=self.Predict_Machines)
        self.Button_show.place(x=370, y=10)

        self.Button_gou = Button(self.LabelFrame_cmd, text="画勾", width=5, command=self.cmdf_gou2)
        self.Button_gou.place(x=450, y=10)

        self.Button_cha = Button(self.LabelFrame_cmd, text="画叉", width=5, command=self.cmdf_cha2)
        self.Button_cha.place(x=530, y=10)

        self.Button_plus = Button(self.LabelFrame_cmd, text="画加", width=5, command=self.cmdf_Splus)
        self.Button_plus.place(x=610, y=10)

        self.Button_minus = Button(self.LabelFrame_cmd, text="画减", width=5, command=self.cmdf_Sminus)
        self.Button_minus.place(x=690, y=10)

        self.Button_1 = Button(self.LabelFrame_cmd, text="1", width=2, command=self.cmdf_S1)
        self.Button_1.place(x=810, y=10)
        self.Button_2 = Button(self.LabelFrame_cmd, text="2", width=2, command=self.cmdf_S2)
        self.Button_2.place(x=840, y=10)
        self.Button_3 = Button(self.LabelFrame_cmd, text="3", width=2, command=self.cmdf_S3)
        self.Button_3.place(x=870, y=10)
        self.Button_4 = Button(self.LabelFrame_cmd, text="4", width=2, command=self.cmdf_S4)
        self.Button_4.place(x=900, y=10)
        self.Button_5 = Button(self.LabelFrame_cmd, text="5", width=2, command=self.cmdf_S5)
        self.Button_5.place(x=930, y=10)
        self.Button_6 = Button(self.LabelFrame_cmd, text="6", width=2, command=self.cmdf_S6)
        self.Button_6.place(x=960, y=10)
        self.Button_7 = Button(self.LabelFrame_cmd, text="7", width=2, command=self.cmdf_S7)
        self.Button_7.place(x=990, y=10)
        self.Button_8 = Button(self.LabelFrame_cmd, text="8", width=2, command=self.cmdf_S8)
        self.Button_8.place(x=1020, y=10)
        self.Button_9 = Button(self.LabelFrame_cmd, text="9", width=2, command=self.cmdf_S9)
        self.Button_9.place(x=1050, y=10)
        self.Button_0 = Button(self.LabelFrame_cmd, text="0", width=2, command=self.cmdf_S0)
        self.Button_0.place(x=1080, y=10)
        # 添加电机控制控件
        # 第一行
        self.Button_cmd_run = Button(self.LabelFrame_ctrl, text="执行", command=self.cmdf_run)
        self.Button_cmd_run.place(x=60, y=10)
        self.Button_cmd_stop = Button(self.LabelFrame_ctrl, text="停止", command=self.cmdf_stop)
        self.Button_cmd_stop.place(x=210, y=10)
        self.Button_cmd_reset = Button(self.LabelFrame_ctrl, text="复位", command=self.cmdf_reset)
        self.Button_cmd_reset.place(x=360, y=10)
        # 第二行
        self.Button_cmd_settrack = Button(self.LabelFrame_ctrl, text="设置轨迹坐标", width=12, command=self.cmdf_settrack)
        self.Button_cmd_settrack.place(x=50, y=80)
        self.Button_cmd_receive = Button(self.LabelFrame_ctrl, text="下降到画板", command=self.cmdf_down2paper)
        self.Button_cmd_receive.place(x=210, y=80)
        self.Button_cmd_getspot = Button(self.LabelFrame_ctrl, text="画斜线", width=12, command=self.cmdf_xiexian)
        self.Button_cmd_getspot.place(x=350, y=80)
        # 第三行
        self.Button_cmd_Xincrease = Button(self.LabelFrame_ctrl, text="X步进", command=self.cmdf_xplus)
        self.Button_cmd_Xincrease.place(x=60, y=150)
        self.Button_cmd_Yincrease = Button(self.LabelFrame_ctrl, text="Y步进", command=self.cmdf_yplus)
        self.Button_cmd_Yincrease.place(x=210, y=150)
        self.Button_cmd_Zincrease = Button(self.LabelFrame_ctrl, text="Z步进", command=self.cmdf_zplus)
        self.Button_cmd_Zincrease.place(x=360, y=150)
        # 第四行
        self.Button_cmd_Xincrease = Button(self.LabelFrame_ctrl, text="X步退", command=self.cmdf_xminus)
        self.Button_cmd_Xincrease.place(x=60, y=220)
        self.Button_cmd_Yincrease = Button(self.LabelFrame_ctrl, text="Y步退", command=self.cmdf_yminus)
        self.Button_cmd_Yincrease.place(x=210, y=220)
        self.Button_cmd_Zincrease = Button(self.LabelFrame_ctrl, text="Z步退", command=self.cmdf_zminus)
        self.Button_cmd_Zincrease.place(x=360, y=220)
        # 添加信息
        # 第一排：发送
        self.Label_send = Label(self.LabelFrame_info, text="串口发送:")
        self.Label_send.place(x=20, y=10)
        self.var_send = StringVar()
        self.Entry_send = Entry(self.LabelFrame_info, textvariable=self.var_send, font=("华文黑体", 15, "bold"), width=50)
        self.Entry_send.place(x=90, y=10)
        self.var_send.set("None")
        # 第1.5排 坐标
        self.Label_x = Label(self.LabelFrame_info, text="X1:")
        self.Label_x.place(x=20, y=55)
        self.var_x = StringVar()
        self.Entry_x = Entry(self.LabelFrame_info, textvariable=self.var_x, font=("华文黑体", 15, "bold"), width=4)
        self.Entry_x.place(x=50, y=50)
        self.var_x.set("0000")

        self.Label_y = Label(self.LabelFrame_info, text="Y1:")
        self.Label_y.place(x=20 + 100, y=55)
        self.var_y = StringVar()
        self.Entry_y = Entry(self.LabelFrame_info, textvariable=self.var_y, font=("华文黑体", 15, "bold"), width=4)
        self.Entry_y.place(x=50 + 100, y=50)
        self.var_y.set("0000")

        self.Label_z = Label(self.LabelFrame_info, text="Z1:")
        self.Label_z.place(x=20 + 100 * 2, y=55)
        self.var_z = StringVar()
        self.Entry_z = Entry(self.LabelFrame_info, textvariable=self.var_z, font=("华文黑体", 15, "bold"), width=4)
        self.Entry_z.place(x=50 + 100 * 2, y=50)
        self.var_z.set("0893")
        # 第二排：接收
        self.Label_receive = Label(self.LabelFrame_info, text="串口接收:")
        self.Label_receive.place(x=20, y=100)
        self.var_receive = StringVar()
        self.Entry_receive = Entry(self.LabelFrame_info, textvariable=self.var_receive, font=("华文黑体", 15, "bold"),
                                   width=50, state='disable')
        self.Entry_receive.place(x=90, y=98)
        self.var_receive.set("")

    def camara_open(self):
        self.canvas.delete('all')
        self.cap = cv2.VideoCapture(0)
        self.stopflag = 0
        while self.cap.isOpened():  # isOpened()  检测摄像头是否处于打开状态
            ref, self.frame = self.cap.read()
            # frame = cv2.flip(frame, 1)  # 摄像头翻转
            cvimage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
            pilImage = Image.fromarray(cvimage)
            pilImage = pilImage.resize((600, 480))#, Image.LANCZOS
            tkImage = ImageTk.PhotoImage(image=pilImage)
            tkImage = np.array(tkImage)
            if ref:  # 如果摄像头读取图像成功
                temp = self.canvas.create_image(300, 240, image=tkImage)
                self.update_idletasks()
                self.update()
                if self.stopflag == 1:
                    break
        self.cap.release()  # 关闭摄像头

    def picture_save(self):
        self.stopflag = 1
        # self.canvas.delete('all')
        cv2.imwrite('./data/frame.jpg', self.frame)  # 保存路径
        self.canvas.create_image(300, 240, image=self.frame)

    def cmdf_run(self):
        cmd = self.Head + self.cmd_run + ' 0000' + self.Tail
        self.var_send.set(cmd)
        Hex_str = bytes.fromhex(cmd)
        s.write(Hex_str)  # 串口发送 Hex_str()
        n = s.inWaiting()  # 串口接收
        if n:
            self.var_receive.set('None')
            data = str(binascii.b2a_hex(s.read(n)))[2:-1]  # Hex转换成字符串
            self.var_receive.set(data)  # 字符串输出

    def cmdf_stop(self):
        cmd = self.Head + self.cmd_stop + ' 0000' + self.Tail
        self.var_send.set(cmd)
        Hex_str = bytes.fromhex(cmd)
        s.write(Hex_str)  # 串口发送 Hex_str()
        n = s.inWaiting()  # 串口接收
        if n:
            self.var_receive.set('None')
            data = str(binascii.b2a_hex(s.read(n)))[2:-1]  # Hex转换成字符串
            self.var_receive.set(data)  # 字符串输出

    def cmdf_reset(self):
        cmd = self.Head + self.cmd_reset + ' 0000' + self.Tail
        self.var_send.set(cmd)
        Hex_str = bytes.fromhex(cmd)
        s.write(Hex_str)  # 串口发送 Hex_str()
        n = s.inWaiting()  # 串口接收
        if n:
            self.var_receive.set('None')
            data = str(binascii.b2a_hex(s.read(n)))[2:-1]  # Hex转换成字符串
            self.var_receive.set(data)  # 字符串输出

    def fun_point_get(self):
        x = self.var_x.get()
        y = self.var_y.get()
        z = self.var_z.get()
        return x, y, z

    def cmdf_settrack(self):
        cmd = self.Head + self.cmd_settrack + ' 0006 ' + self.var_x.get() + ' ' + \
              self.var_y.get() + ' ' + self.var_z.get() + self.Tail + self.Head + self.cmd_run + ' 0000' + self.Tail
        self.var_send.set(cmd)
        Hex_str = bytes.fromhex(cmd)
        s.write(Hex_str)  # 串口发送 Hex_str()
        n = s.inWaiting()  # 串口接收
        if n:
            self.var_receive.set('None')
            data = str(binascii.b2a_hex(s.read(n)))[2:-1]  # Hex转换成字符串
            self.var_receive.set(data)  # 字符串输出

    def fun_point_set(self, x, y, z):
        self.var_x.set(x)
        self.var_y.set(y)
        self.var_z.set(z)
        self.cmdf_settrack()

    def cmdf_down2paper(self):
        self.fun_point_set('0000', '0000', '0893')

    def delta_x(self, x, y, z, n=1, plus=True):
        """
        change x , when plus x++,else x--
        """
        X, Y, Z = x, y, z
        if plus:
            X = str(hex(int(X, 16) + self.step * n)).replace('0x', '').zfill(4) if int(X, 16) <= (
                        int('ffff', 16) - self.step * n) else str(
                hex(self.step * n - int('ffff', 16) + int(X, 16))).replace('0x', '').zfill(4)
            Z = str(hex(int(Z, 16) + self.bias * n)).replace('0x', '').zfill(4) if int(X, 16) < int('f000', 16) else str(
                hex(int(Z, 16) - self.bias * n)).replace('0x', '').zfill(4)
        else:
            X = str(hex(int(X, 16) - self.step * n)).replace('0x', '').zfill(4) if int(X, 16) >= self.step * n else str(
                hex(int('ffff', 16) - self.step * n)).replace('0x', '').zfill(4)
            Z = str(hex(int(Z, 16) - self.bias * n)).replace('0x', '').zfill(4) if int(X, 16) < int('f000', 16) else str(
                hex(int(Z, 16) + self.bias * n)).replace('0x', '').zfill(4)
        return X, Y, Z

    def delta_y(self, x, y, z, n=1, plus=True):
        """
        change y , when plus y++,else y--
        """
        X, Y, Z = x, y, z
        if plus:
            Y = str(hex(int(Y, 16) + self.step * n)).replace('0x', '').zfill(4) if int(Y, 16) <= (
                    int('ffff', 16) - self.step * n) else str(
                hex(self.step * n - int('ffff', 16) + int(Y, 16))).replace('0x', '').zfill(4)
            Z = str(hex(int(Z, 16) + self.bias * n)).replace('0x', '').zfill(4) if int(Y, 16) < int('f000', 16) else str(
                hex(int(Z, 16) - self.bias * n)).replace('0x', '').zfill(4)
        else:
            Y = str(hex(int(Y, 16) - self.step * n)).replace('0x', '').zfill(4) if int(Y, 16) >= self.step * n else str(
                hex(int('ffff', 16) - self.step * n)).replace('0x', '').zfill(4)
            Z = str(hex(int(Z, 16) - (self.bias + 1) * n)).replace('0x', '').zfill(4) if int(Y, 16) < int('f000', 16) else str(
                hex(int(Z, 16) + (self.bias + 1) * n)).replace('0x', '').zfill(4)
        return X, Y, Z

    def delta_z(self, x, y, z, n=1, plus=True):
        """
        change z , when plus z++,else z--
        """
        X, Y, Z = x, y, z
        if plus:
            Z = str(hex(int(Z, 16) + self.step * n)).replace('0x', '').zfill(4)
            if len(Z) > 4: Z = '0000'
        else:
            Z = str(hex(int(Z, 16) - self.step * n)).replace('0x', '').zfill(4) if int(Z, 16) >= self.step * n else '0000'
        return X, Y, Z

    def cmdf_xplus(self, n=1, plus=True):
        X, Y, Z = self.fun_point_get()
        X, Y, Z = self.delta_x(X, Y, Z, n=n, plus=plus)
        self.fun_point_set(X, Y, Z)

    def cmdf_yplus(self, n=1, plus=True):
        X, Y, Z = self.fun_point_get()
        X, Y, Z = self.delta_y(X, Y, Z, n=n, plus=plus)
        self.fun_point_set(X, Y, Z)

    def cmdf_zplus(self, n=1, plus=True):
        X, Y, Z = self.fun_point_get()
        X, Y, Z = self.delta_z(X, Y, Z, n=n, plus=plus)
        self.fun_point_set(X, Y, Z)

    def cmdf_xminus(self, n=1):
        self.cmdf_xplus(n=n, plus=False)

    def cmdf_yminus(self, n=1):
        self.cmdf_yplus(n=n, plus=False)

    def cmdf_zminus(self, n=1):
        self.cmdf_zplus(n=n, plus=False)

    def delta_xy(self, x, y, z, n=3, k=-1, plus=True):
        """
        any slope
        draw a line:y = kx
        n: length
        """
        X, Y, Z = x, y, z
        flag = False if (k > 0) ^ plus else True
        len = n
        # xplus
        X, Y, Z = self.delta_x(X, Y, Z, n=len, plus=plus)
        # yminus
        X, Y, Z = self.delta_y(X, Y, Z, n=round(len * abs(k)), plus=flag)
        if flag:
            X, Y, Z = self.delta_z(X, Y, Z, n=round(len/3), plus=False)
        return X, Y, Z

    def cmdf_xiexian(self, n=3, k=1, plus=False):
        X, Y, Z = self.fun_point_get()
        X, Y, Z = self.delta_xy(X, Y, Z, n, k, plus=plus)
        self.fun_point_set(X, Y, Z)

    def cmdf_gou2(self):
        n = 3
        height = 10
        self.cmdf_yplus(n)
        time.sleep(1)

        self.cmdf_zminus(height)
        time.sleep(1)
        self.cmdf_xiexian(n, -2, plus=True)
        time.sleep(2)

        self.cmdf_xiexian(n * 4, 1, plus=True)
        time.sleep(2)
        self.cmdf_zplus(height)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_chu(self):
        n = 3
        height = 10
        self.cmdf_yplus(n)
        time.sleep(1)
        self.cmdf_xiexian(n, -2, plus=True)
        time.sleep(1)
        self.cmdf_zminus(height)
        time.sleep(1)

        self.cmdf_xiexian(n * 4, 1, plus=True)
        time.sleep(2)
        self.cmdf_zplus(height)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_cha2(self):
        n = 2
        self.cmdf_yplus(n*3)
        time.sleep(1)

        self.cmdf_zminus(self.height)
        time.sleep(1)
        self.cmdf_xiexian(n*4, -1, plus=True)
        time.sleep(2)
        self.cmdf_zplus(self.height)
        time.sleep(1)

        self.cmdf_yplus(n*5)
        time.sleep(2)

        self.cmdf_zminus(self.height + 5)
        time.sleep(2)
        self.cmdf_xiexian(n*5, 1.2, plus=False)
        time.sleep(2)
        self.cmdf_zplus(self.height)
        time.sleep(1)

        self.cmdf_down2paper()
    def cmdf_Splus(self):
        n = 2

        self.cmdf_xminus(n * 2)
        time.sleep(1)

        self.cmdf_zminus(self.height)
        time.sleep(1)
        self.cmdf_xplus(n * 4)
        time.sleep(2)
        self.cmdf_zplus(self.height)
        time.sleep(1)

        self.cmdf_xminus(n * 2)
        time.sleep(1)
        self.cmdf_yplus(n * 2)
        time.sleep(1)

        self.cmdf_zminus(self.height)
        time.sleep(1)
        self.cmdf_yminus(n * 4)
        time.sleep(2)
        self.cmdf_zplus(self.height)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_Sminus(self):
        n = 2
        self.cmdf_xplus(n * 2, plus=False)
        time.sleep(1)

        self.cmdf_zplus(self.height, plus=False)
        time.sleep(1)
        self.cmdf_xplus(n * 4, plus=True)
        time.sleep(2)

        self.cmdf_down2paper()

    def cmdf_S1(self):
        n = 2
        self.cmdf_yplus(n * 2)
        time.sleep(1)

        self.cmdf_zminus(self.height)
        time.sleep(1)
        self.cmdf_yminus(n * 4)
        time.sleep(2)
        self.cmdf_zplus(self.height)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S2(self):
        n = 2
        self.cmdf_xiexian(n * 2, -1, plus=False)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_yminus(n * 2)
        time.sleep(1)
        self.cmdf_xminus(n * 2)
        time.sleep(1)
        self.cmdf_yminus(n * 2)
        time.sleep(1)
        self.cmdf_xplus(n * 2)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S3(self):
        n = 2
        self.cmdf_xiexian(n * 2, -1, plus=False)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_xiexian(n * 2, 1, plus=False)
        time.sleep(1)
        self.cmdf_xiexian(n * 3, -0.5, plus=True)
        time.sleep(1)
        self.cmdf_xiexian(n * 2, 2, plus=False)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S4(self):
        n = 2
        self.cmdf_xiexian(n * 2, -1, plus=True)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_xminus(n * 2 + 1)
        time.sleep(1)
        self.cmdf_xiexian(n * 2 + 1, 1, plus=True)
        time.sleep(1)
        self.cmdf_yminus(n * 4)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S5(self):
        n = 2
        self.cmdf_xiexian(n * 2, 1, plus=True)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_xminus(n * 2)
        time.sleep(1)
        self.cmdf_yminus(n * 1)
        time.sleep(1)
        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_yminus(n * 2)
        time.sleep(1)
        self.cmdf_xminus(n * 2)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S6(self):
        n = 2
        self.cmdf_xiexian(n * 1, -1, plus=False)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_yminus(n * 4)
        time.sleep(1)
        self.cmdf_xplus(n * 3)
        time.sleep(1)
        self.cmdf_yplus(n * 3)
        time.sleep(1)
        self.cmdf_xminus(n * 2)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S7(self):
        n = 2
        self.cmdf_xiexian(n * 2, -1, plus=False)
        time.sleep(1)

        self.cmdf_zminus(self.height)
        time.sleep(1)
        self.cmdf_xplus(n * 3)
        time.sleep(1)
        self.cmdf_xiexian(n * 3, 1, plus=False)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S8(self):
        n = 2
        self.cmdf_xminus(n * 1)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_yminus(n * 2)
        time.sleep(1)
        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_yplus(n * 2)
        time.sleep(1)
        self.cmdf_xminus(n * 2)
        time.sleep(1)
        self.cmdf_yplus(n * 2)
        time.sleep(1)
        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_yminus(n * 2)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S9(self):
        n = 2
        self.cmdf_xplus(n * 1)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_xminus(n * 2)
        time.sleep(1)
        self.cmdf_yplus(n * 2)
        time.sleep(1)
        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_yminus(n * 4)
        time.sleep(1)

        self.cmdf_down2paper()

    def cmdf_S0(self):
        n = 1
        self.cmdf_xminus(n * 1)
        time.sleep(1)
        self.cmdf_zminus(self.height)
        time.sleep(1)

        self.cmdf_yminus(n * 4)
        time.sleep(1)
        self.cmdf_xplus(n * 2)
        time.sleep(1)
        self.cmdf_yplus(n * 4)
        time.sleep(1)
        self.cmdf_xminus(n * 2)
        time.sleep(1)
        # self.cmdf_yminus(n * 2)
        # time.sleep(1)

        self.cmdf_down2paper()

    def Correcting_Machines_2(self):
        """
        1+1=3 ？
        """
        self.stopflag = 1

        img = cv2.imread('./data/frame.jpg')
        # self.canvas.create_image(300, 240, image=cv2.imread('./data/frame.jpg'))
        # self.canvas.create_image(300, 240, image=img)
        # self.update_idletasks()
        # self.update()

        result = reader.readtext(img)
        m = []
        for res in result:
            m.append(res[1])
        #print(m)  # m:['11+11', '=20']
        #print('\n')
        # print(m[0]) #m[0]:11+11   m[1]:=20
        # print('\n')
        arry = []
        for i in m:

            for q in i:
                arry.append(q)
        # print(arry) #arry:  ['1', '1', '+', '1', '1', '=', '2', '0']
        num_1 = []
        num_2 = []
        num_3 = []
        flag = 0
        for i in arry:
            if i.isdigit() and (flag == 0):
                num_1.append(int(i))  # [1, 1]
            elif i.isdigit() and (flag == 1):
                num_2.append(int(i))  # [1, 1]
            elif i.isdigit() and (flag == 2):
                num_3.append(int(i))  # [2, 0]
            elif i != ' ':
                flag = flag + 1
        add_1 = ""
        add_2 = ""
        sum = ""
        for a in num_1:
            add_1 += str(a)
        for a in num_2:
            add_2 += str(a)
        for a in num_3:
            sum += str(a)
        add_1 = int(add_1)  # add_1:11
        add_2 = int(add_2)  # add_2:11
        sum = int(sum)  # sum:20
        if (add_1 + add_2) == sum:
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='green', outline='green', width=2)
            self.canvas.create_text((950, 240), text='Correct!', font=("Microsoft YaHei", 50))
            if self.test == 0:
                self.cmdf_gou2()
            print("Correct!")
        else:
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='red', outline='green', width=2)
            self.canvas.create_text((950, 240), text='Wrong!', font=("Microsoft YaHei", 50))
            if self.test == 0:
                self.cmdf_cha2()
            print("Wrong!")

    def predict(self, x, y, z):
        if x * y == z:
            print("*")
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='blue', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(x)+'X'+str(y)+'='+str(z), font=("Microsoft YaHei", 50))
            if self.test == 0:
                self.cmdf_cha2()
            return 0
        elif x + y == z:
            print("+")
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='blue', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(x) + '+' + str(y) + '=' + str(z), font=("Microsoft YaHei", 50))
            if self.test == 0:
                self.cmdf_Splus()
            return 1
        elif x - y == z:
            print("-")
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='blue', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(x) + '-' + str(y) + '=' + str(z), font=("Microsoft YaHei", 50))
            if self.test == 0:
                self.cmdf_Sminus()
            return 2
        elif x // y == z:
            print("/")
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='blue', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(x) + '/' + str(y) + '=' + str(z), font=("Microsoft YaHei", 50))
            if self.test == 0:
                self.cmdf_Schu()
            return 3


    def Predict_Machines(self):
        """
        1？1 =2
        """
        self.stopflag = 1
        img = cv2.imread('./data/frame.jpg')
        result = reader.readtext(img)
        m = []
        for res in result:
            m.append(res[1])
        arry = []
        for i in m:
            for q in i:
                arry.append(q)
        num_1 = []
        num_2 = []
        num_3 = []
        flag = 0
        for i in arry:
            if i.isdigit() and (flag == 0):
                num_1.append(int(i))  # [3]
            elif i.isdigit() and (flag == 1):
                num_2.append(int(i))  # [1, 1]
            # elif i.isdigit() and (flag == 2):
            #   num_3.append(int(i)) #[2, 0]
            elif i != ' ':
                flag = flag + 1
        insert_pos = len(num_1) // 2
        num_1.insert(insert_pos, 'x')
        num_1_1 = []
        num_2_2 = []
        funk = 0
        for i in num_1:
            if type(i) == int and (funk == 0):
                num_1_1.append(int(i))
            elif type(i) == int and (funk == 1):
                num_2_2.append(int(i))
            elif i != ' ':
                funk = funk + 1
        add_1 = ""
        add_2 = ""
        sum = ""
        for a in num_1_1:
            add_1 += str(a)
        for a in num_2_2:
            add_2 += str(a)
        for a in num_2:
            sum += str(a)
        add_1 = int(add_1)  # add_1:14
        add_2 = int(add_2)  # add_2:21
        sum = int(sum)  # sum:294
        self.predict(add_1, add_2, sum)

    def Compute_machine(self):
        """
        1+1=?
        """
        self.stopflag = 1
        img = cv2.imread('./data/frame.jpg')
        m = []
        result = reader.readtext(img)
        for res in result:
            m.append(res[1])
        print('\n')
        arry = []
        for i in m:
            for q in i:
                arry.append(q)
        num_1 = []
        num_2 = []
        num_3 = []
        flag = 0
        for i in arry:
            if i.isdigit() and (flag == 0):
                num_1.append(int(i))  # [3]
            elif i.isdigit() and (flag == 1):
                num_2.append(int(i))  # [1, 1]
            elif i != ' ':
                num_3.append(i)
                flag = flag + 1
        num_4 = str(num_3[0])  # 符号 +
        add_1 = ""
        add_2 = ""
        for a in num_1:
            add_1 += str(a)
        for a in num_2:
            add_2 += str(a)
        add_1 = int(add_1)  # add_1:12
        add_2 = int(add_2)  # add_2:18
        if num_4 == '+':
            final = add_1 + add_2
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='yellow', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(add_1) + '+' + str(add_2) + '=' + str(final), font=("Microsoft YaHei", 50))
            self
        elif num_4 == '-':
            final = add_1 - add_2
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='yellow', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(add_1) + '-' + str(add_2) + '=' + str(final), font=("Microsoft YaHei", 50))
        elif num_4 == 'X' or 'x':
            final = add_1 * add_2
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='yellow', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(add_1) + 'X' + str(add_2) + '=' + str(final), font=("Microsoft YaHei", 50))
        elif num_4 == '/':
            final = add_1 // add_2
            self.canvas.create_rectangle(650, 5, 1250, 480, fill='yellow', outline='green', width=2)
            self.canvas.create_text((950, 240), text=str(add_1) + '/' + str(add_2) + '=' + str(final), font=("Microsoft YaHei", 50))
        print(final)

if __name__ == "__main__":
    this_main = MainWindow()
    this_main.mainloop()
