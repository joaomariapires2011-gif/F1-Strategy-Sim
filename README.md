# 🏎️ F1 Strategy & Pit Window Simulator

A Python-based simulation engine designed to evaluate Formula 1 race strategies, tire degradation models, and pit stop time loss calculations.

![Continuous Integration](https://github.com/joaomariapires2011-gif/F1-Strategy-Sim/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📌 Features

* **Tire Degradation Modeling:** Simulates exponential pace loss on Soft, Medium, and Hard compounds based on stint length.
* **Pit Stop Delta Evaluation:** Calculates net race time including pit lane delta loss (e.g., 22.5s at Monza).
* **Strategy Comparison Engine:** Ranks 1-stop vs 2-stop strategies by overall race completion time.

## 🚀 Usage

```bash
python f1_strategy_sim.py
