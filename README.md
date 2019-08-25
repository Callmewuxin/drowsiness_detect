# Description
1. Drowsiness detection based on EAR
2. EAR based on dlib's facial landmark

# Feature
1. *.py file for detect drowsiness step by step
2. run video_drowniess_detect.py, when detect drowsiness, serial sends alarm and arduino starts vibrated.

# heart beat for detection
1. bluetooth.py for collect heart beat data 10ms, 500 per sample.
2. drowsiness detection using heart beat is limited by data scales and simple device
3. Conv1D network was utilized to end-to-end classify drowsiness state and awake state
4. validation accuracy reaches 100%, but loss curve shows no convergence