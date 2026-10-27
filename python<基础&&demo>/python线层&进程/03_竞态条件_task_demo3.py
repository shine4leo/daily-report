import threading
import time

# 全局变量：记录下载完成的文件数
completed_count = 0


def download_file(file_id):
    global completed_count

    print(f"文件 {file_id} 开始下载")
    time.sleep(1)
    print(f"文件 {file_id} 下载完成")

    # 读取当前完成数量
    old_count = completed_count

    # 模拟读取后发生线程切换
    time.sleep(0.1)

    # 更新完成数量：多个线程可能写入相同的结果
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
