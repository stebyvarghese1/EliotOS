# 🧪 EliotOS (Ongoing Not completed)

**EliotOS** is a fully customizable Python-based desktop environment designed for cybersecurity enthusiasts, ethical hackers, and power users. Built using PyQt6, it mimics an operating system UI with real-time network monitoring, hacking distro launchers, system panels, and dynamic animations — all in a sleek hacker-themed interface.

---

## 🖥️ Features

- ⚙️ **Desktop Grid Layout** with 4 Panels:
  - 📡 Network Monitor
  - 🗂️ File Explorer (placeholder)
  - 📊 System Monitor (placeholder)
  - 🌦️ Weather & Alerts (placeholder)
- 🚀 **Live Launchers** for:
  - Kali, Parrot, BlackArch, BackBox, Pentoo, Tails, DEFT, CAINE
- 🧪 **Real-Time Network Panel**:
  - Upload/Download Speed (live)
  - IP, MAC, Gateway Info
- 🎨 **Custom GUI** with:
  - Fullscreen, animated buttons
  - Circular icons
  - Hacker-themed dark style
- 🧲 Hidden App Dock that toggles with animation

---

## 📂 File Structure

```

.
├── app.py                 # Main app entry point
├── icons/               # Folder containing PNG icons for launch buttons
│   ├── kali.png
│   ├── parrot.png
│   └── ...etc
├── \~/.launch\_kali.sh    # Launcher scripts to be created by user
└── README.md

````

---

## 🧰 Requirements

- Python 3.8+
- PyQt6
- psutil

---

## 🔧 Setup & Run

1. **Install requirements:**

```bash
pip install PyQt6 psutil
````

2. **Ensure launcher scripts exist** in your home directory:

```bash
touch ~/.launch_kali.sh ~/.launch_parrot.sh
chmod +x ~/.launch_*.sh
```

> Modify each script to launch the actual ISO, VM, or shell app.

3. **Run EliotOS:**

```bash
python app.py
```

---

## 🔒 Security Notes

This OS-like UI is meant for educational and hobby use. Launcher scripts and system access should be handled with care and proper permissions.

---

## 📸 Preview

![elio](https://github.com/user-attachments/assets/0ea7de85-c362-491d-a60e-8d5c40d64cbb)


## 🙌 Credits

* Developed by **Steby Varghese**
* Built using Python + PyQt6

```
