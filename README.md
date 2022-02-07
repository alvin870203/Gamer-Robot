# Gamer Robot: Applying Pikaliya Chess Algorithm on a TM5-900 Robot Arm with an RGB camera
機器人學 | Robotics | 傅立成教授 | 2020 Spring

## Demo Video

https://user-images.githubusercontent.com/57071722/152855695-99cc6d42-2a28-4f54-8f12-5cf0a8739fbf.mp4

## Goal:
We propose a Gamer Robot that can play Pikaliya chess with humans. The rule of Pikaliya chess is a combination of Tic-Tac-Toe and Gomoku. Generally, two players are required. However, with Gamer Robot, even a single person can play.

## Implementation
With ROS camera calibration toolkits and OpenCV library. 
The robot can obtain the correct camera coordinates for the chess pieces.
Then, an accurate frame transformation matrix enables the robot to reach the target piece.
Combine the above techniques with the Pikaliya chess algorithm, which separates into placing and moving sub-algorithm.
