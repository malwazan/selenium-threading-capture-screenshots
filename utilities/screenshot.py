import os
import time


# takes screenshots
def capture_screenshot(driver, ss_path, stop_thread):
	while True:
		if stop_thread():
			print("Exiting loop")
			break

		# if not os.path.exists("screenshots"):
		# 	os.mkdir("screenshots")

		if not driver.service.is_connectable():
			break

		driver.save_screenshot(f"{ss_path}{str(time.time())}.png")
		time.sleep(1)