# 贪心

> 来源：灵茶山艾府的 [贪心题单](https://leetcode.cn/discuss/post/3091107/fen-xiang-gun-ti-dan-tan-xin-ji-ben-tan-k58yb/)；完整题目会随原题单更新，以各小节的「完整题单」链接为准。

贪心的关键不是“每次选看起来最好的”，而是要先定义局部选择，并证明它不会排除全局最优解。常见证明方法是交换论证法：把任意最优解中的某一步替换为贪心选择，证明答案不会变差。

## 刷题前检查

1. **排序后是否更容易决策？** 如果元素顺序和答案无关，优先尝试排序。
2. **能否固定当前选择？** 选最小、最大、最左、最右后，剩余问题是否同类。
3. **局部选择会不会损失未来？** 如果会，考虑堆和“反悔贪心”，或改用 DP。
4. **区间按什么排序？** 选最多不相交区间通常按右端点；合并区间通常按左端点。
5. **如何证明？** 尝试交换两个相邻决策，比较交换前后的答案。

---

## 10.1 基本贪心策略

### 10.1.1 从最小 / 最大开始贪心

**思路：** 排序后优先处理最小或最大的元素。典型目标是用有限资源尽量完成更多任务，或优先去掉影响最小的元素。

**代表题：**

- [3074. 重新分装苹果](https://leetcode.cn/problems/apple-redistribution-into-boxes/)
- [2279. 装满石头的背包的最大数量](https://leetcode.cn/problems/maximum-bags-with-full-capacity-of-rocks/)
- [1833. 雪糕的最大数量](https://leetcode.cn/problems/maximum-ice-cream-bars/)
- [2144. 打折购买糖果的最小开销](https://leetcode.cn/problems/minimum-cost-of-buying-candies-with-discount/)
- [1005. K 次取反后最大化的数组和](https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations/)
- [1710. 卡车上的最大单元数](https://leetcode.cn/problems/maximum-units-on-a-truck/)
- [945. 使数组唯一的最小增量](https://leetcode.cn/problems/minimum-increment-to-make-array-unique/)
- [1647. 字符频次唯一的最小删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-character-frequencies-unique/)

[完整题单](https://leetcode.cn/problem-list/hXx4UEmC/)

### 10.1.2 单序列配对

**思路：** 同一数组内部配对时，排序后通常让相邻元素配对，避免把大的差距留下。

**代表题：**

- [561. 数组拆分](https://leetcode.cn/problems/array-partition/)
- [1877. 数组中最大数对和的最小值](https://leetcode.cn/problems/minimize-maximum-pair-sum-in-array/)
- [881. 救生艇](https://leetcode.cn/problems/boats-to-save-people/)
- [2592. 最大化数组的伟大值](https://leetcode.cn/problems/maximize-greatness-of-an-array/)
- [2576. 求出最多标记下标](https://leetcode.cn/problems/find-the-maximum-number-of-marked-indices/)

[完整题单](https://leetcode.cn/problem-list/Ca4lFmGL/)

### 10.1.3 双序列配对

**思路：** 两个数组分别排序；根据目标选择“最小配最小”或“最小配最大”。双指针是常用实现。

**代表题：**

- [2037. 使每位学生都有座位的最少移动次数](https://leetcode.cn/problems/minimum-number-of-moves-to-seat-everyone/)
- [455. 分发饼干](https://leetcode.cn/problems/assign-cookies/)
- [2410. 运动员和训练师的最大匹配数](https://leetcode.cn/problems/maximum-matching-of-players-with-trainers/)
- [870. 优势洗牌](https://leetcode.cn/problems/advantage-shuffle/)
- [826. 安排工作以达到最大收益](https://leetcode.cn/problems/most-profit-assigning-work/)

[完整题单](https://leetcode.cn/problem-list/0XXpbxI5/)

### 10.1.4 从最左 / 最右开始贪心

**思路：** 当顺序不能随意改变时，扫描数组或字符串；让当前位置满足约束，并把影响传给后续位置。

**代表题：**

- [1827. 最少操作使数组递增](https://leetcode.cn/problems/minimum-operations-to-make-the-array-increasing/)
- [605. 种花问题](https://leetcode.cn/problems/can-place-flowers/)
- [2027. 转换字符串的最少操作次数](https://leetcode.cn/problems/minimum-moves-to-convert-string/)
- [3192. 使二进制数组全部等于 1 的最少操作次数 II](https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-ii/)
- [861. 翻转矩阵后的得分](https://leetcode.cn/problems/score-after-flipping-matrix/)
- [2366. 将数组排序的最少替换次数](https://leetcode.cn/problems/minimum-replacements-to-sort-the-array/)

[完整题单](https://leetcode.cn/problem-list/HbGPwmVI/)

### 10.1.5 划分型贪心

**思路：** 从左到右维护当前段；若加入下一个元素会违反约束，就在当前位置切段。

**代表题：**

- [1221. 分割平衡字符串](https://leetcode.cn/problems/split-a-string-in-balanced-strings/)
- [2405. 子字符串的最优划分](https://leetcode.cn/problems/optimal-partition-of-string/)
- [2294. 划分数组使最大差为 K](https://leetcode.cn/problems/partition-array-such-that-maximum-difference-is-k/)
- [2522. 将字符串分割成值不超过 K 的子字符串](https://leetcode.cn/problems/partition-string-into-substrings-with-values-at-most-k/)

[完整题单](https://leetcode.cn/problem-list/BThSBbqv/)

### 10.1.6 先枚举，再贪心

**思路：** 枚举一个关键值、最终状态或分界点；在该条件固定后，剩余部分可以按贪心求最优。

**代表题：**

- [2171. 拿出最少数目的魔法豆](https://leetcode.cn/problems/removing-minimum-number-of-magic-beans/)
- [3085. 成为 K 特殊字符串需要删除的最少字符数](https://leetcode.cn/problems/minimum-deletions-to-make-string-k-special/)
- [1727. 重新排列后的最大子矩阵](https://leetcode.cn/problems/largest-submatrix-with-rearrangements/)
- [2910. 合法分组的最少组数](https://leetcode.cn/problems/minimum-number-of-groups-to-create-a-valid-assignment/)

[完整题单](https://leetcode.cn/problem-list/5ex0hHxT/)

### 10.1.7 交换论证法

**思路：** 猜测处理顺序后，交换相邻两项，证明交换不会让答案变差；据此确定排序规则。

**代表题：**

- [1877. 数组中最大数对和的最小值](https://leetcode.cn/problems/minimize-maximum-pair-sum-in-array/)
- [2895. 最小处理时间](https://leetcode.cn/problems/minimum-processing-time/)
- [1665. 完成所有任务的最少初始能量](https://leetcode.cn/problems/minimum-initial-energy-to-finish-tasks/)
- [2136. 全部开花的最早一天](https://leetcode.cn/problems/earliest-possible-day-of-full-bloom/)

[完整题单](https://leetcode.cn/problem-list/X2aHytcZ/)

### 10.1.8 相邻不同

**思路：** 先比较最高频元素出现次数与其余元素数量，判断能否把高频元素插开；常配合大根堆。

**代表题：**

- [2335. 装满杯子需要的最短总时长](https://leetcode.cn/problems/minimum-amount-of-time-to-fill-cups/)
- [1753. 移除石子的最大得分](https://leetcode.cn/problems/maximum-score-from-removing-stones/)
- [767. 重构字符串](https://leetcode.cn/problems/reorganize-string/)
- [1054. 距离相等的条形码](https://leetcode.cn/problems/distant-barcodes/)
- [621. 任务调度器](https://leetcode.cn/problems/task-scheduler/)

[完整题单](https://leetcode.cn/problem-list/pA6sYOTz/)

### 10.1.9 反悔贪心

**思路：** 先选择当前看起来可行的方案；一旦发现不满足约束，就撤销代价最大或收益最小的历史选择。通常用堆实现。

**代表题：**

- [LCP 30. 魔塔游戏](https://leetcode.cn/problems/p0NxJO/)
- [1642. 可以到达的最远建筑](https://leetcode.cn/problems/furthest-building-you-can-reach/)
- [630. 课程表 III](https://leetcode.cn/problems/course-schedule-iii/)
- [871. 最低加油次数](https://leetcode.cn/problems/minimum-number-of-refueling-stops/)
- [2813. 子序列最大优雅度](https://leetcode.cn/problems/maximum-elegance-of-a-k-length-subsequence/)

[完整题单](https://leetcode.cn/problem-list/fWNS1Enz/)

---

## 10.2 区间贪心

### 10.2.1 不相交区间

**规则：** 按右端点升序，优先保留结束最早的区间，为后面留下最多空间。

- [435. 无重叠区间](https://leetcode.cn/problems/non-overlapping-intervals/)
- [646. 最长数对链](https://leetcode.cn/problems/maximum-length-of-pair-chain/)
- [1520. 最多的不重叠子字符串](https://leetcode.cn/problems/maximum-number-of-non-overlapping-substrings/)

[完整题单](https://leetcode.cn/problem-list/F04huxG0/)

### 10.2.2 区间分组

**规则：** 按左端点排序；用最小堆维护每组的结束时间。当前区间能复用最早结束的一组时复用，否则新开一组。

- [2406. 将区间分为最少组数](https://leetcode.cn/problems/divide-intervals-into-minimum-number-of-groups/)
- [253. 会议室 II](https://leetcode.cn/problems/meeting-rooms-ii/)（会员题）

[完整题单](https://leetcode.cn/problem-list/97JcWfiV/)

### 10.2.3 区间选点

**规则：** 按右端点排序，每次把点放在当前尚未覆盖区间的最右端，能覆盖尽量多的后续区间。

- [452. 用最少数量的箭引爆气球](https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/)
- [757. 设置交集大小至少为 2](https://leetcode.cn/problems/set-intersection-size-at-least-two/)
- [2589. 完成所有任务的最少时间](https://leetcode.cn/problems/minimum-time-to-complete-all-tasks/)

[完整题单](https://leetcode.cn/problem-list/0G1x696r/)

### 10.2.4 区间覆盖

**规则：** 在当前可覆盖范围内，选择右端点最远的区间；若无法向前推进则无解。

- [45. 跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/)
- [1024. 视频拼接](https://leetcode.cn/problems/video-stitching/)
- [1326. 灌溉花园的最少水龙头数目](https://leetcode.cn/problems/minimum-number-of-taps-to-open-to-water-a-garden/)

[完整题单](https://leetcode.cn/problem-list/y8H3iG0Y/)

### 10.2.5 合并区间

**规则：** 按左端点排序，维护已合并区间的右端点；新区间重叠则更新右端点，否则开新段。

- [56. 合并区间](https://leetcode.cn/problems/merge-intervals/)
- [57. 插入区间](https://leetcode.cn/problems/insert-interval/)
- [55. 跳跃游戏](https://leetcode.cn/problems/jump-game/)
- [763. 划分字母区间](https://leetcode.cn/problems/partition-labels/)

[完整题单](https://leetcode.cn/problem-list/H98XrMCK/)

### 10.2.6 其他区间贪心

- [1288. 删除被覆盖区间](https://leetcode.cn/problems/remove-covered-intervals/)
- [1705. 吃苹果的最大数目](https://leetcode.cn/problems/maximum-number-of-eaten-apples/)
- [1353. 最多可以参加的会议数目](https://leetcode.cn/problems/maximum-number-of-events-that-can-be-attended/)
- [2054. 两个最好的不重叠活动](https://leetcode.cn/problems/two-best-non-overlapping-events/)

[完整题单](https://leetcode.cn/problem-list/dPUurL9H/)

---

## 10.3 字典序贪心

### 10.3.1 字典序最小 / 最大

**思路：** 字典序由最靠左的不同位置决定。因此优先在前缀处放更小或更大的可行字符，同时保证剩余部分还能完成。

- [1323. 6 和 9 组成的最大数字](https://leetcode.cn/problems/maximum-69-number/)
- [2697. 字典序最小回文串](https://leetcode.cn/problems/lexicographically-smallest-palindrome/)
- [1881. 插入后的最大值](https://leetcode.cn/problems/maximum-value-after-insertion/)
- [1663. 具有给定数值的最小字符串](https://leetcode.cn/problems/smallest-string-with-a-given-numeric-value/)
- [1328. 破坏回文串](https://leetcode.cn/problems/break-a-palindrome/)
- [738. 单调递增的数字](https://leetcode.cn/problems/monotone-increasing-digits/)
- [670. 最大交换](https://leetcode.cn/problems/maximum-swap/)

[完整题单](https://leetcode.cn/problem-list/Rj3RPiwu/)

### 10.3.2 回文串贪心

**思路：** 回文要求两侧成对。先统计字符次数或从两端决策，再把奇数次数、中心位置和字典序限制分别处理。

- [409. 最长回文串](https://leetcode.cn/problems/longest-palindrome/)
- [680. 验证回文串 II](https://leetcode.cn/problems/valid-palindrome-ii/)
- [2384. 最大回文数字](https://leetcode.cn/problems/largest-palindromic-number/)
- [1400. 构造 K 个回文字符串](https://leetcode.cn/problems/construct-k-palindrome-strings/)
- [2131. 连接两字母单词得到的最长回文串](https://leetcode.cn/problems/longest-palindrome-by-concatenating-two-letter-words/)

[完整题单](https://leetcode.cn/problem-list/TEEhCLX2/)

---

## 10.4 数学贪心

### 10.4.1 基础

- [2160. 拆分数位后四位数字的最小和](https://leetcode.cn/problems/minimum-sum-of-four-digit-number-after-splitting-digits/)
- [2578. 最小和分割](https://leetcode.cn/problems/split-with-minimum-sum/)
- [2244. 完成所有任务需要的最少轮数](https://leetcode.cn/problems/minimum-rounds-to-complete-all-tasks/)
- [2870. 使数组为空的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-empty/)
- [1217. 玩筹码](https://leetcode.cn/problems/minimum-cost-to-move-chips-to-the-same-position/)

[完整题单](https://leetcode.cn/problem-list/WD43sGvX/)

### 10.4.2 乘积贪心

**要点：** 注意负数个数、绝对值和符号。最大乘积常比较最大三个数与最小两个数乘最大数。

- [628. 三个数的最大乘积](https://leetcode.cn/problems/maximum-product-of-three-numbers/)
- [1567. 乘积为正数的最长子数组长度](https://leetcode.cn/problems/maximum-length-of-subarray-with-positive-product/)

[完整题单](https://leetcode.cn/problem-list/pblWWEeC/)

### 10.4.3 排序不等式

**要点：** 两个序列同序配对通常最大化乘积和，逆序配对通常最小化乘积和。

- [2285. 道路的最大总重要性](https://leetcode.cn/problems/maximum-total-importance-of-roads/)
- [3016. 输入单词需要的最少按键次数 II](https://leetcode.cn/problems/minimum-number-of-pushes-to-type-word-ii/)
- [1402. 做菜顺序](https://leetcode.cn/problems/reducing-dishes/)
- [1589. 所有排列中的最大和](https://leetcode.cn/problems/maximum-sum-obtained-of-any-permutation/)

[完整题单](https://leetcode.cn/problem-list/vAzHtfPn/)

### 10.4.4 基本不等式

**要点：** 在和固定时，乘积通常在各部分尽量均衡时达到最优；遇到平方和、乘积或拆分问题时可尝试此方向。

- [1969. 数组元素的最小非零乘积](https://leetcode.cn/problems/minimum-non-zero-product-of-the-array-elements/)
- [2939. 最大异或乘积](https://leetcode.cn/problems/maximum-xor-product/)
- [2897. 对数组执行操作使平方和最大](https://leetcode.cn/problems/apply-operations-on-array-to-maximize-sum-of-squares/)

[完整题单](https://leetcode.cn/problem-list/VAsNbuYm/)

### 10.4.5 中位数贪心

**要点：** 最小化到所有点的绝对距离和时，目标取中位数；最大化配对类问题时，先排序再选定位置。

- [462. 最少移动次数使数组元素相等 II](https://leetcode.cn/problems/minimum-moves-to-equal-array-elements-ii/)
- [1552. 两球之间的磁力](https://leetcode.cn/problems/magnetic-force-between-two-balls/)
- [2966. 划分数组使最大差为 K](https://leetcode.cn/problems/divide-array-into-arrays-with-max-difference/)

[完整题单](https://leetcode.cn/problem-list/GX4gGXE0/)

### 10.4.6 归纳法

**思路：** 从小规模结论寻找递推规律，再证明加入一个元素后结论仍成立。

[完整题单](https://leetcode.cn/problem-list/ct0noofX/)

### 10.4.7 其他数学贪心

[完整题单](https://leetcode.cn/problem-list/6FYmIaCF/)

---

## 10.5 思维题

### 10.5.1 从特殊到一般

**方法：** 先手算长度为 1、2、3 的情况，再观察极端数据：全相等、只有一个异常值、仅两类元素等。

- [2745. 构造最长的新字符串](https://leetcode.cn/problems/construct-the-longest-new-string/)
- [1029. 两地调度](https://leetcode.cn/problems/two-city-scheduling/)
- [2645. 构造有效字符串的最少插入数](https://leetcode.cn/problems/minimum-additions-to-make-valid-string/)
- [2202. K 次操作后最大化顶端元素](https://leetcode.cn/problems/maximize-the-topmost-element-after-k-moves/)
- [1702. 修改后的最大二进制字符串](https://leetcode.cn/problems/maximum-binary-string-after-change/)

[完整题单](https://leetcode.cn/problem-list/HkiqWNrS/)

### 10.5.2 脑筋急转弯

**方法：** 先排除无关信息，找不变量、奇偶性、最大值 / 最小值或必然发生的结构。

- [2733. 既不是最小值也不是最大值](https://leetcode.cn/problems/neither-minimum-nor-maximum/)
- [1903. 字符串中的最大奇数](https://leetcode.cn/problems/largest-odd-number-in-string/)
- [1689. 十-二进制数的最少数目](https://leetcode.cn/problems/partitioning-into-minimum-number-of-deci-binary-numbers/)
- [1007. 行相等的最少多米诺旋转](https://leetcode.cn/problems/minimum-domino-rotations-for-equal-row/)
- [463. 岛屿的周长](https://leetcode.cn/problems/island-perimeter/)

[完整题单](https://leetcode.cn/problem-list/ue0NqYCr/)

### 10.5.3 逆向思维

**方法：** 正向操作分支多时，从目标倒推；逆向操作常更少、单调性更强。

- [2139. 得到目标值的最少行动次数](https://leetcode.cn/problems/minimum-moves-to-reach-target-score/)
- [991. 坏了的计算器](https://leetcode.cn/problems/broken-calculator/)
- [780. 到达终点](https://leetcode.cn/problems/reaching-points/)
- [1558. 得到目标数组的最少函数调用次数](https://leetcode.cn/problems/minimum-numbers-of-function-calls-to-make-target-array/)
- [936. 戳印序列](https://leetcode.cn/problems/stamping-the-sequence/)

[完整题单](https://leetcode.cn/problem-list/IEBgD9HL/)

---

## 10.6 构造题

**思路：** 先确认答案是否必然存在；再寻找可以直接满足约束的排列、分配或矩阵。构造题经常不要求唯一答案。

- [1304. 和为零的 N 个不同整数](https://leetcode.cn/problems/find-n-unique-integers-sum-up-to-zero/)
- [942. 增减字符串匹配](https://leetcode.cn/problems/di-string-match/)
- [1253. 重构 2 行二进制矩阵](https://leetcode.cn/problems/reconstruct-a-2-row-binary-matrix/)
- [969. 煎饼排序](https://leetcode.cn/problems/pancake-sorting/)
- [406. 根据身高重建队列](https://leetcode.cn/problems/queue-reconstruction-by-height/)
- [1605. 给定行和列的和求可行矩阵](https://leetcode.cn/problems/find-valid-matrix-given-row-and-column-sums/)
- [1980. 找出不同的二进制字符串](https://leetcode.cn/problems/find-unique-binary-string/)
- [932. 漂亮数组](https://leetcode.cn/problems/beautiful-array/)

[完整题单](https://leetcode.cn/problem-list/CDHFrNJF/)

## 10.7 其他

用于收录不适合以上分类、但仍能通过局部选择或构造发现规律的题目；做题时优先写出小样例，明确每次选择对答案的影响。

[完整题单](https://leetcode.cn/problem-list/qkgusKjH/)

## 题解记录模板

每道题建议记录以下内容：

```md
# 题号. 题名

- 题目链接：
- 贪心选择：
- 为什么局部最优能推出全局最优：
- 排序 / 堆 / 双指针的作用：
- 时间复杂度：
- 空间复杂度：
- 易错点：
```
