import threading
import time
from concurrent.futures import ThreadPoolExecutor


def download_file(file_id):
    thread_name = threading.current_thread().name
    print(f"{thread_name} 开始下载文件 {file_id}")
    time.sleep(1)
    print(f"{thread_name} 完成文件 {file_id}")
    return file_id


if __name__ == "__main__":
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(download_file, range(1, 9)))

    end = time.perf_counter()

    print("--------------------")
    print(f"完成任务数量：{len(results)}")
    print(f"完成文件编号：{results}")
    print(f"总耗时：{end - start:.2f} 秒")
