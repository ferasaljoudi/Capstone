import time
import unittest

import numpy as np
from eye_detection_tflite import prepare_eye_for_model, get_box
from eye_detection_tflite import calculate_mouth_ratio
from eye_detection_tflite import detect_yawn, detect_eye_closure
from eye_detection_tflite import yawn_alert_func, closed_alert_func


class TestDrowsinessDetection(unittest.TestCase):
	def test_prepare_eye_for_model(self):
		# Create a dummy eye image (64x64 image with random values)
		dummy_eye_img = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
		# Call the function
		processed_eye = prepare_eye_for_model(dummy_eye_img)
		# Check the output shape
		self.assertEqual(processed_eye.shape, (1, 48, 48, 3))

	def test_get_box(self):
		# Create dummy landmarks with normalized values
		landmarks = {
			0: type('', (), {"x": 0.5, "y": 0.5})(),
			1: type('', (), {"x": 0.6, "y": 0.6})(),
			2: type('', (), {"x": 0.4, "y": 0.4})(),
			3: type('', (), {"x": 0.45, "y": 0.55})()
		}
		# IDs to landmarks
		ids = [0, 1, 2, 3]
		# Set frame dimensions
		frame_width = 100
		frame_height = 200
		# Call the function
		x_min, y_min, x_max, y_max = get_box(landmarks, ids, frame_width, frame_height)
		# Check the output
		self.assertEqual(x_min, 30)
		self.assertEqual(y_min, 60)
		self.assertEqual(x_max, 70)
		self.assertEqual(y_max, 130)

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

	def test_eye_closure_detection_below_boundary(self):
		# Assume closed started 0.9 second ago
		closed_start_time = time.time() - 0.9
		eye_status = "Closed"
		# Default variables
		sleepy_detected, closed_alert = False, False
		new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
			eye_status, closed_start_time, sleepy_detected, closed_alert, duration=1
		)
		# Sleepy should not be detected
		self.assertFalse(new_sleepy_detected)
		self.assertFalse(new_closed_alert)

	def test_eye_closure_detection_at_boundary(self):
		# Assume closed started 1 second ago
		closed_start_time = time.time() - 1
		eye_status = "Closed"
		# Default variables
		sleepy_detected, closed_alert = False, False
		new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
			eye_status, closed_start_time, sleepy_detected, closed_alert, duration=1
		)
		# Sleepy should be detected
		self.assertTrue(new_sleepy_detected)
		self.assertTrue(new_closed_alert)

	def test_eye_closure_detection_above_boundary1(self):
		# Assume closed started 1.1 second ago
		closed_start_time = time.time() - 1.1
		eye_status = "Closed"
		# Default variables
		sleepy_detected, closed_alert = False, False
		new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
			eye_status, closed_start_time, sleepy_detected, closed_alert, duration=1
		)
		# Sleepy should be detected
		self.assertTrue(new_sleepy_detected)
		self.assertTrue(new_closed_alert)
	
	def test_eye_closure_detection_above_boundary2(self):
		# Assume closed started 1.5 second ago
		closed_start_time = time.time() - 1.5
		eye_status = "Open"
		# Default variables
		sleepy_detected, closed_alert = False, False
		new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
			eye_status, closed_start_time, sleepy_detected, closed_alert, duration=1
		)
		# Sleepy should not be detected
		self.assertFalse(new_sleepy_detected)
		self.assertFalse(new_closed_alert)
		
	def test_eye_closure_detected_and_alert(self):
		# Assume closed started 1.2 second ago
		closed_start_time = time.time() - 1.3
		eye_status = "Closed"
		# Default variables
		sleepy_detected, closed_alert = False, False
		new_closed_start_time, new_sleepy_detected, new_closed_alert = detect_eye_closure(
			eye_status, closed_start_time, sleepy_detected, closed_alert, duration=1
		)
		# Sleepy should be detected
		self.assertIsNotNone(new_closed_start_time)
		self.assertTrue(new_sleepy_detected)
		self.assertTrue(new_closed_alert)

		# Path to the audio alert
		file1 = "focus_on_the_road.mp3"
		# call the alert function
		new_closed_start_time, new_sleepy_detected, new_closed_alert = closed_alert_func(
			new_closed_start_time, new_sleepy_detected, new_closed_alert, file1)
		# Variables must be reseted at this point
		self.assertIsNone(new_closed_start_time)
		self.assertFalse(new_sleepy_detected)
		self.assertFalse(new_closed_alert)
		
	def test_yawn_detected_and_alert(self):
		# Assume yawn started 3.5 seconds ago
		yawn_start_time = time.time() - 3.5
		# Above threshold
		average_ratio_lips = 38
		# Default variables
		yawn_detected, yawn_alert = False, False
		new_yawn_start_time, new_yawn_detected, new_yawn_alert = detect_yawn(
			average_ratio_lips, yawn_start_time, yawn_detected, yawn_alert, threshold=30, duration=2)
		# Yawn should be detected
		self.assertIsNotNone(new_yawn_start_time)
		self.assertTrue(new_yawn_detected)
		self.assertTrue(new_yawn_alert)

		# Path to the audio alert
		file2 = "consider_taking_a_rest.mp3"
		# call the alert function
		new_yawn_start_time, new_yawn_detected, new_yawn_alert = yawn_alert_func(
			new_yawn_start_time, new_yawn_detected, new_yawn_alert, file2)
		# Variables must be reseted at this point
		self.assertIsNone(new_yawn_start_time)
		self.assertFalse(new_yawn_detected)
		self.assertFalse(new_yawn_alert)
        
	def test_get_box_and_process_image(self):
		# Simulate dummy landmarks with normalized values
		landmarks = {
			0: type('', (), {"x": 0.5, "y": 0.5})(),
			1: type('', (), {"x": 0.6, "y": 0.6})(),
			2: type('', (), {"x": 0.4, "y": 0.4})(),
			3: type('', (), {"x": 0.45, "y": 0.55})()
		}
		# IDs to landmarks
		ids = [0, 1, 2, 3]
		# Set frame dimensions
		frame_width = 100
		frame_height = 200
		# Create a dummy eye image (64x64 image with random values)
		dummy_eye_img = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
		# Call the get_box to extract the bounding box
		x_min, y_min, x_max, y_max = get_box(landmarks, ids, frame_width, frame_height)
		# Check the output
		self.assertEqual(x_min, 30)
		self.assertEqual(y_min, 60)
		self.assertEqual(x_max, 70)
		self.assertEqual(y_max, 130)
		# Crop the image
		cropped_image = dummy_eye_img[y_min:y_max, x_min:x_max]
		# Call the process image function
		processed_eye = prepare_eye_for_model(cropped_image)
		# Check the output shape
		self.assertEqual(processed_eye.shape, (1, 48, 48, 3))
		
if __name__ == "__main__":
    unittest.main()
