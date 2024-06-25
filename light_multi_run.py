import subprocess
import argparse

# Function to process each video
def process_video(video_file, log_file):
    # Remove trailing newline and any carriage return characters
    video_id = video_file.strip().rstrip('\r')[:-4]  # Remove .mp4 extension
    
    print(f"Processing {video_id}")
    
    # Construct the command to execute
    command = f"CUDA_VISIBLE_DEVICES=0 bash data_gen/runs/nerf/light_run.sh {video_id}"
    
    # Open log file in append mode
    with open(log_file, 'a') as log:
        # Execute the command and redirect stdout and stderr to the log file
        result = subprocess.run(command, shell=True, stdout=log, stderr=subprocess.STDOUT)
        
        # Check if there was an error
        if result.returncode != 0:
            log.write(f"Error processing {video_id}\n")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process videos and log output.")
    parser.add_argument('--video_list', type=str, required=True, help='Path to the file containing the list of video files.')
    parser.add_argument('--log_file', type=str, required=True, help='Path to the log file.')

    args = parser.parse_args()
    
    # Read video IDs from the file
    with open(args.video_list, 'r') as file:
        videos = file.readlines()
    
    # Process each video
    for video in videos:
        process_video(video, args.log_file)
