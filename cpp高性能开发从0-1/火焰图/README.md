# perf 性能分析

> Linux 平台专属，以下内容基于 CentOS 环境。

Linux 性能分析与调试工具实践笔记：使用 **perf** 生成火焰图定位 CPU 热点、使用 **gdb** 调试 coredump 文件，以及使用 **ASan / Valgrind** 检测 C/C++ 内存问题。

## 目录

- [1. perf](#1-perf)
  - [安装 perf](#安装-perf)
  - [查看 perf 版本](#查看-perf-版本)
  - [测试代码](#测试代码)
  - [使用 perf 对系统 CPU 事件做采样](#使用-perf-对系统-cpu-事件做采样)
  - [生成火焰图](#生成火焰图)
  - [将火焰图从 docker 中导出到本地](#将火焰图从-docker-中导出到本地)
  - [从火焰图可以获得的信息](#从火焰图可以获得的信息)
  - [生成火焰图常见问题](#生成火焰图常见问题)
- [2. 使用 gdb 调试 coredump 文件](#2-使用-gdb-调试-coredump-文件)
- [3. 趣味命令](#3-趣味命令)
- [4. 疑问](#4-疑问)
- [5. ASan（AddressSanitizer）](#5-asanaddresssanitizer)
- [6. Valgrind](#6-valgrind)
- [7. ASan 与 Valgrind 的区别](#7-asan-与-valgrind-的区别)
- [8. 参考文档](#8-参考文档)

---

## 1. perf

💡 快速找出性能瓶颈和优化点。

### 安装 perf

```bash
# Ubuntu 系统
sudo apt-get install -y linux-tools-common linux-tools-generic linux-tools-`uname -r`

# Centos 系统
yum install -y perf
```

### 查看 perf 版本

```bash
$ perf --version
perf version 5.4.44

$ man perf

# 测试
perf stat ls

# 查看支持的 events
perf list

# 查看上下文切换
perf stat -e cs ls

# trace = strace
perf trace ls
```

### 测试代码

```cpp
#include <stdio.h>
#include <stdlib.h>

void long_test() {
    int i, j;
    for (i = 0; i < 1000000; i++) j = i;
}

void foo2() {
    int i;
    for (i = 0; i < 10; i++) long_test();
}

void foo1() {
    int i;
    for (i = 0; i < 100; i++) long_test();
}

int main(void) {
    foo1();
    foo2();
}
```

编译成二进制文件：

```bash
g++ -o test test.cpp
```

### 使用 perf 对系统 CPU 事件做采样

> 采样 60s，会生成一个 perf.data 文件。

```bash
# 方式一：对一个正在运行的进程进行采样（PID 换成要检测的进程 ID）
perf record -p PID -g -- sleep 60

# 方式二：全新运行一个二进制文件 main 进行采样（./main 这个可执行文件必须存在）
sudo perf record -F 99 -g ./main -- sleep 60
```

### 生成火焰图

> 利用这个开源工具可以将报告生成可视化的 svg 图片，更容易查看对应的 CPU 开销时间和调用栈深度。

```bash
git clone --depth 1 https://github.com/brendangregg/FlameGraph.git

# 安装 perl
yum install -y perl
# Ubuntu
apt install -y perl
```

生成火焰图的脚本（对二进制文件 `main` 进行 10 秒采样，然后生成火焰图；非 root 用户需要加 sudo）：

```bash
perf record -g ./main sleep 10
perf script -i perf.data &> perf.unfold
./FlameGraph/stackcollapse-perf.pl perf.unfold &> perf.folded
./FlameGraph/flamegraph.pl perf.folded > perf.svg
```

### 将火焰图从 docker 中导出到本地

```bash
# 3cf72755eea5 为容器 ID
docker cp 3cf72755eea5:/home/tmp/perf.svg /Users/yaojun/Desktop
```

### 从火焰图可以获得的信息

- 调用栈从下往上，下层为父类，上层为子类。
- 点击父类缩小，点击子类放大。
- 只关注自己实现的函数名，忽略标准库中的函数。
- 火焰图的宽度用于比较不同函数或代码路径的性能，高度用于显示函数调用堆栈的深度。

### 生成火焰图常见问题

- 没有加 root 权限。

---

## 2. 使用 gdb 调试 coredump 文件

### 设置允许 Linux 系统生成 coredump

```bash
vim /etc/profile
ulimit -c unlimited
source /etc/profile
```

查看是否支持生成 coredump：

```bash
$ ulimit -a | grep core
core file size          (blocks, -c) unlimited
```

### 设置 coredump 文件路径

```bash
# vim /etc/sysctl.conf
kernel.core_pattern=/var/core/core_%E.%p.%t.%s
```

> - `%E`：程序文件的完整路径（路径中的 `/` 会被 `!` 替代）
> - `%p`：进程 ID
> - `%t`：进程崩溃的时间戳
> - `%s`：哪个信号让进程崩溃

```bash
sysctl -p /etc/sysctl.conf

# 创建生成的目录，并且给目录加权限
mkdir -p /var/core
chmod 777 /var/core
```

### 创建生成 coredump 的 C++ 文件

```cpp
#include <thread>
#include <chrono>

int main()
{
    std::this_thread::sleep_for(std::chrono::hours(1));  // 休眠一个小时
    return 0;
}
```

编译并触发崩溃：

```bash
$ g++ -std=c++11 -g -o main main.cpp
$ ./main &
[1] 4190567
$ kill -s SIGSEGV 4190567
```

### 查看 coredump 文件产生的原因

```bash
# gdb binaryfile
gdb main /var/crash/'!home!ubuntu!main.4190567.1687675924.11'

# 查看堆栈
$ bt
```

---

## 3. 趣味命令

在 Linux 环境打印一些有趣的图形：

```bash
# 安装
$ sudo apt-get install cowsay

# 运行
$ cowsay "I am your father!"

# 小火车
$ sudo apt-get install sl

# 执行
$ sl
```

---

## 4. 疑问

- explain 和 strace 的区别？

```bash
strace ./a.out
```

---

## 5. ASan（AddressSanitizer）

无需安装任何工具，默认就有这个组件。

编译时添加参数：`-fsanitize=address`（这是核心）。

### 有内存泄露的代码

```cpp
#include <iostream>
#include <stdlib.h>

using namespace std;

void func(){
    int *x=(int *)malloc( 10 * sizeof ( int ) ) ;
    x[10]=0;
}

int main(){
    func();
    cout<<"done"<<endl;
    return 0;
}
```

### 编译生成可执行文件

```bash
g++ -fsanitize=address -o test_asan test.cpp -g
```

### 直接运行

```bash
$ ./test_asan
=================================================================
==58231==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x604000000038 at pc 0x5616ea3e0302 bp 0x7ffe31bf1430 sp 0x7ffe31bf1420
WRITE of size 4 at 0x604000000038 thread T0
    #0 0x5616ea3e0301 in func() /home/ubuntu/test.cpp:6
    #1 0x5616ea3e0317 in main /home/ubuntu/test.cpp:9
    #2 0x7f052becd082 in __libc_start_main ../csu/libc-start.c:308
    #3 0x5616ea3e01ed in _start (/home/ubuntu/test_asan+0x11ed)

0x604000000038 is located 0 bytes to the right of 40-byte region [0x604000000010,0x604000000038)
allocated by thread T0 here:
    #0 0x7f052c4f4808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x5616ea3e02be in func() /home/ubuntu/test.cpp:5
    #2 0x5616ea3e0317 in main /home/ubuntu/test.cpp:9
    #3 0x7f052becd082 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/ubuntu/test.cpp:6 in func()
...
==58231==ABORTING
```

> 主要出错位置在 `#0 ... func() /home/ubuntu/test.cpp:6` 和 `#1 ... main /home/ubuntu/test.cpp:9`。

---

## 6. Valgrind

memcheck 是 valgrind 应用最广泛的工具，也是 valgrind 的默认工具。

```bash
$ valgrind --version
valgrind-3.15.0
```

<!-- TODO: 原文档中的"程序运行时内存空间布局图"为飞书私有图片，无法在 GitHub 直接展示，请替换为可访问的图片链接。 -->

### 查看栈的大小

```bash
$ ulimit -a
core file size          (blocks, -c) unlimited
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 15355
max locked memory       (kbytes, -l) 65536
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 15355
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```

### 有内存泄露的代码

```cpp
#include <iostream>
#include <stdlib.h>

using namespace std;

void func(){
    int *x=(int *)malloc( 10 * sizeof ( int ) ) ;
    x[10]=0;
}

int main(){
    func();
    cout<<"done"<<endl;
    return 0;
}
```

### 编译生成可执行文件

```bash
g++ -g -o test test.cpp
```

### 使用 valgrind 检测

编译时**加上 `-g` 参数**，valgrind 才能在报告中显示具体的出错代码行号。

```text
$ valgrind ./test
==52268== Memcheck, a memory error detector
==52268== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==52268== Using Valgrind-3.15.0 and LibVEX; rerun with -h for copyright info
==52268== Command: ./test
==52268==
==52268== Invalid write of size 4
==52268==    at 0x1091EB: func() (test.cpp:6)
==52268==    by 0x109200: main (test.cpp:9)
==52268==  Address 0x4dabca8 is 0 bytes after a block of size 40 alloc'd
==52268==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==52268==    by 0x1091DE: func() (test.cpp:5)
==52268==    by 0x109200: main (test.cpp:9)
==52268==
done
==52268==
==52268== HEAP SUMMARY:
==52268==     in use at exit: 40 bytes in 1 blocks
==52268==   total heap usage: 3 allocs, 2 frees, 73,768 bytes allocated
==52268==
==52268== LEAK SUMMARY:
==52268==    definitely lost: 40 bytes in 1 blocks
==52268==    indirectly lost: 0 bytes in 0 blocks
==52268==      possibly lost: 0 bytes in 0 blocks
==52268==    still reachable: 0 bytes in 0 blocks
==52268==         suppressed: 0 bytes in 0 blocks
==52268== Rerun with --leak-check=full to see details of leaked memory
==52268==
==52268== For lists of detected and suppressed errors, rerun with: -s
==52268== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

> 如果不加 `-g` 参数，报告中就不会显示出错代码的行号信息（如 `func() (test.cpp:6)` 部分）。

完整内存泄漏检查：

```bash
valgrind --tool=memcheck --leak-check=full ./main_cpp
```

---

## 7. ASan 与 Valgrind 的区别

| 对比维度 | ASan（AddressSanitizer） | Valgrind |
| --- | --- | --- |
| **实现方式** | 静态和动态混合的工具，编译时插入额外代码，运行时检测内存访问错误（缓冲区溢出、使用已释放的内存等） | 动态二进制工具，运行时对二进制代码进行重写和模拟；提供更广泛的工具集（Memcheck、Cachegrind、Callgrind 等） |
| **性能开销** | 更快，编译时引入的运行时检查开销相对较小，对程序性能影响通常较小 | 更慢，运行时重写和模拟，大型应用程序的性能开销可能很高 |
| **检测能力** | 主要用于内存访问错误（缓冲区溢出、内存泄漏等），在这些方面非常强大 | Memcheck 除内存访问错误外，还能检测未初始化的内存访问、内存泄漏、不匹配的内存分配/释放等，某些情况下检测更全面 |

<!-- TODO: 原文档中"We Can Also Use perf"课程配图为飞书私有图片，无法在 GitHub 直接展示，请替换为可访问的图片链接。 -->

---

## 8. 参考文档

- [perf 的基本使用方法](https://www.coonote.com/vim-note/perf-usage.html)
- [perf（深入理解）](http://senlinzhan.github.io/2018/03/18/perf/)
- [阮一峰 - 如何读懂火焰图？](https://www.ruanyifeng.com/blog/2017/09/flame-graph.html)
- [使用 gdb 调试 coredump](http://senlinzhan.github.io/2017/12/31/coredump/)
- [使用 valgrind 检测 C/C++ 内存泄漏问题](http://senlinzhan.github.io/2017/12/31/valgrind/)
- [ASan 参考博客](https://cloud.tencent.com/developer/article/2000208)
