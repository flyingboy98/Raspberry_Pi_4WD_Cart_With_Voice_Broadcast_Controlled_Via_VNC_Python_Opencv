import os
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Servo init
GPIO_SERVO = 17
GPIO.setup(GPIO_SERVO, GPIO.OUT)
servo = GPIO.PWM(GPIO_SERVO, 50)
servo.start(0)
servo.ChangeDutyCycle(7.5)
time.sleep(1)
servo.ChangeDutyCycle(0)

# Motor init
GPIO_MOTOR1_IN1 = 16
GPIO_MOTOR1_IN2 = 19
GPIO_MOTOR2_IN1 = 20
GPIO_MOTOR2_IN2 = 26
GPIO_MOTOR3_IN1 = 10
GPIO_MOTOR3_IN2 = 9
GPIO_MOTOR4_IN1 = 8
GPIO_MOTOR4_IN2 = 7

MO_FR = 10000

GPIO.setup(GPIO_MOTOR1_IN1, GPIO.OUT)
GPIO.setup(GPIO_MOTOR1_IN2, GPIO.OUT)
GPIO.setup(GPIO_MOTOR2_IN1, GPIO.OUT)
GPIO.setup(GPIO_MOTOR2_IN2, GPIO.OUT)
GPIO.setup(GPIO_MOTOR3_IN1, GPIO.OUT)
GPIO.setup(GPIO_MOTOR3_IN2, GPIO.OUT)
GPIO.setup(GPIO_MOTOR4_IN1, GPIO.OUT)
GPIO.setup(GPIO_MOTOR4_IN2, GPIO.OUT)

GPIO.output(GPIO_MOTOR1_IN1, False)
GPIO.output(GPIO_MOTOR1_IN2, False)
GPIO.output(GPIO_MOTOR2_IN1, False)
GPIO.output(GPIO_MOTOR2_IN2, False)
GPIO.output(GPIO_MOTOR3_IN1, False)
GPIO.output(GPIO_MOTOR3_IN2, False)
GPIO.output(GPIO_MOTOR4_IN1, False)
GPIO.output(GPIO_MOTOR4_IN2, False)

motor1_z = GPIO.PWM(GPIO_MOTOR1_IN1,MO_FR)
motor1_f = GPIO.PWM(GPIO_MOTOR1_IN2,MO_FR)
motor2_z = GPIO.PWM(GPIO_MOTOR2_IN1,MO_FR)
motor2_f = GPIO.PWM(GPIO_MOTOR2_IN2,MO_FR)
motor3_z = GPIO.PWM(GPIO_MOTOR3_IN1,MO_FR)
motor3_f = GPIO.PWM(GPIO_MOTOR3_IN2,MO_FR)
motor4_z = GPIO.PWM(GPIO_MOTOR4_IN1,MO_FR)
motor4_f = GPIO.PWM(GPIO_MOTOR4_IN2,MO_FR)
motor1_z.start(0)
motor1_f.start(0)
motor2_z.start(0)
motor2_f.start(0)
motor3_z.start(0)
motor3_f.start(0)
motor4_z.start(0)
motor4_f.start(0)
motor1_z.ChangeDutyCycle(0)
motor1_f.ChangeDutyCycle(0)
motor2_z.ChangeDutyCycle(0)
motor2_f.ChangeDutyCycle(0)
motor3_z.ChangeDutyCycle(0)
motor3_f.ChangeDutyCycle(0)
motor4_z.ChangeDutyCycle(0)
motor4_f.ChangeDutyCycle(0)

# Sensor init
GPIO_ECHO = 23
GPIO_TRIGGER = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)
time.sleep(2)

GPIO_INFARED_BACK = 4
GPIO.setup(GPIO_INFARED_BACK,GPIO.IN)

GPIO_INFARED_DOWN = 18
GPIO.setup(GPIO_INFARED_DOWN,GPIO.IN)

# Camera init
video_source = 0


class App:
    
    # Servo position arg
    sl = False
    sr = False
    # "f" for motor speed arg, "b" for mode "dao"
    f = 0
    b = 0
    
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.minsize(800, 700)
        
        #Background
        background_image = tkinter.PhotoImage(file="bg.png")
        background_label = tkinter.Label(window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image
        
        # Open video source
        self.vid = MyVideoCapture(video_source)
        
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack(anchor=tkinter.CENTER)
        
        # Keyboard controlling
        self.window.bind('a', self.keyboard_s_l)
        self.window.bind('w', self.keyboard_s_c)
        self.window.bind('d', self.keyboard_s_r)
        
        self.window.bind('<Up>', self.jia)
        self.window.bind('<Down>', self.jian)
        self.window.bind('<Left>', self.zuo)
        self.window.bind('<Right>', self.you)
        self.window.bind('p', self.ting)
        self.window.bind('b', self.dao)
        
        # Button controlling
        self.btn_servo_l=tkinter.Button(window, text="左看", width=3, height=3, command=self.button_s_l)
        self.btn_servo_l.place(x=8, y=240)
        self.btn_servo_l.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red', font=('', 10,))

        self.btn_servo_r=tkinter.Button(window, text="右看", width=3, height=3, command=self.button_s_r)
        self.btn_servo_r.place(x=728, y=240)
        self.btn_servo_r.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red', font=('', 10,))

        self.btn_jia=tkinter.Button(window, text="前进/加速", width=4, height=2, command=self.jia)
        self.btn_jia.place(x=370, y=485)
        self.btn_jia.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red')

        self.btn_jian=tkinter.Button(window, text="减速", width=4, height=2, command=self.jian)
        self.btn_jian.place(x=370, y=605)
        self.btn_jian.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red')

        self.btn_zuo=tkinter.Button(window, text="左转", width=4, height=2, command=self.zuo)
        self.btn_zuo.place(x=290, y=545)
        self.btn_zuo.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red')

        self.btn_you=tkinter.Button(window, text="右转", width=4, height=2, command=self.you)
        self.btn_you.place(x=450, y=545)
        self.btn_you.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red')

        self.btn_ting=tkinter.Button(window, text="停车", width=4, height=2, command=self.ting)
        self.btn_ting.place(x=370, y=545)
        self.btn_ting.config(bd=5, bg='light green', activebackground='light green', fg='black', activeforeground='red')

        self.btn_dao=tkinter.Button(window, text="倒车", width=4, height=2, command=self.dao)
        self.btn_dao.place(x=645, y=605)
        self.btn_dao.config(bd=5, bg='dark green', activebackground='dark green', fg='black', activeforeground='red')

        # Labels
        self.label4=tkinter.Label(window, text="4", width=3, height=2)
        self.label4.place(x=179, y=485)
        self.label4.config(bd=0, bg='dark red', fg='black')

        self.label3=tkinter.Label(window, text="3", width=3, height=2)
        self.label3.place(x=146, y=485)
        self.label3.config(bd=0, bg='dark red', fg='black')

        self.label2=tkinter.Label(window, text="2", width=3, height=2)
        self.label2.place(x=113, y=485)
        self.label2.config(bd=0, bg='dark red', fg='black')

        self.label1=tkinter.Label(window, text="1", width=3, height=2)
        self.label1.place(x=80, y=485)
        self.label1.config(bd=0, bg='dark red', fg='black')
        
        self.label5=tkinter.Label(window, text="提示信息", width=16, height=2)
        self.label5.place(x=80, y=545)
        self.label5.config(bg='light yellow')
        
        self.label6=tkinter.Label(window, text="", width=16, height=2)
        self.label6.place(x=80, y=580)
        self.label6.config(bg='light yellow')

        self.label7=tkinter.Label(window, text="", width=16, height=2)
        self.label7.place(x=80, y=615)
        self.label7.config(bg='light yellow')

        # Entry box
        self.entry=tkinter.Entry(window, width=25,)
        self.entry.place(x=490, y=485)
        self.speak_butt=tkinter.Button(window, text="发送", width=2, height=1, command=self.speak)
        self.speak_butt.place(x=675, y=515)


        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        
        self.window.mainloop()

    # Control servo from screen
    def button_s_l(self):
            
        if self.sl:
            self.btn_servo_l["background"] = "dark green"
            self.btn_servo_l["activebackground"] = "dark green"
            servo.ChangeDutyCycle(7.5)
            time.sleep(1)
            self.sl = False
        else:
            if self.sr:
                self.sr = False
                self.btn_servo_r["background"] = "dark green"
                self.btn_servo_r["activebackground"] = "dark green"
            self.btn_servo_l["background"] = "light green"
            self.btn_servo_l["activebackground"] = "light green"
            servo.ChangeDutyCycle(2.5)
            time.sleep(1)
            self.sl = True
            
        servo.ChangeDutyCycle(0)
        
    def button_s_r(self):
  
        if self.sr:
            self.btn_servo_r["background"] = "dark green"
            self.btn_servo_r["activebackground"] = "dark green"
            servo.ChangeDutyCycle(7.5)
            time.sleep(1)
            self.sr = False
        else:
            if self.sl:
                self.sl = False
                self.btn_servo_l["background"] = "dark green"
                self.btn_servo_l["activebackground"] = "dark green"
            self.btn_servo_r["background"] = "light green"
            self.btn_servo_r["activebackground"] = "light green"
            servo.ChangeDutyCycle(12.5)
            time.sleep(1)
            self.sr = True
            
        servo.ChangeDutyCycle(0)

    # Control servo from keyboard
    def keyboard_s_l(self, _event=None):
        self.btn_servo_l["background"] = "light green"
        self.btn_servo_l["activebackground"] = "light green"
        self.btn_servo_r["background"] = "dark green"
        self.btn_servo_r["activebackground"] = "dark green"
            
        if self.sl:
            time.sleep(0.1)
        else:
            servo.ChangeDutyCycle(2.5)
            time.sleep(1)
            servo.ChangeDutyCycle(0)
            self.sl = True
            self.sr = False
            
    def keyboard_s_c(self, _event=None):
        
        self.btn_servo_l["background"] = "dark green"
        self.btn_servo_l["activebackground"] = "dark green"
        self.btn_servo_r["background"] = "dark green"
        self.btn_servo_r["activebackground"] = "dark green"
            
        if self.sr:
            servo.ChangeDutyCycle(7.5)
            time.sleep(1)
            servo.ChangeDutyCycle(0)
            self.sr = False
        elif self.sl:
            servo.ChangeDutyCycle(7.5)
            time.sleep(1)
            servo.ChangeDutyCycle(0)
            self.sl = False            
            
    def keyboard_s_r(self, _event=None):
        
        self.btn_servo_l["background"] = "dark green"
        self.btn_servo_l["activebackground"] = "dark green"
        self.btn_servo_r["background"] = "light green"
        self.btn_servo_r["activebackground"] = "light green"
            
        if self.sr:
            time.sleep(0.1)
        else:
            servo.ChangeDutyCycle(12.5)
            time.sleep(1)
            servo.ChangeDutyCycle(0)
            self.sl = False
            self.sr = True

    # Control motors
    def zuo(self, _event=None):

        if self.b == 1:
            GPIO.output(GPIO_MOTOR1_IN1, False)
            GPIO.output(GPIO_MOTOR1_IN2, True)
            GPIO.output(GPIO_MOTOR2_IN1, False)
            GPIO.output(GPIO_MOTOR2_IN2, False)
            GPIO.output(GPIO_MOTOR3_IN1, False)
            GPIO.output(GPIO_MOTOR3_IN2, True)
            GPIO.output(GPIO_MOTOR4_IN1, False)
            GPIO.output(GPIO_MOTOR4_IN2, False)            
            motor1_f.ChangeDutyCycle(25)
            motor2_f.ChangeDutyCycle(0)            
            motor3_f.ChangeDutyCycle(25)
            motor4_f.ChangeDutyCycle(0)
        else:
            GPIO.output(GPIO_MOTOR1_IN1, False)
            GPIO.output(GPIO_MOTOR1_IN2, False)
            GPIO.output(GPIO_MOTOR2_IN1, True)
            GPIO.output(GPIO_MOTOR2_IN2, False)
            GPIO.output(GPIO_MOTOR3_IN1, False)
            GPIO.output(GPIO_MOTOR3_IN2, False)
            GPIO.output(GPIO_MOTOR4_IN1, True)
            GPIO.output(GPIO_MOTOR4_IN2, False)            
            motor1_z.ChangeDutyCycle(0)
            motor2_z.ChangeDutyCycle(25)
            motor3_z.ChangeDutyCycle(0)
            motor4_z.ChangeDutyCycle(25)
            
            self.f = 1
        
        self.btn_zuo["background"] = "light green"
        self.btn_zuo["activebackground"] = "light green"
        self.btn_you["background"] = "dark green"
        self.btn_you["activebackground"] = "dark green"
        self.btn_jia["background"] = "dark green"
        self.btn_jia["activebackground"] = "dark green"
        self.btn_jian["background"] = "dark green"
        self.btn_jian["activebackground"] = "dark green"
        self.btn_ting["background"] = "dark green"
        self.btn_ting["activebackground"] = "dark green"
        
        self.label1["background"] = "red"
        self.label2["background"] = "dark red"
        self.label3["background"] = "dark red"
        self.label4["background"] = "dark red"
   
    def you(self, _event=None):
        
        if self.b == 1:
            GPIO.output(GPIO_MOTOR1_IN1, False)
            GPIO.output(GPIO_MOTOR1_IN2, False)
            GPIO.output(GPIO_MOTOR2_IN1, False)
            GPIO.output(GPIO_MOTOR2_IN2, True)
            GPIO.output(GPIO_MOTOR3_IN1, False)
            GPIO.output(GPIO_MOTOR3_IN2, False)
            GPIO.output(GPIO_MOTOR4_IN1, False)
            GPIO.output(GPIO_MOTOR4_IN2, True)            
            motor1_f.ChangeDutyCycle(0)
            motor2_f.ChangeDutyCycle(25)            
            motor3_f.ChangeDutyCycle(0)
            motor4_f.ChangeDutyCycle(25)
        else:
            GPIO.output(GPIO_MOTOR1_IN1, True)
            GPIO.output(GPIO_MOTOR1_IN2, False)
            GPIO.output(GPIO_MOTOR2_IN1, False)
            GPIO.output(GPIO_MOTOR2_IN2, False)
            GPIO.output(GPIO_MOTOR3_IN1, True)
            GPIO.output(GPIO_MOTOR3_IN2, False)
            GPIO.output(GPIO_MOTOR4_IN1, False)
            GPIO.output(GPIO_MOTOR4_IN2, False)            
            motor1_z.ChangeDutyCycle(25)
            motor2_z.ChangeDutyCycle(0)
            motor3_z.ChangeDutyCycle(25)
            motor4_z.ChangeDutyCycle(0)
            
            self.f = 1
        
        self.btn_you["background"] = "light green"
        self.btn_you["activebackground"] = "light green"
        self.btn_zuo["background"] = "dark green"
        self.btn_zuo["activebackground"] = "dark green"
        self.btn_jia["background"] = "dark green"
        self.btn_jia["activebackground"] = "dark green"
        self.btn_jian["background"] = "dark green"
        self.btn_jian["activebackground"] = "dark green"
        self.btn_ting["background"] = "dark green"
        self.btn_ting["activebackground"] = "dark green"

        self.label1["background"] = "red"
        self.label2["background"] = "dark red"
        self.label3["background"] = "dark red"
        self.label4["background"] = "dark red"
        
    def jia(self, _event=None):
        
        # mode "dao" can't be accelerated.
        if self.b == 1:
            return
        
        # mode "turn" can't be accelerated, make it forward.
        if self.btn_zuo["background"] == "light green" or self.btn_you["background"] == "light green":
            pass
        else:
            self.f += 1
            if self.f > 4:
                self.f = 4
            
        if self.f == 1:
            GPIO.output(GPIO_MOTOR1_IN1, True)
            GPIO.output(GPIO_MOTOR1_IN2, False)
            GPIO.output(GPIO_MOTOR2_IN1, True)
            GPIO.output(GPIO_MOTOR2_IN2, False)
            GPIO.output(GPIO_MOTOR3_IN1, True)
            GPIO.output(GPIO_MOTOR3_IN2, False)
            GPIO.output(GPIO_MOTOR4_IN1, True)
            GPIO.output(GPIO_MOTOR4_IN2, False)            
            motor1_z.ChangeDutyCycle(25)
            motor2_z.ChangeDutyCycle(25)
            motor3_z.ChangeDutyCycle(25)
            motor4_z.ChangeDutyCycle(25)
            self.label1["background"] = "red"
            self.label1["activebackground"] = "red"
        elif self.f==2:
            motor1_z.ChangeDutyCycle(50)
            motor2_z.ChangeDutyCycle(50)
            motor3_z.ChangeDutyCycle(50)
            motor4_z.ChangeDutyCycle(50)
            self.label1["background"] = "dark red"
            self.label2["background"] = "red"
        elif self.f==3:
            motor1_z.ChangeDutyCycle(75)
            motor2_z.ChangeDutyCycle(75)
            motor3_z.ChangeDutyCycle(75)
            motor4_z.ChangeDutyCycle(75)
            self.label2["background"] = "dark red"
            self.label3["background"] = "red"
        elif self.f==4:
            motor1_z.ChangeDutyCycle(99)
            motor2_z.ChangeDutyCycle(99)
            motor3_z.ChangeDutyCycle(99)
            motor4_z.ChangeDutyCycle(99)
            self.label3["background"] = "dark red"
            self.label4["background"] = "red"
        
        self.btn_jia["background"] = "light green"
        self.btn_jia["activebackground"] = "light green"
        self.btn_you["background"] = "dark green"
        self.btn_you["activebackground"] = "dark green"
        self.btn_zuo["background"] = "dark green"
        self.btn_zuo["activebackground"] = "dark green"
        self.btn_jian["background"] = "dark green"
        self.btn_jian["activebackground"] = "dark green"
        self.btn_ting["background"] = "dark green"
        self.btn_ting["activebackground"] = "dark green"
        self.btn_dao["background"] = "dark green"
        self.btn_dao["activebackground"] = "dark green"        
        
    def jian(self, _event=None):
        
        if self.b == 1:
            self.ting()
            return
            
        self.f -= 1        
        if self.f < 0:
            self.f = 0
            return
            
        if self.f == 0:
            self.ting()
            return
            
        elif self.f==1:
            motor1_z.ChangeDutyCycle(25)
            motor2_z.ChangeDutyCycle(25)
            motor3_z.ChangeDutyCycle(25)
            motor4_z.ChangeDutyCycle(25)
            self.label1["background"] = "red"
            self.label2["background"] = "dark red"
        elif self.f==2:
            motor1_z.ChangeDutyCycle(50)
            motor2_z.ChangeDutyCycle(50)
            motor3_z.ChangeDutyCycle(50)
            motor4_z.ChangeDutyCycle(50)
            self.label2["background"] = "red"
            self.label3["background"] = "dark red"
        elif self.f==3:
            motor1_z.ChangeDutyCycle(75)
            motor2_z.ChangeDutyCycle(75)
            motor3_z.ChangeDutyCycle(75)
            motor4_z.ChangeDutyCycle(75)
            self.label3["background"] = "red"
            self.label4["background"] = "dark red"
         
        if self.f != 0:
            self.btn_jian["background"] = "light green"
            self.btn_jian["activebackground"] = "light green"
        self.btn_you["background"] = "dark green"
        self.btn_you["activebackground"] = "dark green"
        self.btn_jia["background"] = "dark green"
        self.btn_jia["activebackground"] = "dark green"
        self.btn_zuo["background"] = "dark green"
        self.btn_zuo["activebackground"] = "dark green"
        self.btn_ting["background"] = "dark green"
        self.btn_ting["activebackground"] = "dark green"
        self.btn_dao["background"] = "dark green"
        self.btn_dao["activebackground"] = "dark green"        
       
    def ting(self, _event=None):
        
        GPIO.output(GPIO_MOTOR1_IN1, GPIO.LOW)
        GPIO.output(GPIO_MOTOR1_IN2, GPIO.LOW)
        GPIO.output(GPIO_MOTOR2_IN1, GPIO.LOW)
        GPIO.output(GPIO_MOTOR2_IN2, GPIO.LOW)
        GPIO.output(GPIO_MOTOR3_IN1, GPIO.LOW)
        GPIO.output(GPIO_MOTOR3_IN2, GPIO.LOW)
        GPIO.output(GPIO_MOTOR4_IN1, GPIO.LOW)
        GPIO.output(GPIO_MOTOR4_IN2, GPIO.LOW)
        motor1_z.ChangeDutyCycle(0)
        motor2_z.ChangeDutyCycle(0)
        motor3_z.ChangeDutyCycle(0)
        motor4_z.ChangeDutyCycle(0)
        motor1_f.ChangeDutyCycle(0)
        motor2_f.ChangeDutyCycle(0)
        motor3_f.ChangeDutyCycle(0)
        motor4_f.ChangeDutyCycle(0)
        
        self.f = 0
        self.b = 0
        
        time.sleep(2)
        
        self.label1["background"] = "dark red"
        self.label2["background"] = "dark red"
        self.label3["background"] = "dark red"
        self.label4["background"] = "dark red"
        
        self.btn_ting["background"] = "light green"
        self.btn_ting["activebackground"] = "light green"
        self.btn_you["background"] = "dark green"
        self.btn_you["activebackground"] = "dark green"
        self.btn_jia["background"] = "dark green"
        self.btn_jia["activebackground"] = "dark green"
        self.btn_jian["background"] = "dark green"
        self.btn_jian["activebackground"] = "dark green"
        self.btn_zuo["background"] = "dark green"
        self.btn_zuo["activebackground"] = "dark green"
        self.btn_dao["background"] = "dark green"
        self.btn_dao["activebackground"] = "dark green"
        
    def dao(self, _event=None):
        
        if self.f != 0:
            self.ting()
        
        self.b = 1
        
        self.label1["background"] = "dark red"
        self.label2["background"] = "dark red"
        self.label3["background"] = "dark red"
        self.label4["background"] = "dark red"
        
        self.btn_dao["background"] = "light green"
        self.btn_dao["activebackground"] = "light green"
        self.btn_ting["background"] = "dark green"
        self.btn_ting["activebackground"] = "dark green"
        self.btn_you["background"] = "dark green"
        self.btn_you["activebackground"] = "dark green"
        self.btn_jia["background"] = "dark green"
        self.btn_jia["activebackground"] = "dark green"
        self.btn_jian["background"] = "dark green"
        self.btn_jian["activebackground"] = "dark green"
        self.btn_zuo["background"] = "dark green"
        self.btn_zuo["activebackground"] = "dark green"

        GPIO.output(GPIO_MOTOR1_IN1, False)
        GPIO.output(GPIO_MOTOR1_IN2, True)
        GPIO.output(GPIO_MOTOR2_IN1, False)
        GPIO.output(GPIO_MOTOR2_IN2, True)
        GPIO.output(GPIO_MOTOR3_IN1, False)
        GPIO.output(GPIO_MOTOR3_IN2, True)
        GPIO.output(GPIO_MOTOR4_IN1, False)
        GPIO.output(GPIO_MOTOR4_IN2, True)
        motor1_f.ChangeDutyCycle(25)
        motor2_f.ChangeDutyCycle(25)
        motor3_f.ChangeDutyCycle(25)
        motor4_f.ChangeDutyCycle(25)
        
    def speak(self):
        in_str = self.entry.get()
        comm_line = "python3 ./yy/bin/zhspeak.py " + in_str
        os.system(comm_line)
        
        self.entry.delete(0, 'end')
        self.speak_butt.focus_set()
            
    def check_sensor(self):
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        distance = round((TimeElapsed * 34300) / 2, 2)
        
        if distance < 30:
            if self.f != 0:
                self.ting()
            self.label5["text"] = "前方有障碍物！请注意！"
            self.label5["background"] = "yellow"
        else:
            if self.label5["text"] == "前方有障碍物！请注意！":
                self.label5["text"] = "提示信息"
                self.label5["background"] = "light yellow"
                
        if GPIO.input(GPIO_INFARED_BACK)==0:
            if self.b == 1:
                self.ting()
                self.label6["text"] = "后方有障碍物！请注意！"
            else:
                self.label6["text"] = "后方有人靠近！请注意！"
            self.label6["background"] = "yellow"
        else:
            if self.label6["text"] == "后方有障碍物！请注意！" or self.label6["text"] == "后方有人靠近！请注意！":
                self.label6["text"] = ""
                self.label6["background"] = "light yellow"
                
        if GPIO.input(GPIO_INFARED_DOWN)==1:
            self.label7["text"] = "车已离开地面！请注意！"
            self.label7["background"] = "yellow"
            os.system("mplayer if001.mp3")
        else:
            if self.label7["text"] == "车已离开地面！请注意！":
                self.label7["text"] = ""
                self.label7["background"] = "light yellow"
            
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        # Check sensor state
        css = self.check_sensor()
            
        self.window.after(self.delay, self.update)
        
    def __del__(self):
        servo.ChangeDutyCycle(0)
        motor1_z.ChangeDutyCycle(0)
        motor2_z.ChangeDutyCycle(0)            
        motor3_z.ChangeDutyCycle(0)
        motor4_z.ChangeDutyCycle(0)
        motor1_f.ChangeDutyCycle(0)
        motor2_f.ChangeDutyCycle(0)            
        motor3_f.ChangeDutyCycle(0)
        motor4_f.ChangeDutyCycle(0)
        GPIO.output(GPIO_SERVO, False)
        GPIO.output(GPIO_MOTOR1_IN1, False)
        GPIO.output(GPIO_MOTOR1_IN2, False)
        GPIO.output(GPIO_MOTOR2_IN1, False)
        GPIO.output(GPIO_MOTOR2_IN2, False)
        GPIO.output(GPIO_MOTOR3_IN1, False)
        GPIO.output(GPIO_MOTOR3_IN2, False)
        GPIO.output(GPIO_MOTOR4_IN1, False)
        GPIO.output(GPIO_MOTOR4_IN2, False)
        GPIO.output(GPIO_TRIGGER, False)
       
        GPIO.cleanup()
        
class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
    
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        
    # Use the read method of the VideoCapture class to get a frame from the video source
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
        


# Create a window and pass it to the Application object
print("程序启动中，请稍等...")
App(tkinter.Tk(), "视频窗口")
  
            