import unittest

from eye_detection_mediapipe import calculate_eye_ratio, calculate_mouth_ratio


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

if __name__ == "__main__":
    unittest.main()
