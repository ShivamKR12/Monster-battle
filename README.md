# 🐉 Monster Battle ⚔️

[![Build Status](https://github.com/ShivamKR12/Monster-battle/actions/workflows/build.yml/badge.svg)](https://github.com/ShivamKR12/Monster-battle/actions/workflows/build.yml)
[![Latest Release](https://img.shields.io/github/v/release/ShivamKR12/Monster-battle?label=Latest%20Release)](https://github.com/ShivamKR12/Monster-battle/releases/latest)

A fully-featured, turn-based monster battling game built in Python using **Pygame-CE**. Assemble your team, master the elemental type matchups, and defeat your opponents to achieve victory!

## ✨ Features

- **Turn-Based Combat:** Classic RPG-style battling system.
- **Elemental Matchups:** Strategic combat featuring Fire, Water, Plant, and Normal types. 
- **Roster Management:** Switch dynamically between your active team of monsters during battle.
- **Animations & Audio:** Animated attack sprites, screen shakes, and engaging sound effects.
- **Dynamic UI:** Intuitive, grid-based menus with dynamic health bars and battle logs.
- **Fullscreen Experience:** Scales seamlessly to your native display resolution.

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **Arrow Keys (↑ ↓ ← →)** | Navigate menus / Select monsters and attacks |
| **Spacebar** | Confirm selection / Action |
| **ESC** | Go back (in menus) / Quit Game (from main or end screen) |

## 🚀 How to Play (Standalone Executable)

If you have downloaded the `.exe` version of the game:
1. Simply double-click `MonsterBattle.exe` (or `main.exe`).
2. The game will launch in fullscreen mode automatically. No installation required!

## 🛠️ How to Run from Source

If you want to run or modify the game's Python source code, follow these steps:

1. **Clone or Download** this repository.
2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   # source venv/bin/activate # Mac/Linux
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Game:**
   ```bash
   python code/main.py
   ```

## 📦 Building the Executable

To compile the game into a standalone `.exe` using PyInstaller, run the following command from the root project directory:

```bash
pyinstaller --noconsole --onefile --add-data "images;images" --add-data "audio;audio" code\main.py
```

*The compiled game will be generated inside the `dist` folder.*
