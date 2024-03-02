import subprocess
import os
import pandas as pd


def cut_video(input_file, output_folder, clip_duration, output_csv):
    # Get video duration
    command = ['ffmpeg', '-i', input_file, '-f', 'null', '-']
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode('utf-8')

    # Check if output contains duration information
    if 'Duration: ' not in output:
        print("Error: Failed to get video duration.")
        return

    duration_index = output.find('Duration: ') + len('Duration: ')
    duration = output[duration_index:duration_index+11]
    duration = duration.split(':')
    duration = int(duration[0])*3600 + int(duration[1]) * \
        60 + int(duration[2].split('.')[0])

    # Calculate number of clips
    num_clips = duration // clip_duration

    # Create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # Create DataFrame to store clip start times
    clip_start_times = []

    # Cut each clip
    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = start_time + clip_duration

        # Generate command line for FFMPEG
        command_line = ['-hide_banner', '-i', input_file, '-map', '0', '-c', 'copy', '-ss',
                        "{:02d}:{:02d}:{:02d}".format(
                            start_time // 3600, (start_time // 60) % 60, start_time % 60),
                        '-to',
                        "{:02d}:{:02d}:{:02d}".format(end_time // 3600, (end_time // 60) % 60, end_time % 60)]

        # Set output file path
        output_file = os.path.join(output_folder, f"video_test_{i+1}.avi")
        command_line += [output_file]

        # Run FFMPEG to cut the video
        subprocess.run(['ffmpeg'] + command_line)

        # Store clip start time
        clip_start_times.append("{:02d}:{:02d}:{:02d}".format(
            start_time // 3600, (start_time // 60) % 60, start_time % 60))

    # Create DataFrame with clip start times
    df = pd.DataFrame({'clip_start_times': clip_start_times})
    # Save DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
