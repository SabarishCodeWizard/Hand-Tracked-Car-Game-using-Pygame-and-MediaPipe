

# Car Game with Hand Tracking

This is a simple car game implemented in Python using Pygame for graphics and MediaPipe for hand tracking. The player controls the car using hand gestures detected via the webcam.

## Features

- Control the car using hand gestures detected via webcam.
- Dodge obstacles and collect power-ups to increase score.
- Power-ups include invincibility, speed boost, and extra points.
- Dynamic obstacle generation within road boundaries.
- Speed increases over time for added challenge.
- Real-time hand landmark tracking and gesture recognition.

## Requirements

- Python 3.x
- Pygame
- OpenCV (cv2)
- MediaPipe

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SabarishCodeWizard/Hand-Tracked-Car-Game-using-Pygame-and-MediaPipe.git
   cd car-game
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:

   ```bash
   python car.py
   ```

## How to Play

- Start the game and place your hand in front of the webcam.
- Move your hand to control the car's position on the screen.
- Dodge thunder obstacles, spaceships, and collect power-ups to increase your score.
- Game ends when the car collides with an obstacle (unless invincibility is active).

## Controls

- **Hand Gestures**: Control the car by moving your hand in front of the webcam.

## Power-Ups

- **Invincibility**: Makes the car invincible for a short period.
- **Speed Boost**: Increases the car's speed temporarily.
- **Extra Points**: Instantly increases the score.

## Game Mechanics

- **Obstacle Generation**: Obstacles are generated within the defined road boundaries to ensure they appear on the road.
- **Speed Increment**: The speed of the car and obstacles increases at regular intervals to add difficulty.
- **Collision Detection**: Collisions with obstacles end the game, unless the invincibility power-up is active.
- **Score**: Score increases over time and with certain power-ups.

## Credits

- Images and music,videos used in the game are sourced from various free asset websites.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
