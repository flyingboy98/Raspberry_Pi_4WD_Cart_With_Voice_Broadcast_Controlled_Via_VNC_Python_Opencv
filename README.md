　　用树莓派作主板的四轮驱动小车，通过VNC来控制，有语音播放功能。Python编程。



主要特点：

　　＊四轮驱动，动力强，可载重二十公斤。

　　＊前进，后退，转向灵活行驶。

　　＊手动五档位(包括倒档)。车轮直径越大速度越快。

　　＊树莓派连接USB摄像头，捕捉实时影像，上位机通过VNC远程遥控。

　　＊树莓派音频输出到功放模块，由扬声器播放。通过TTS(text-to-speech),
可实现远程语音播放。

　　＊前后和下方均安装传感器，可自动避障和人为干扰提醒。

　　＊图形操作界面。可显示摄像头传回的影像(略有延迟)以及档位，摄像头方向，操
作提醒等信息。根据上位机设备类型，可选择通过触屏点击，鼠标，键盘，游戏杆等来
控制。



主要硬件：

　　＊Raspberry Pi 3或4。

　　＊USB摄像头。

　　＊12v蓄电池。安时数越高使用时间越长，但重量也越大。本例采用20AH(长宽高20*8*18cm，大约6Kg)。

　　＊180度伺服电机(舵机)。用于控制摄像头转向。型号：SG90。

　　＊直流电机＋支架 x 4。要求速度选择高速电机，要求载重选择减速大扭力电机。
本例使用的是JGB37-520减速电机，12v，额定转数140转/分钟，额定电流1A，堵转
电流2.3A，额定扭力6.5Kg，最大扭力9Kg，轴径6mm，轴长22mm。

　　＊电机控制模块 x 2。型号：L298N。

　　＊直流降压模块 x 2。型号：LM2596S。用于树莓派和网络模块。

　　＊微型直流降压模块。功能同上，体积小，只有22*17mm。用于功放等其它设备。

　　＊2*3W功放模块。型号：D类PAM8403，输入电压3-5V。

　　＊超声波距离传感器。型号：HC-SR04。

　　＊红外距离传感器 x 2。

　　＊扬声器。型号：8欧，直径4cm，0.5W。

　　＊3.5mm耳机插头连接线。用于从Pi输出音频到功放模块。

　　＊网络模块。接入互联网用4G路由器.如果只用于wifi环境，可用移动无线路由或
将Pi上的wifi模块设置为热点。

　　＊Pi GPIO 40P排线。两端都是双排母痤。用于将各种设备连接至Pi GPIO。

　　＊USB母座 x ４。分别用于树莓派，网络模块和其它设备供电。

　　＊2P连接头 x 3(副)。用于连接降压模块和USB母座，如直接焊接可不用。26AWG
的电线。

　　＊2P电源连接头(副)。用于连接蓄电池和主供电电路板。20或22AWG的电线。

　　＊6mm法兰盘联轴器　x 4。用于连接电机和车轮。

　　＊５*7cm电路板 x 2。

　　＊1P排针若干。型号：2.54mm。用于将降压模块，功放模块等焊接在一块电路板
上。

　　＊六角尼龙柱若干。型号：M2*20,M3*20。

　　＊26AWG电线，面包板，跳线，杜邦线，各种螺丝，连接件若干。

　　＊烙铁，焊锡等焊接设备和万用表，M2,M3钻头，螺丝刀，锯等工具。

　　＊车体：为减轻车身自重，全部使用木质材料。

　　　　　　尺寸50*30*27.5cm(长＊宽＊高)，车轮直径15cm。

　　　　　　底盘木方+木板：50*2*2木方 x 3，30*2*2木方 x 4，30*50*3木板。

　　　　　　车厢木板：20*50 x 2，20*29.4 x 3，10*30 x 1。



制作组装：

　　＊制作12V主供电电路。将一块5*7电路板切割成两块，其中一块要能并列摆放四
个USB母座。在另一块上将20(或22)AWG电线的连接头焊接在电路板的两端作为主电
源正负极，做好标记。连接头另一端连接至蓄电池正负极。

　　在主电源电路板上引出两组12V26AWG电源线，分别连接到两个电机控制模块的电
机供电接口，注意正负极。



　　＊制作调试降压电路。在一块5*7电路板上。用单排针焊接固定三个降压模块和功
放模块。并分别从降压模块的输入端引出导线焊接至主供电电路板的正负极，输出端分
别引出26AWG线的2P连接头。

　　检查接线和正负极是否正确，确定无误后接通蓄电池与主供电电路板的2P接头，用
万用表分别测量降压模块的输出电压并用小螺丝刀调试输出电压至4V。调试完毕后断开
主电源连接。

　　从一个降压模块的输出端引出导线焊接至功放模块的供电端，将3.5mm耳机插头线
焊接至功放模块的音频输入端。从功放模块的音频输出左或右任一声道引出导线焊接到
扬声器上，注意正负极，接反声音非常小。

　　请按以上顺序操作！



　　＊制作USB供电电路。从主供电电路板切割下来的另一块电路板上焊接四个USB母
座，并分别在USB供电接头焊接三个26AWG线的2P连接头(降压电路板上三个连接头的
另一端)。其中两根分别连接两个USB母座，用于Pi和网络模块单独供电；一根连接两
个并联的USB母座，与功放模块共用一个降压模块，为其它设备供电。关于USB接头顺
序，请查阅相关资料。



　　＊在四个电机上焊接导线，另一端分两组分别连接至两块电机控制板上的电机接口，
不用注意极性，软件可调。



　　＊将Pi GPIO 40P双排母座一端插到Pi上，另一端用杜邦线连接其它设备，注意
端口顺序，最好做标记。从Pi上分别引出+5V, +3V和接地(Ground)三根线到一块小
面包板，与其它设备共用。以下GPIO序号均为GPIO号(BCM)，不是板载序号(BOARD).
主要连接的设备：

　　接地(Ground)，分别连接到两块电机控制板的接地端(Ground)。

　　伺服电机三根线，红线连接+5V，棕线接地(Ground)，桔线PWM接GPIO 17

　　电机控制板电机1：GPIO 16, 19

　　电机控制板电机2：GPIO 20, 26

　　电机控制板电机3：GPIO 10, 9

　　电机控制板电机4：GPIO 8, 7

　　超声波距离传感器：ECHO接GPIO 23，TRIGGER接GPIO 24

　　红外距离传感器：两个的供电端接+3V和接地(Ground)。数据端，安装在车尾
部的接GPIO 4，车底部的接GPIO 18

　　＊至此，电路部分完成。反复仔细检查线路，正负极，无误后准备调试。



软件环境：

　　＊系统Raspberry Pi OS(Rasbian).

　　　sudo apt update

　　　sudo apt upgrade



　　＊安装系统支持文件:

　　　sudo apt install python-pip python3-pip python-pyaudio python3-pyaudio pulseaudio libpulse-dev libportaudio2 mplayer

　　　sudo -H pip3 install --upgrade pip

　　　sudo pip3 install RPi.GPIO

　　　sudo pip3 install pyttsx3

　　　sudo usermod -aG gpio pi

　　　sudo usermod -aG video pi

　　　sudo usermod -aG audio pi



　　＊安装Opencv4.4：编译。

　　　sudo apt install cmake gfortran libjpeg-dev libtiff-dev libgif-dev libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libgtk-3-dev libxvidcore-dev libx264-dev libgtk-3-dev libtbb2 libtbb-dev libdc1394-22-dev libv4l-dev libopenblas-dev libatlas-base-dev libblas-dev libopenblas-dev libatlas-base-dev libblas-dev libopenblas-dev libatlas-base-dev libblas-dev



　　　cd ~

　　　wget -O opencv.zip https://github.com/opencv/opencv/archive/4.４.0.zip

　　　wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.3.0.zip



　　　unzip opencv.zip

　　　unzip opencv_contrib.zip



　　　mv opencv-4.3.0 opencv

　　　mv opencv_contrib-4.3.0 opencv_contrib



　　　cd ~/opencv/

　　　mkdir build

　　　cd build



　　　sudo vi /etc/hosts

　　　添加：

　　　151.101.108.133 raw.githubusercontent.com

　　　(上面的数字IP可以通过IP查询网站，查找raw.githubusercontent.com，
会出现多个数字IP，用ping命令选择最快的。)

　　　保存退出。



　　　sudo apt update

　　　sudo apt upgrade



　　　联网状态下执行：

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D WITH_OPENMP=ON \
      -D BUILD_TIFF=ON \
      -D WITH_FFMPEG=ON \
      -D WITH_GSTREAMER=ON \
      -D WITH_TBB=ON \
      -D BUILD_TBB=ON \
      -D BUILD_TESTS=OFF \
      -D WITH_EIGEN=OFF \
      -D WITH_V4L=ON \
      -D WITH_LIBV4L=ON \
      -D WITH_VTK=OFF \
      -D WITH_QT=OFF \
      -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D BUILD_NEW_PYTHON_SUPPORT=ON \
      -D BUILD_opencv_python3=TRUE \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D BUILD_EXAMPLES=OFF ..

　　如果出错，重新执行。如果是由于下载组件失败，查看上面修改hosts的内容是否
有效。



　　　临时修改交换文件大小：

　　　sudo nano /etc/dphys-swapfile

　　　CONF_SWAPSIZE = 2048

　　　保存退出

　　　sudo /etc/init.d/dphys-swapfile stop

　　　sudo /etc/init.d/dphys-swapfile start



　　　模拟四核CPU执行make命令，这一步在Pi4 4G版上大约耗时35分钟。

　　　make -j4



　　　sudo make install

　　　sudo ldconfig

　　　sudo apt update



　　　改回交换文件大小：

　　　sudo nano /etc/dphys-swapfile

　　　CONF_SWAPSIZE=100


　　　cd ~

　　　rm opencv.zip

　　　rm opencv_contrib.zip

　　　reboot



　　＊安装本软件：

　　　cd /home/pi/Documents
 
　　Pi3下载简版：

　　wget -O 4WD_Cart_Pi3_Lite.py https://github.com/flyingboy98/Raspberry_Pi_4WD_Cart_With_Voice_Broadcast_Controlled_Via_VNC_Python_Opencv/raw/main/4WD_Cart_Pi3_Lite.py

　　Pi4下载完整版：

　　wget -O 4WD_Cart_Pi4_Full.py https://github.com/flyingboy98/Raspberry_Pi_4WD_Cart_With_Voice_Broadcast_Controlled_Via_VNC_Python_Opencv/raw/main/4WD_Cart_Pi4_Full.py

　　下载背景图片，也可以用其它自己喜欢的(分辨率800*700, png格式)：

　　wget -O bg.png https://github.com/flyingboy98/Raspberry_Pi_4WD_Cart_With_Voice_Broadcast_Controlled_Via_VNC_Python_Opencv/raw/main/bg.png

　　下载简化版余音，只保留了汉语普通话。完整版请到余音官网下载(www.eguidedog.net/cn/ekho_cn.php)。

　　wget -O yy.zip https://github.com/flyingboy98/Ekho_Mandarin_Only/raw/main/yy.zip

　　unzip yy
.zip
　　sudo rm yy.zip
　　建立小车脱离地面时的语音提醒，自行录制：

　　touch if001.mp3
　　cd ~



调试：Pi直接连接外设进行调试。主要是调整四个电机的运转方向，使其协调一致。

　　　例如想改变电机1运转方向，在py文件中将：

　　　GPIO_MOTOR1_IN1 = 16

　　　GPIO_MOTOR1_IN2 = 19

　　　改为：

　　　GPIO_MOTOR1_IN1 = 19

　　　GPIO_MOTOR1_IN2 = 16



车体组装：重点在于四个电机支架的位置，也就是四轮定位！首先，四个支架之
间的距离误差要尽量小，宽度要测量支架侧面前缘之间和后缘之间的距离是否一致；其
次尽量做到前后两个电机支架的侧面在一个平面上。

　　　    所有固定螺丝的螺母和螺帽两端都要加垫片。

　　　    底盘用M3钻头开孔，用M3*50的螺丝固定。

　　　    车厢用M2钻头开孔，用M2*8的螺丝和L型连接片固定。



使用：Pi上开启real-vnc-server，上位机用real-vnc-viewer接入Pi。如果只
在wifi环境下使用，简单进行局域网IP设置即可连接；如果接入互联网，在real-vnc
注册云帐号，登陆后连接。


