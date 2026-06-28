# 🪵 Board Feet Cost Calculator

A simple Streamlit app for figuring out what your lumber is going to cost — calculated properly by board feet, not just guessed at. Built for handling a stack of boards at once, even when they're all different sizes.

## Features

- Add as many boards as you need, each with its own thickness, width, length, quantity, and price per board foot
- Automatic board foot math: `(Thickness × Width × Length) / 12`
- Per-board breakdown table plus running totals for board feet and cost
- A built-in, collapsible explainer for anyone new to what a "board foot" actually is
- Warm, wood-toned theme

## Running it locally

```bash
pip install -r requirements.txt
streamlit run board_feet_calculator.py
```

It'll open automatically in your browser.

## The math

A board foot is a unit of volume, not just length — it's how lumber yards price hardwood. One board foot equals a piece of wood 12" long × 12" wide × 1" thick (144 cubic inches). This app takes your board's actual thickness, width, and length and works out exactly how many board feet you're buying.

## Built with

- [Streamlit](https://streamlit.io)
