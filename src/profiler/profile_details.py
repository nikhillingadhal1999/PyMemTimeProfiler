import sys
import time
import tracemalloc
import json
from pathlib import Path
import os
import gc
from pympler import asizeof
import psutil
import io
from line_profiler import LineProfiler
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.helpers.helper import check_event, check_external_functions, get_all_args, is_user_code, detect_mem_leak
from src.config.config import file_path, dir_path

class Profiler:
    def __init__(self, root_path, leak_threshold_kb=3000):
        self.root_path = Path(root_path).resolve()
        self.records = {}
        self.call_stack = {}
        self.leak_threshold_kb = leak_threshold_kb
        self.proc = psutil.Process(os.getpid())
        tracemalloc.start()

        self.line_profiler = LineProfiler()
        self.line_profiled_functions = set()
        self.line_profiled_output = {}
        self.enable_line_profiling = True

    def profile_func(self, frame, event, arg):
        if check_event(event):
            return self.profile_func

        code = frame.f_code
        func_name = code.co_name

        if check_external_functions(func_name):
            return self.profile_func

        if not is_user_code(frame, self.root_path):
            return self.profile_func

        key = (func_name, code.co_filename, frame.f_lineno)

        if event == "call":
            time.sleep(0.2)
            print("Clearing mem...")
            gc.collect()

            all_args = get_all_args(frame)
            cpu_start = time.process_time()
            wall_start = time.perf_counter()
            start_snapshot = tracemalloc.take_snapshot()
            mem_start = self.proc.memory_info().rss

            self.call_stack[frame] = {
                "start_time": wall_start,
                "start_cpu": cpu_start,
                "start_snapshot": start_snapshot,
                "args": all_args,
                "mem_start": mem_start
            }

            print(f"[CALL] {func_name} at {code.co_filename}")

        elif event == "return" and frame in self.call_stack:
            code_obj = frame.f_code

            if self.enable_line_profiling and code_obj not in self.line_profiled_functions:
                func = frame.f_globals.get(code_obj.co_name)
                if callable(func):
                    self.line_profiler.add_function(func)
                    self.line_profiled_functions.add(code_obj)

            call_info = self.call_stack.pop(frame)
            end_time = time.perf_counter()
            end_cpu = time.process_time()
            mem_end = self.proc.memory_info().rss

            duration = end_time - call_info["start_time"]
            cpu_time = end_cpu - call_info["start_cpu"]

            time.sleep(0.02)
            print("Clearing mem...")
            gc.collect()
            end_snapshot = tracemalloc.take_snapshot()
            memory_diff = end_snapshot.compare_to(call_info["start_snapshot"], "lineno")
            total_mem = sum([stat.size_diff for stat in memory_diff])
            max_mem = max([stat.size_diff for stat in memory_diff], default=0)
            mem_growth = mem_end - call_info["mem_start"]

            returned_size = asizeof.asizeof(arg)
            returned_enough = abs(total_mem - returned_size) / 1000
            leak_candidates = detect_mem_leak(memory_diff, self.leak_threshold_kb, self.root_path)

            record = self.records.get(
                key,
                {
                    "function": func_name,
                    "file": code.co_filename,
                    "line": frame.f_lineno,
                    "max_time": 0,
                    "cpu_time": 0,
                    "max_mem": 0,
                    "mem_growth_rss": 0,
                    "args": call_info["args"],
                    "possible_memory_leak": None,
                    "note": []
                },
            )

            record["max_time"] = max(record["max_time"], duration)
            record["cpu_time"] = max(record["cpu_time"], cpu_time)
            record["max_mem"] = max(record["max_mem"], max_mem)
            record["max_time_ms"] = round(record["max_time"] * 1000, 3)
            record["cpu_time_ms"] = round(record["cpu_time"] * 1000, 3)
            record["max_mem_kb"] = round(record["max_mem"] / 1024, 3)
            record["mem_growth_rss_kb"] = round(mem_growth / 1024, 3)
            record["returned_size"] = returned_size

            if (self.leak_threshold_kb * 1000) < returned_size:
                record["note"].append("Obj return size is huge. Please check.")

            self.records[key] = record

        return self.profile_func

    def write_output(self, output_file="profile_output.json"):
        output = list(self.records.values())
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n Profile results written to {output_file}")
