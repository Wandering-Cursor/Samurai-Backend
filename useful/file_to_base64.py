import base64


def file_to_base64(file_path):
	try:
		with open(file_path, "rb") as file:
			# Read the file content
			file_content = file.read()

			# Encode the file content to Base64
			base64_string = base64.b64encode(file_content).decode("utf-8")

			# Output the Base64 string
			print(f"Base64-encoded content:\n{base64_string}")
			print(base64_string, file=open("out.txt", "w"))

	except FileNotFoundError:
		print(f"Error: File '{file_path}' not found.")
	except Exception as e:
		print(f"Error: {e}")


# Replace 'your_file.txt' with the path to your file
file_to_base64("image.jpg")
