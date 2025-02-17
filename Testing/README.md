# IFS DriverAlert Testing Documentation

Below is a description of the testing documents in this directory:

### `1stSemesterTestingDoc.pdf`

- This document has the initial testing which was done on the first stage of the project.
- It contains some user testing based on the initial implementation.

### `IFS_BoundaryValueTesting.pdf`

- This document has the BoundaryValueTesting, which shows various detection features (eyes closed, yawning, looking away, multi-face detection, and auto detection activation).
- Each table presents test cases with boundary conditions, detected values, and expected results to ensure the system correctly identifies conditions at, below, and above the set thresholds.
- The tests verify that the system behaves correctly under edge cases, improving reliability in real world applications.

### `IFS_DecisionTableTesting.pdf`

- This document shows Decision Table for the IFS system, which shows different conditions (closed eyes, yawning, looking away) to corresponding alert actions.
- It defines condition stubs (C1, C2, C3) for detection and action stubs (A1, A2, A3) for triggering alerts, with rules indicating when alerts should be triggered.

### `IFS_EquivalenceClassTesting.pdf`

- This document shows the Equivalence Class Testing, which test various input conditions to maximize coverage.
- It categorizes test functions conducted in [test_tflite.py](https://github.com/ferasaljoudi/Capstone/blob/main/Code/RaspberryPi5/test_tflite.py) and [test_mediapipe.py](https://github.com/ferasaljoudi/Capstone/blob/main/Code/RaspberryPi5/test_mediapipe.py).

### `IFS_IntegrationTesting.pdf`

- This document shows the Integration Testing, which make sure key components interact correctly to detect drowsiness indicators and trigger alerts.
- It categorizes test functions conducted in [test_tflite.py](https://github.com/ferasaljoudi/Capstone/blob/main/Code/RaspberryPi5/test_tflite.py) and [test_mediapipe.py](https://github.com/ferasaljoudi/Capstone/blob/main/Code/RaspberryPi5/test_mediapipe.py).

