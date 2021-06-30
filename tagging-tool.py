from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl, QTime


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 300, 800, 500)
        self.setWindowIcon(QIcon('player.png'))
        self.tagging = False
        self.timeStamps = []
        self.curTimeStamp = []
        self.filename = ""

        p = self.palette()
        p.setColor(QPalette.Window, Qt.gray )
        self.setPalette(p)

        self.init_ui()


        self.show()


    def init_ui(self):

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        #create videowidget object

        videowidget = QVideoWidget()


        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)



        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.tagBtn = QPushButton("Start Tagging")
        self.tagBtn.setEnabled(True)
        self.tagBtn.clicked.connect(self.tag_video)

        self.finishBtn = QPushButton("finish")
        self.finishBtn.clicked.connect(self.finish_tagging)


        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(200,0)
        self.slider.sliderMoved.connect(self.set_position)



        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(self.tagBtn)
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.finishBtn)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)


        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)


        #media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def tag_video(self):
        if not self.tagging:
            self.tagging = True
            self.tagBtn.setText("Finish Tagging")
            position = self.mediaPlayer.position()
            timeStamp = self.get_time_format(position)
            self.curTimeStamp.append(timeStamp)
        else:
            self.tagging = False
            self.tagBtn.setText("Start Tagging")
            position = self.mediaPlayer.position()
            timeStamp = self.get_time_format(position)
            self.curTimeStamp.append(timeStamp)
            # print(self.curTimeStamp)
            self.timeStamps.append(self.curTimeStamp)
            self.curTimeStamp = []

    def get_time_format(self, duration):
        timeStamp = ""
        hours = int((duration / 3600000) % 24)
        if hours // 10 == 0:
            timeStamp += "0"
        timeStamp += str(hours) + ":"
        minutes = int((duration / 60000) % 60)
        if minutes // 10 == 0:
            timeStamp += "0"
        timeStamp += str(minutes) + ":"
        seconds = int((duration / 1000) % 60)
        if seconds // 10 == 0:
            timeStamp += "0"
        timeStamp += str(seconds) + ","
        milisec = int(duration % 1000)
        timeStamp += str(milisec)
        return timeStamp

    def finish_tagging(self):
        if self.filename != "":
            with open(self.filename.split('.')[0] + ".cnsr","w")as file:
                for timestamp in self.timeStamps:
                    file.write(timestamp[0] + " - " + timestamp[1] + ";1 \n")
        exit()

    def open_file(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if  self.filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.filename)))
            self.playBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())





app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())