import sys
import os
from PyQt6.QtWidgets import ( QSizePolicy,QGraphicsDropShadowEffect,QFrame, QApplication, QWidget, 
                             QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QGroupBox, QGraphicsOpacityEffect, QSizePolicy )
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QIcon, QPen, QColor
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QPointF,QRectF, QRect
import psutil, socket, uuid

from PyQt6.QtGui import QFont, QPalette

class NetworkPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0d1b16; border-radius: 15px;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Network Monitor")
        title.setStyleSheet("color: #00ffcc; font: 18pt 'JetBrains Mono'; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Main Grid Layout
        grid = QGridLayout()
        grid.setSpacing(20)

        # Upload/Download Section (Left)
        traffic_frame = QFrame()
        traffic_frame.setStyleSheet("background-color: #05130e; border: 1px solid #00ffcc; border-radius: 10px;")
        traffic_layout = QVBoxLayout(traffic_frame)

        self.upload_arrow = QLabel("↑")
        self.download_arrow = QLabel("↓")
        for arrow in [self.upload_arrow, self.download_arrow]:
            arrow.setStyleSheet("color: #00ffcc; font: 24pt 'JetBrains Mono';")
            arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.upload_label = QLabel("Upload: 0 KB/s")
        self.download_label = QLabel("Download: 0 KB/s")

        for lbl in [self.upload_label, self.download_label]:
            lbl.setStyleSheet("color: #ccffcc; font: 12pt 'Consolas';")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        traffic_layout.addWidget(self.upload_arrow)
        traffic_layout.addWidget(self.upload_label)
        traffic_layout.addWidget(self.download_arrow)
        traffic_layout.addWidget(self.download_label)
        grid.addWidget(traffic_frame, 0, 0)

        # Info Panel (Right)
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #05130e; border: 1px solid #00ffcc; border-radius: 10px;")
        info_layout = QVBoxLayout(info_frame)

        self.ip_label = QLabel(f"IP Address: {self.get_ip()}")
        self.mac_label = QLabel(f"MAC Address: {self.get_mac()}")
        self.gw_label = QLabel(f"Gateway: {self.get_gateway()}")

        for lbl in [self.ip_label, self.mac_label, self.gw_label]:
            lbl.setStyleSheet("color: #ccffcc; font: 11pt 'Consolas'; padding: 6px;")
            info_layout.addWidget(lbl)

        grid.addWidget(info_frame, 0, 1)

        main_layout.addLayout(grid)

        # Timers for speed updates
        self.prev_bytes_sent = psutil.net_io_counters().bytes_sent
        self.prev_bytes_recv = psutil.net_io_counters().bytes_recv

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(1000)

    def update_speed(self):
        counters = psutil.net_io_counters()
        sent = counters.bytes_sent
        recv = counters.bytes_recv

        upload_kb = max(0, (sent - self.prev_bytes_sent) / 1024)
        download_kb = max(0, (recv - self.prev_bytes_recv) / 1024)

        self.upload_label.setText(f"Upload: {upload_kb:.2f} KB/s")
        self.download_label.setText(f"Download: {download_kb:.2f} KB/s")

        self.prev_bytes_sent = sent
        self.prev_bytes_recv = recv
    def showEvent(self, event):
        super().showEvent(event)
        self.animate_arrow(self.upload_arrow)
        self.animate_arrow(self.download_arrow)

    def animate_arrow(self, label):
        effect = QGraphicsOpacityEffect()
        label.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(1000)
        anim.setStartValue(0.3)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.setLoopCount(-1)
        anim.start()
        label.animation = anim  # Keep reference

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"

    def get_mac(self):
        mac = hex(uuid.getnode()).replace('0x', '').upper()
        return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

    def get_gateway(self):
        try:
            gws = psutil.net_if_addrs()
            for iface, addrs in gws.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        return addr.address
            return "Unknown"
        except:
            return "Unknown"

class MyOS(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eliot OS - Hacker Edition")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: black; color: white;")
        self.apps_visible = False

        # === MAIN CONTAINER ===
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, self.width(), self.height())

        # === MAIN LAYOUT ===
        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # === GRID UI (Equal 4 Panels) ===
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        def create_panel(name):
            label = QLabel(name)
            label.setStyleSheet(f"""
                background-color: #111;
                border: 2px solid green;
                border-radius: 15px;
                color: green;
                font: bold 16px 'Segoe UI';
                padding: 20px;
            """)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            return label

        self.grid.addWidget(NetworkPanel(), 0, 0)
        self.grid.addWidget(create_panel("File Explorer"), 0, 1)
        self.grid.addWidget(create_panel("System Monitoring"), 1, 0)
        self.grid.addWidget(create_panel("Weather + Alerts"), 1, 1)

        # Set stretch so all 4 squares fill equally
        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

        self.main_layout.addLayout(self.grid)

        # === APP LAUNCH BUTTONS (hidden/animated) ===
        self.app_buttons = []

        tools = {
            "Kali": "~/.launch_kali.sh",
            "Parrot": "~/.launch_parrot.sh",
            "BlackArch": "~/.launch_blackarch.sh",
            "BackBox": "~/.boot_backbox.sh",
            "Pentoo": "~/.boot_pentoo.sh",
            "Tails": "~/.boot_tails.sh",
            "DEFT": "~/.launch_deft.sh",
            "CAINE": "~/.launch_caine.sh",
        }

        def circular_icon(path, size=64):
            pixmap = QPixmap(path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            masked = QPixmap(size, size)
            masked.fill(Qt.GlobalColor.transparent)

            painter = QPainter(masked)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            path_circle = QPainterPath()
            path_circle.addEllipse(0, 0, size, size)
            painter.setClipPath(path_circle)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()

            return QIcon(masked)

        for name, script in tools.items():
            btn = QPushButton(self.container)
            btn.setIcon(circular_icon(f"icons/{name.lower()}.png"))
            btn.setIconSize(QSize(50, 50))
            btn.setFixedSize(55, 55)
            btn.setToolTip(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    border-radius: 25px;
                }
                QPushButton:hover {
                    background-color: red;
                }
            """)
            btn.clicked.connect(lambda _, s=script: os.system(f"bash {s} &"))
            btn.hide()
            self.app_buttons.append(btn)

        # === TASKBAR WITH MAIN LAUNCH BUTTON ===
        self.taskbar = QHBoxLayout()
        self.taskbar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.launch_btn = QPushButton()
        self.launch_btn.setIcon(circular_icon("icons/launch.png"))
        self.launch_btn.setIconSize(QSize(41, 41))
        self.launch_btn.setStyleSheet("""
            QPushButton {
                background-color: green;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        self.launch_btn.clicked.connect(self.toggle_apps)
        self.taskbar.addWidget(self.launch_btn)

        self.main_layout.addLayout(self.taskbar)

    def toggle_apps(self):
        self.apps_visible = not self.apps_visible

        launch_center_x = self.launch_btn.x() + self.launch_btn.width() // 2
        launch_center_y = self.container.height() - 40

        button_size = 55
        spacing = 20
        total_width = len(self.app_buttons) * button_size + (len(self.app_buttons) - 1) * spacing
        start_x = launch_center_x - total_width // 2
        final_y = self.container.height() - 100

        if self.apps_visible:
            for i, btn in enumerate(self.app_buttons):
                final_x = start_x + i * (button_size + spacing)
                start_x_pos = launch_center_x - button_size // 2
                start_y_pos = launch_center_y - button_size // 2

                btn.setGeometry(start_x_pos, start_y_pos, button_size, button_size)
                btn.setVisible(True)
                btn.raise_()

                anim = QPropertyAnimation(btn, b"pos", self)
                anim.setDuration(400)
                anim.setStartValue(QPoint(start_x_pos, start_y_pos))
                anim.setEndValue(QPoint(final_x, final_y))
                anim.setEasingCurve(QEasingCurve.Type.OutBack)
                QTimer.singleShot(i * 80, anim.start)
        else:
            for i, btn in enumerate(self.app_buttons):
                current_pos = btn.pos()
                end_x = launch_center_x - button_size // 2
                end_y = launch_center_y - button_size // 2

                anim = QPropertyAnimation(btn, b"pos", self)
                anim.setDuration(400)
                anim.setStartValue(current_pos)
                anim.setEndValue(QPoint(end_x, end_y))
                anim.setEasingCurve(QEasingCurve.Type.InBack)

                def hide_btn(b=btn):
                    b.setVisible(False)

                QTimer.singleShot(i * 80, anim.start)
                QTimer.singleShot(400 + i * 80, hide_btn)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container.setGeometry(0, 0, self.width(), self.height())
        if self.apps_visible:
            self.toggle_apps()
            QTimer.singleShot(10, self.toggle_apps)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyOS()
    window.showFullScreen()  # Fullscreen-like
    sys.exit(app.exec())