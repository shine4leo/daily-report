import threading
import time

completed_count = 0
lock = threading.Lock()


def download_file(file_id):
    global completed_count

    print(f"文件 {file_id} 开始下载")
    time.sleep(1)
    print(f"文件 {file_id} 下载完成")

    # 临界区：同一时间只允许一个线程更新计数器
    with lock:
        old_count = completed_count
        time.sleep(0.1)
        completed_count = old_count + 1


if __name__ == "__main__":
    threads = []

    for i in range(1, 5):
        thread = threading.Thread(target=download_file, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("--------------------")
    print(f"实际完成任务数：{completed_count}")
    print("预期完成任务数：4")
