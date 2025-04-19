# Zero-Hassle Python Profiler for Time & Memory

A lightweight, zero-configuration profiler that captures function-level performance metrics with **no code changes**. Ideal for:

- Python scripts  
- Flask projects  
- Real-time debugging of performance bottlenecks  

---

## Features

### Zero Code Changes
Just run your Python script — no decorators, annotations, or modifications needed.

### Time & Memory Metrics
Automatically captures:
- Max execution time (CPU)
- Peak memory usage
- RSS memory growth
- Return object size
- Arguments passed

### Project-Aware Analysis
Only **your** code is profiled.  
System libraries and external modules are ignored using intelligent project-path detection.

## Profiler Metrics

The following table describes the metrics collected by the profiler:

| **Metric**               | **Description**                                                                                   | **Key**                           |
|--------------------------|---------------------------------------------------------------------------------------------------|-----------------------------------|
| **Function Name**         | The name of the function being profiled.                                                          | `function`                        |
| **File Path**             | The absolute path to the file where the function is defined.                                      | `file`                            |
| **Line Number**           | The line number where the function starts in the file.                                            | `line`                            |
| **Execution Time**        | Maximum time taken by each function in milliseconds (ms).                                         | `max_time_ms`                     |
| **CPU Time**              | Time spent by the CPU on this function (ms).                                                      | `cpu_time_ms`                     |
| **Peak Memory Usage**     | Maximum memory usage during function execution in kilobytes (KB).                                 | `max_mem`                         |
| **RSS Memory Growth**     | Growth in Resident Set Size (RSS) memory in kilobytes (KB), helps spot memory leaks.              | `mem_growth_rss_kb`               |
| **Arguments**             | The arguments passed to the function being profiled.                                              | `args`                            |
| **Possible Memory Leak**  | Indicates if a potential memory leak is detected (if any).                                        | `possible_memory_leak`            |
| **Notes**                 | Any additional notes related to the profiling data.                                               | `note`                            |
| **Returned Object Size**  | The size of the returned object in bytes.                                                         | `return_obj`                      |



### Structured JSON Reports
Each function includes:
- Function name
- Source file and line number
- Time (ms)
- Memory usage (KB)
- Return object size
- Arguments
- Memory growth & potential leaks

### Works with Any Project Structure
Handles **nested folder hierarchies** easily — just point to your project root and go.

---

## Setup Instructions

### 1. Set Environment Variables

```bash
export PROFILER_FILE_PATH="/absolute/path/to/your_script.py"
export PROFILER_DIR_PATH="/absolute/path/to/your/project/root"
```
If you just want to try, you can test it with sample_project. 
> `PROFILER_FILE_PATH="$(pwd)/sample_project/inside/app.py"`: The Python file to be profiled  
> `PROFILER_DIR_PATH="$(pwd)/sample_project/inside"`: Root of your project for accurate filtering

### 2. Optional: Suppress Console Output

By default, profiler prints a table to the console. To disable:

```bash
export CONSOLE_DISPLAY=False
```
## Environment Setup

If you **already have a virtual environment**, just install the dependencies:

```bash
make setup
```

This will install the requirements in your env

If you **don't have a virtual environment**, just install the dependencies:

```bash
make setup
```

This will create an env and install requirements

## Run profiler

```bash
make run
```


This will:
- Read the env vars
- Launch your script
- Record memory + execution stats
- Save detailed JSON report

---

## Supported Use Cases

- Pure Python projects
- Flask APIs and apps
- Any directory layout

---

## Want More?

- [ ] Console table toggle
- [ ] HTML report output
- [ ] Jupyter Notebook integration

Pull requests are welcome!
