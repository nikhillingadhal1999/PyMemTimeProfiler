import os
file_path = os.getenv('PROFILER_FILE_PATH','None')
dir_path = os.getenv('PROFILER_DIR_PATH','None')
# have a seperate folder and all project in that. Don't include the env in that folder.