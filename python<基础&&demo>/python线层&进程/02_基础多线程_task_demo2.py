import threading
import time


def download_file(file_id):
    print(f"文件 {file_id} 开始下载")
    time.sleep(2)
    print(f"文件 {file_id} 下载完成")


if __name__ == "__main__":
    start = time.perf_counter()
    threads = []

    for i in range(1, 5):
        thread = threading.Thread(target=download_file, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = time.perf_counter()
    print(f"总耗时：{end - start:.2f} 秒")
