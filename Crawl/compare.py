import os
import subprocess

def compare(option: int) -> bool:
    print(option)
    dir = sorted(os.listdir("source"))[-1]
    print(dir)
    if not os.path.exists(f"result/{dir}"):
        os.makedirs(f"result/{dir}")
    if not os.path.exists(f"result/{dir}/COMPARE_ROUND{option}"):
        os.makedirs(f"result/{dir}/COMPARE_ROUND{option}")
    os.environ["source_path"] = f"source\\{dir}"
    os.environ["result_path"] = f"result\\{dir}"
    print(os.environ["source_path"])
    subprocess.run(["dbt","run","-s",f"compare.COMPARE_ROUND{option}*"], shell=True, capture_output=True, text=True)
