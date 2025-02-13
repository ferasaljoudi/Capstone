import time
import unittest
from collections import namedtuple

from eye_detection_mediapipe import (alert_func, calculate_eye_ratio,
                                     calculate_face_turn_ratio,
                                     calculate_mouth_ratio, detect_signs)

Landmark = namedtuple("Landmark", ["x", "y"])

class TestDrowsinessDetection(unittest.TestCase):
    def test_valid_eye_ratio(self):
        # Simulate valid eye landmarks
        eye_coords = [
            (30, 60),  # Top point
            (30, 20),  # Bottom point
            (0, 40),   # Left point
            (60, 40)   # Right point
        ]
        # Vertical / Horizontal * 100
        expected_ratio = (40 / 60) * 100
        result = calculate_eye_ratio(eye_coords)
        self.assertAlmostEqual(result, expected_ratio, places=2)

    def test_nonvalid_eye_ratio(self):
        # Simulate invalid eye landmarks (missing points)
        eye_coords = [
            (30, 60),  # Top point
            (30, 20),  # Bottom point
            (0, 40)   # Left point
        ]
        # Expected result is 100 since it is missing coords
        result = calculate_eye_ratio(eye_coords)
        self.assertEqual(result, 100)

    def test_valid_mouth_ratio(self):
        # Simulate valid mouth landmarks
        upper_lip = (20, 40)
        lower_lip = (20, 10)
        left_lip = (0, 25)
        right_lip = (40, 25)
        # Vertical / Horizontal * 100
        expected_ratio = (30 / 40) * 100
        result = calculate_mouth_ratio(upper_lip, lower_lip, left_lip, right_lip)
        self.assertAlmostEqual(result, expected_ratio, places=2)
        
    def test_nonvalid_mouth_ratio(self):
        # Simulate non valid mouth landmarks
        upper_lip = (20, 40)
        lower_lip = (20, 10)
        left_lip = (40, 25)
        right_lip = (40, 25)
        # Horizontal distance will be 0 which is not allowed
        with self.assertRaises(ValueError) as context:
                calculate_mouth_ratio(upper_lip, lower_lip, left_lip, right_lip)
        # Verify the error message
        self.assertEqual(str(context.exception), "Horizontal distance can not be zero.")
        
    def test_valid_turn_ratio(self):
        # Simulate valid face landmarks
        left_eyebrow = Landmark(20, 40)
        right_eyebrow = Landmark(30, 10)
        left_cheek = Landmark(0, 25)
        right_cheek = Landmark(40, 25)
        # eyebrows_width / face_width * 180 = 45
        expected_ratio = (10 / 40) * 180
        result = calculate_face_turn_ratio(left_eyebrow, right_eyebrow, left_cheek, right_cheek)
        self.assertAlmostEqual(result, expected_ratio, places=2)
        
    def test_nonvalid_turn_ratio(self):
        # Simulate non valid face landmarks
        left_eyebrow = Landmark(20, 40)
        right_eyebrow = Landmark(30, 10)
        left_cheek = Landmark(40, 25)
        right_cheek = Landmark(40, 25)
        # eyebrows_width / face_width * 180 = (10/0) x 180
        with self.assertRaises(ValueError) as context:
                calculate_face_turn_ratio(left_eyebrow, right_eyebrow, left_cheek, right_cheek)
        # Verify the error message
        self.assertEqual(str(context.exception), "Face width distance can not be zero.")

    def test_no_yawn_detected_below_boundary1(self):
        # Assume yawn started less than 2 seconds ago
        yawn_start_time = time.time() - 1.9
        # At threshold
        average_ratio_lips = 30
        # Default variables
        yawn_detected, yawn_alert = False, False
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_signs(
            average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should not be detected
        self.assertFalse(new_yawn_detected)
        self.assertFalse(new_yawn_alert)
        
    def test_no_yawn_detected_below_boundary2(self):
        # Assume yawn started 2 seconds ago
        yawn_start_time = time.time() - 2
        # Below threshold
        average_ratio_lips = 29.9
        # Default variables
        yawn_detected, yawn_alert = False, False
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_signs(
            average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should not be detected
        self.assertFalse(new_yawn_detected)
        self.assertFalse(new_yawn_alert)
        
    def test_yawn_detected_at_boundary(self):
        # Assume yawn started 2 seconds ago
        yawn_start_time = time.time() - 2
        # At threshold
        average_ratio_lips = 30
        # Default variables
        yawn_detected, yawn_alert = False, False
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_signs(
            average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should be detected
        self.assertTrue(new_yawn_detected)
        self.assertTrue(new_yawn_alert)
        
    def test_yawn_detected_above_boundary(self):
        # Assume yawn started 2.1 seconds ago
        yawn_start_time = time.time() - 2.1
        # Above threshold
        average_ratio_lips = 31
        # Default variables
        yawn_detected, yawn_alert = False, False
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_signs(
            average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should be detected
        self.assertTrue(new_yawn_detected)
        self.assertTrue(new_yawn_alert)

    def test_no_turn_detected_below_boundary1(self):
        # Assume turn started less than 3 seconds ago
        turn_start_time = time.time() - 2.9
        # At threshold
        averaged_yaw = 103
        # Default variables
        turn_detected, turn_alert = False, False
        turn_start_time, turn_detected, turn_alert = detect_signs(
			averaged_yaw, turn_start_time, turn_detected, turn_alert, threshold=103, duration=3)
		# Turn should not be detected
        self.assertFalse(turn_detected)
        self.assertFalse(turn_alert)
		
    def test_turn_detected_at_boundary(self):
		# Assume turn started 3 seconds ago
        turn_start_time = time.time() - 3
		# At threshold
        averaged_yaw = 103
		# Default variables
        turn_detected, turn_alert = False, False
        turn_start_time, turn_detected, turn_alert = detect_signs(
			averaged_yaw, turn_start_time, turn_detected, turn_alert, threshold=103, duration=3)
		# Turn should be detected
        self.assertTrue(turn_detected)
        self.assertTrue(turn_alert)
		
    def test_turn_detected_above_boundary(self):
		# Assume turn started 3.1 seconds ago
        turn_start_time = time.time() - 3.1
		# Above threshold
        averaged_yaw = 104
        # Default variables
        turn_detected, turn_alert = False, False
        turn_start_time, turn_detected, turn_alert = detect_signs(
			averaged_yaw, turn_start_time, turn_detected, turn_alert, threshold=103, duration=3)
		# Turn should not be detected
        self.assertFalse(turn_detected)
        self.assertFalse(turn_alert)
		
    def test_eye_closure_detection_below_boundary1(self):
        # Assume closed started 0.9 second ago
        closed_start_time = time.time() - 0.9
        # At threshold
        average_ratio_eyes = 24
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_signs(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1)
        # Sleepy should not be detected
        self.assertFalse(new_sleepy_detected)
        self.assertFalse(new_closed_alert)
    
    def test_eye_closure_detection_below_boundary2(self):
        # Assume closed started 1 second ago
        closed_start_time = time.time() - 1
        # Below threshold
        average_ratio_eyes = 23.9
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_signs(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1)
        # Sleepy should be detected
        self.assertTrue(new_sleepy_detected)
        self.assertTrue(new_closed_alert)
    
    def test_eye_closure_detection_at_boundary(self):
        # Assume closed started 1 second ago
        closed_start_time = time.time() - 1
        # At threshold
        average_ratio_eyes = 24
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_signs(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1)
        # Sleepy should be detected
        self.assertTrue(new_sleepy_detected)
        self.assertTrue(new_closed_alert)
    
    def test_eye_closure_detection_above_boundary(self):
        # Assume closed started 1.1 second ago
        closed_start_time = time.time() - 1.1
        # Above threshold
        average_ratio_eyes = 24.1
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_signs(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1)
        # Sleepy should not be detected
        self.assertFalse(new_sleepy_detected)
        self.assertFalse(new_closed_alert)

    def test_eye_closure_detected_and_alert(self):
        # Assume closed started 1.2 second ago
        closed_start_time = time.time() - 1.2
        # Below threshold
        average_ratio_eyes = 23
        # Default variables
        sleepy_detected, closed_alert = False, False
        closed_start_time, sleepy_detected, closed_alert = detect_signs(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1)
        # Sleepy should be detected
        self.assertIsNotNone(closed_start_time)
        self.assertTrue(sleepy_detected)
        self.assertTrue(closed_alert)
        # Paths to the audio alert
        eyes_audio1 = "focus_on_the_road.mp3"
        eyes_audio2 = "Closed_eyes_detected_Stay_focused.mp3"
        eye_alert_count = 0
        eye_alert_time = None
        # Call the alert function and check variables
        closed_start_time, sleepy_detected, closed_alert, eye_alert_count, eye_alert_time = alert_func(
            closed_start_time, sleepy_detected, closed_alert, eyes_audio1, eyes_audio2, eye_alert_count, eye_alert_time)
        # Variables must be reseted at this point
        self.assertIsNotNone(eye_alert_time)
        self.assertEqual(eye_alert_count, 1)
        self.assertIsNone(closed_start_time)
        self.assertFalse(sleepy_detected)
        self.assertFalse(closed_alert)
        # Call the alert function and check variables for second time
        closed_start_time = time.time() - 1.6
        sleepy_detected, closed_alert = True, True
        closed_start_time, sleepy_detected, closed_alert, eye_alert_count, eye_alert_time = alert_func(
			closed_start_time, sleepy_detected, closed_alert, eyes_audio1, eyes_audio2, eye_alert_count, eye_alert_time)
        self.assertEqual(eye_alert_count, 2)
        # Call the alert function and check variables for third time
        closed_start_time = time.time() - 2.3
        sleepy_detected, closed_alert = True, True
        closed_start_time, sleepy_detected, closed_alert, eye_alert_count, eye_alert_time = alert_func(
			closed_start_time, sleepy_detected, closed_alert, eyes_audio1, eyes_audio2, eye_alert_count, eye_alert_time)
        self.assertEqual(eye_alert_count, 3)

    def test_eye_closure_notdetected_and_alert(self):
        # Assume closed started 0.7 second ago
        closed_start_time = time.time() - 0.7
        # Below threshold
        average_ratio_eyes = 22
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_signs(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=24, duration=1)
        # Sleepy should not be detected
        self.assertIsNotNone(new_closed_start_time)
        self.assertFalse(new_sleepy_detected)
        self.assertFalse(new_closed_alert)
        # Paths to the audio alert
        eyes_audio1 = "focus_on_the_road.mp3"
        eyes_audio2 = "Closed_eyes_detected_Stay_focused.mp3"
        eye_alert_count = 0
        eye_alert_time = None
        # call the alert function
        new_closed_start_time, new_sleepy_detected, new_closed_alert, eye_alert_count, eye_alert_time = alert_func(
            new_closed_start_time, new_sleepy_detected, new_closed_alert, eyes_audio1, eyes_audio2, eye_alert_count, eye_alert_time)
        # Variables must stay same
        self.assertEqual(eye_alert_count, 0)
        self.assertIsNotNone(new_closed_start_time)
        self.assertFalse(new_sleepy_detected)
        self.assertFalse(new_closed_alert)
        
    def test_yawn_detected_and_alert(self):
        # Assume yawn started 3.5 seconds ago
        yawn_start_time = time.time() - 3.5
        # Above threshold
        average_ratio_lips = 38
        # Default variables
        yawn_detected, yawn_alert = False, False
        yawn_start_time, yawn_detected, yawn_alert = detect_signs(
			average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should be detected
        self.assertIsNotNone(yawn_start_time)
        self.assertTrue(yawn_detected)
        self.assertTrue(yawn_alert)
        # Paths to the audio alert
        yawn_audio1 = "consider_taking_a_break.mp3"
        yawn_audio2 = "Yawning_detected_Take_a_rest_soon.mp3"
        yawn_alert_count = 0
        yawn_alert_time = None
        # Call the alert function and check variables
        yawn_start_time, yawn_detected, yawn_alert, yawn_alert_count, yawn_alert_time = alert_func(
			yawn_start_time, yawn_detected, yawn_alert, yawn_audio1, yawn_audio2, yawn_alert_count, yawn_alert_time)
        # Check updated variables
        self.assertIsNotNone(yawn_alert_time)
        self.assertEqual(yawn_alert_count, 1)
        self.assertIsNone(yawn_start_time)
        self.assertFalse(yawn_detected)
        self.assertFalse(yawn_alert)
        # Call the alert function and check variables for second time
        yawn_start_time = time.time() - 3.3
        yawn_detected, yawn_alert = True, True
        yawn_start_time, yawn_detected, yawn_alert, yawn_alert_count, yawn_alert_time = alert_func(
			yawn_start_time, yawn_detected, yawn_alert, yawn_audio1, yawn_audio2, yawn_alert_count, yawn_alert_time)
        self.assertEqual(yawn_alert_count, 2)
        # Call the alert function and check variables for third time
        yawn_start_time = time.time() - 4
        yawn_detected, yawn_alert = True, True
        yawn_start_time, yawn_detected, yawn_alert, yawn_alert_count, yawn_alert_time = alert_func(
			yawn_start_time, yawn_detected, yawn_alert, yawn_audio1, yawn_audio2, yawn_alert_count, yawn_alert_time)
        self.assertEqual(yawn_alert_count, 3)

    def test_turn_detected_and_alert(self):
        # Assume turn started 3.6 seconds ago
        turn_start_time = time.time() - 3.6
        # At threshold
        averaged_yaw = 103
        # Default variables
        turn_detected, turn_alert = False, False
        turn_start_time, turn_detected, turn_alert = detect_signs(
			averaged_yaw, turn_start_time, turn_detected, turn_alert, threshold=103, duration=3)
        # Turn should be detected
        self.assertIsNotNone(turn_start_time)
        self.assertTrue(turn_detected)
        self.assertTrue(turn_alert)
        # Paths to the audio alert
        turn_audio1 = "Eyes_on_the_road.mp3"
        turn_audio2 = "You_looking_away_Please_focus_on_driving.mp3"
        turn_alert_count = 0
        turn_alert_time = None
        # Call the alert function and check variables
        turn_start_time, turn_detected, turn_alert, turn_alert_count, turn_alert_time = alert_func(
			turn_start_time, turn_detected, turn_alert, turn_audio1, turn_audio2, turn_alert_count, turn_alert_time)
        # Check updated variables
        self.assertIsNotNone(turn_alert_time)
        self.assertEqual(turn_alert_count, 1)
        self.assertIsNone(turn_start_time)
        self.assertFalse(turn_detected)
        self.assertFalse(turn_alert)
        # Call the alert function and check variables for second time
        turn_start_time = time.time() - 3.3
        turn_detected, turn_alert = True, True
        turn_start_time, turn_detected, turn_alert, turn_alert_count, turn_alert_time = alert_func(
			turn_start_time, turn_detected, turn_alert, turn_audio1, turn_audio2, turn_alert_count, turn_alert_time)
        self.assertEqual(turn_alert_count, 2)
        # Call the alert function and check variables for third time
        turn_start_time = time.time() - 4
        turn_detected, turn_alert = True, True
        turn_start_time, turn_detected, turn_alert, turn_alert_count, turn_alert_time = alert_func(
			turn_start_time, turn_detected, turn_alert, turn_audio1, turn_audio2, turn_alert_count, turn_alert_time)
        self.assertEqual(turn_alert_count, 3)
        
    def test_yawn_notdetected_and_alert(self):
        # Assume yawn started 1.8 seconds ago
        yawn_start_time = time.time() - 1.8
        # Above threshold
        average_ratio_lips = 38
        # Default variables
        yawn_detected, yawn_alert = False, False
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_signs(
            average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should not be detected
        self.assertIsNotNone(new_yawn_start_time)
        self.assertFalse(new_yawn_detected)
        self.assertFalse(new_yawn_alert)
        # Paths to the audio alert
        yawn_audio1 = "consider_taking_a_break.mp3"
        yawn_audio2 = "Yawning_detected_Take_a_rest_soon.mp3"
        yawn_alert_count = 0
        yawn_alert_time = None
        # call the alert function
        new_yawn_start_time, new_yawn_detected, new_yawn_alert, yawn_alert_count, yawn_alert_time = alert_func(
            new_yawn_start_time, new_yawn_detected, new_yawn_alert, yawn_audio1, yawn_audio2, yawn_alert_count, yawn_alert_time)
        # Variables must stay same
        self.assertEqual(yawn_alert_count, 0)
        self.assertIsNotNone(new_yawn_start_time)
        self.assertFalse(new_yawn_detected)
        self.assertFalse(new_yawn_alert)
        
if __name__ == "__main__":
    unittest.main()