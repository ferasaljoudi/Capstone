import time
import unittest

from eye_detection_mediapipe import (calculate_eye_ratio,
                                     calculate_mouth_ratio, detect_eye_closure,
                                     detect_yawn)


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
        # Simulate invalid eye landmarks (missing point)
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

    def test_no_yawn_detected_below_boundary1(self):
        # Assume yawn started less than 2 seconds ago
        yawn_start_time = time.time() - 1.9
        # At threshold
        average_ratio_lips = 30
        # Default variables
        yawn_detected, yawn_alert = False, False
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_yawn(
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
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_yawn(
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
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_yawn(
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
        new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_yawn(
            average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
        # Yawn should be detected
        self.assertTrue(new_yawn_detected)
        self.assertTrue(new_yawn_alert)

    def test_eye_closure_detection_below_boundary1(self):
        # Assume yawn started 0.9 second ago
        closed_start_time = time.time() - 0.9
        # At threshold
        average_ratio_eyes = 25
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=25, duration=1
        )
        # Sleepy should not be detected
        self.assertFalse(new_sleepy_detected)
        self.assertFalse(new_closed_alert)

    def test_eye_closure_detection_below_boundary2(self):
        # Assume yawn started 1 second ago
        closed_start_time = time.time() - 1
        # Below threshold
        average_ratio_eyes = 24.9
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=25, duration=1
        )
        # Sleepy should be detected
        self.assertTrue(new_sleepy_detected)
        self.assertTrue(new_closed_alert)

    def test_eye_closure_detection_at_boundary(self):
        # Assume yawn started 1 second ago
        closed_start_time = time.time() - 1
        # At threshold
        average_ratio_eyes = 25
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=25, duration=1
        )
        # Sleepy should be detected
        self.assertTrue(new_sleepy_detected)
        self.assertTrue(new_closed_alert)

    def test_eye_closure_detection_above_boundary(self):
        # Assume yawn started 1.1 second ago
        closed_start_time = time.time() - 1.1
        # Above threshold
        average_ratio_eyes = 25.1
        # Default variables
        sleepy_detected, closed_alert = False, False
        new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
            average_ratio_eyes, closed_start_time, sleepy_detected, closed_alert, threshold=25, duration=1
        )
        # Sleepy should not be detected
        self.assertFalse(new_sleepy_detected)
        self.assertFalse(new_closed_alert)

if __name__ == "__main__":
    unittest.main()
