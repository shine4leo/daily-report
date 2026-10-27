import threading
import time
from queue import Queue

completed_count = 0
lock = threading.Lock()


def download_file(file_id):
    thread_name = threading.current_thread().name
    print(f"{thread_name} 开始下载文件 {file_id}")
    time.sleep(1)
    print(f"{thread_name} 完成文件 {file_id}")


def worker(task_queue):
    global completed_count

    while True:
        file_id = task_queue.get()
        try:
            if file_id is None:  # 哨兵值：通知当前工作线程退出
                break

            download_file(file_id)
            with lock:
                completed_count += 1
        finally:
            # 每次 get() 都要对应一次 task_done()
            task_queue.task_done()


if __name__ == "__main__":
    start = time.perf_counter()
    task_queue = Queue()

    for i in range(1, 9):
        task_queue.put(i)

    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=worker,
            args=(task_queue,),
            name=f"Worker-{i + 1}",
        )
        threads.append(thread)
        thread.start()

    # 每个工作线程各投递一个退出信号
    for _ in threads:
        task_queue.put(None)

    task_queue.join()

    for thread in threads:
        thread.join()

    end = time.perf_counter()

    print("--------------------")
    print(f"实际完成任务数：{completed_count}")
    print(f"总耗时：{end - start:.2f} 秒")
