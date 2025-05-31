import os
import json
import shutil # For copying dummy files

# --- Configuration ---
VIDEOS_ROOT_DIR = 'videos/' # The main directory where all show folders are
TARGET_SHOW_FOLDER = 'show_A' # The specific folder where renaming will occur
RENAME_PREFIX = '_monster.mkv' # Suffix for the renamed files (e.g., 'eleven_monster.mkv')

# Naming convention for the new files
START_NUMBER = 11
END_NUMBER = 20 # Aapne bola 20 tak chahiye, toh ye 20 kar diya

# Mapping for numbers to words for renaming (e.g., 11 -> "eleven")
NUMBER_TO_WORD = {
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
    11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
    16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
    20: 'twenty',
    21: 'twenty-one', 22: 'twenty-two', 23: 'twenty-three', 24: 'twenty-four', 25: 'twenty-five'
}
# Upar NUMBER_TO_WORD ko 25 tak extend kar diya hai, taaki agar END_NUMBER badhao toh kaam aaye.

JSON_FILE_PATH = 'episode_data.json'
DEFAULT_POSTER_PATH = 'posters/default_poster.jpg' # Make sure this path is correct if you have one
DEFAULT_DESCRIPTION = "A thrilling episode of the series."

# --- Helper Functions ---

def create_dummy_video_file(path, size_kb=10):
    """Creates a small dummy file at the given path."""
    if not os.path.exists(path):
        with open(path, 'wb') as f:
            f.write(os.urandom(1024 * size_kb)) # Create a file with random bytes

def generate_episode_title_smart(filename, episode_num=None):
    """Generates a more readable title from a filename."""
    name_parts = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').split()
    
    # Try to find a pattern like "eleven_monster" or "SXXEXX"
    for word_num, word_val in NUMBER_TO_WORD.items():
        if word_val in name_parts and "_monster" in filename: # Specific to your naming
            return f"Episode {word_num} (Monster)"

    if episode_num:
        return f"Episode {episode_num}"
        
    # Fallback for general filenames
    title = ' '.join([part.capitalize() for part in name_parts if not part.isdigit() and len(part) > 1])
    if not title:
        title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    
    return title.replace('Mkv', '').strip() # Clean up extensions if they somehow remain

# --- Main Script Logic ---

def automate_video_tasks():
    print("Starting video automation tasks...")

    # Create root video directory if it doesn't exist
    os.makedirs(VIDEOS_ROOT_DIR, exist_ok=True)
    target_show_path = os.path.join(VIDEOS_ROOT_DIR, TARGET_SHOW_FOLDER)
    os.makedirs(target_show_path, exist_ok=True)

    # --- Renaming specific show files (NEW & IMPROVED LOGIC) ---
    print(f"Checking video files in '{target_show_path}' for intelligent renaming.")

    # Get all video files in the target show folder
    all_current_videos = [f for f in os.listdir(target_show_path) if f.lower().endswith(('.mkv', '.mp4', '.avi', '.mov', '.webm'))]

    # Identify files that are ALREADY named correctly according to the NUMBER_TO_WORD pattern
    already_correctly_named_files = set()
    for num_key, word_val in NUMBER_TO_WORD.items():
        if START_NUMBER <= num_key <= END_NUMBER:
            expected_name = f"{word_val}{RENAME_PREFIX}"
            if expected_name in all_current_videos:
                already_correctly_named_files.add(expected_name)

    # Separate files to be renamed from those that are already correct
    files_to_rename_candidates = sorted([
        f for f in all_current_videos if f not in already_correctly_named_files
    ])

    print(f"Total video files in '{target_show_path}': {len(all_current_videos)}")
    print(f"Files already correctly named (and will be skipped): {len(already_correctly_named_files)}")
    print(f"Files available for renaming (candidates): {len(files_to_rename_candidates)}")

    rename_candidate_index = 0 # This index will keep track of which candidate file we are renaming

    for current_num in range(START_NUMBER, END_NUMBER + 1):
        if current_num not in NUMBER_TO_WORD:
            print(f"Warning: No word mapping for number {current_num}. Skipping this number for renaming.")
            continue 

        desired_word_name = NUMBER_TO_WORD[current_num]
        desired_new_filename = f"{desired_word_name}{RENAME_PREFIX}"
        desired_new_filepath = os.path.join(target_show_path, desired_new_filename)

        if os.path.exists(desired_new_filepath):
            # Agar file already sahi naam se hai, toh kuch mat karo, aage badho
            print(f"'{desired_new_filename}' already exists and is correctly named. Skipping.")
            continue 
        
        # Agar yahan tak pahunche hain, toh is 'current_num' ke liye sahi file abhi nahi hai.
        # Toh, files_to_rename_candidates se ek file leke rename karte hain.
        if rename_candidate_index < len(files_to_rename_candidates):
            old_filename_to_rename = files_to_rename_candidates[rename_candidate_index]
            old_filepath_to_rename = os.path.join(target_show_path, old_filename_to_rename)

            try:
                os.rename(old_filepath_to_rename, desired_new_filepath)
                print(f"Renamed: '{old_filename_to_rename}' to '{desired_new_filename}'")
                rename_candidate_index += 1 # Agli candidate file par jao
            except OSError as e:
                print(f"Error renaming '{old_filename_to_rename}' to '{desired_new_filename}': {e}")
        else:
            # Agar koi aur unnamed video file bachi hi nahi rename karne ke liye
            print(f"No more unnamed video files available to rename to '{desired_new_filename}'.")
            # Iska matlab hai ki aapke paas utni source files nahi hain jitne episodes aap chahte ho.

    print("Renaming process complete for show_A.")


    # --- Generate episode_data.json ---
    episodes_data = []
    episode_counter = 1 # Use a separate counter for overall episode IDs

    # Walk through the entire VIDEOS_ROOT_DIR to find all video files
    for root, _, files in os.walk(VIDEOS_ROOT_DIR):
        for file in files:
            if file.lower().endswith(('.mkv', '.mp4', '.avi', '.mov', '.webm')):
                file_path = os.path.join(root, file)
                # Make file path relative for web serving
                relative_path = os.path.relpath(file_path, start=os.getcwd()).replace('\\', '/')

                # Extract a cleaner ID and title
                episode_id = f"ep-{episode_counter}" # Default ID
                title = generate_episode_title_smart(file, episode_counter) # Default title

                # If the file matches the specific TARGET_SHOW_FOLDER pattern, use its unique ID
                # and more specific title. This handles the 'monster' series.
                if TARGET_SHOW_FOLDER in root and RENAME_PREFIX in file:
                    try:
                        # Extract the number from the word_monster format
                        word_part = file.split(RENAME_PREFIX)[0]
                        # Corrected line where the typo was:
                        num_key = next((k for k, v in NUMBER_TO_WORD.items() if v == word_part), None) 
                        if num_key:
                            episode_id = f"ep-{num_key}" 
                            title = f"Episode {num_key} (Monster)"
                        # Else, if it's a monster file but word not found, use smart title
                    except Exception:
                        pass # Ignore error and use default title

                episodes_data.append({
                    "id": episode_id,
                    "title": title,
                    "filePath": relative_path,
                    "posterPath": DEFAULT_POSTER_PATH, 
                    "description": DEFAULT_DESCRIPTION
                })
                episode_counter += 1

    # Sort episodes by their numeric ID to ensure they appear in order
    def sort_key(item):
        try:
            return int(item['id'].split('-')[1])
        except (ValueError, IndexError):
            return float('inf') # Put items with non-numeric IDs at the end

    episodes_data.sort(key=sort_key)


    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(episodes_data, f, indent=4)
    print(f"Generated '{JSON_FILE_PATH}' with {len(episodes_data)} episodes.")
    print("Automation complete!")

if __name__ == "__main__":
    automate_video_tasks()