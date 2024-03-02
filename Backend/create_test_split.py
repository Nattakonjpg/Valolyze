import os


def create_test_split(input_path, output_file_path):
    with open(output_file_path, "w") as f:
        for i, filename in enumerate(os.listdir(input_path), start=1):
            if filename.endswith(".avi"):
                new_filename = f"video_test_{i}.avi 2\n"
                f.write(new_filename)
