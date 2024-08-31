# Advanced Soccer Game - README

## Overview
"Advanced Soccer Game" is a 2D sports game developed using the LÖVE framework. The game simulates a soccer match between two paddles, where the player controls the left paddle and competes against an AI-controlled right paddle. The objective is to score points by hitting the ball past the opponent's paddle until one player reaches the winning score.

## Features
- **Single Player Mode**: Play against an AI opponent with adjustable difficulty levels.
- **Dynamic Gameplay**: The ball's speed and angle change dynamically based on collisions, creating an engaging and unpredictable experience.
- **Power-Ups**: Randomly spawning power-ups enhance gameplay by increasing the ball's speed, adding an extra layer of challenge.
- **Particle Effects**: Collisions and events are visually enhanced with particle effects.
- **Pause and Resume**: The game can be paused and resumed using the 'P' key.

## Controls
- **Left Paddle (Player)**
  - Move Up: `W`
  - Move Down: `S`
  - Boost Speed: `Left Shift`
- **Game Controls**
  - Pause/Resume: `P`
  - Enter Name/Start Game: `Enter`
  - Delete Character in Name Input: `Backspace`

## Getting Started
1. **Prerequisites**: 
   - Install the LÖVE framework from [love2d.org](https://love2d.org/).
   
2. **Running the Game**:
   - Run the `main.lua` file in the LÖVE framework to start the game.
   
3. **Gameplay**:
   - On launch, enter your player name and press `Enter` to start the match.
   - Control the left paddle using the `W` and `S` keys to move up and down.
   - Press `Left Shift` for a temporary speed boost.
   - The game ends when either player reaches the winning score.

## Game Rules
- **Scoring**: Each time the ball passes a player's paddle, the opponent scores a point.
- **Winning Condition**: The first player to reach the winning score of 5 points wins the match.
- **Power-Ups**: Power-ups randomly appear on the field and enhance the ball's speed when collected.

## Game Modes
- **Single Player**: Compete against the AI, which adjusts its difficulty based on game settings.

## Customization
- Modify the `winningScore`, `paddleWidth`, `paddleHeight`, and other game parameters in the `love.load()` function to customize gameplay.
- Adjust AI difficulty by modifying the `rightPaddle.difficulty` variable in the `love.load()` function.
