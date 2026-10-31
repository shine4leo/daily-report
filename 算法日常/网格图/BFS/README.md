# 网格图 · BFS

> 来源：灵茶山艾府 [网格图（DFS / BFS / 综合应用）题单](https://leetcode.cn/discuss/post/YiXPXW/)。题目顺序沿用原题单。

## 适用场景

BFS 适合计算**无权图中的最短距离**：每次移动代价相同，例如网格中向上下左右移动一步。

- DFS 像沿一条路走到底后再回溯。
- BFS 像往水塘中扔石头：从起点开始一圈圈向外扩散，先访问距离近的格子，再访问距离远的格子。
- 一个格子**第一次入队**时，得到的就是从起点到它的最短距离。
- 时间复杂度为 `O(mn)`，每个格子至多入队一次；`m × n` 是网格大小。

## 单源最短路模板

```cpp
#include <queue>
#include <utility>
#include <vector>

using namespace std;

constexpr int DIRS[4][2] = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}}; // 左右上下

// 返回从 (start_x, start_y) 出发，到其余格子的最短距离
// grid 中 '.' 表示可以通行的格子，可按题意修改
// 时间复杂度 O(mn)
vector<vector<int>> bfsGrid(
    vector<vector<char>>& grid,
    int start_x,
    int start_y
) {
    int m = grid.size(), n = grid[0].size();
    vector dis(m, vector<int>(n, -1));
    queue<pair<int, int>> q;

    dis[start_x][start_y] = 0;
    q.emplace(start_x, start_y);

    while (!q.empty()) {
        auto [i, j] = q.front();
        q.pop();

        for (auto [dx, dy] : DIRS) {
            int x = i + dx, y = j + dy;

            // 这里 grid[x][y] == '.' 根据题意修改
            if (0 <= x && x < m && 0 <= y && y < n &&
                grid[x][y] == '.' && dis[x][y] < 0) {
                dis[x][y] = dis[i][j] + 1;
                q.emplace(x, y);
            }
        }
    }

    return dis;
}
```

### 模板要点

- `dis[x][y] == -1` 同时表示“未访问”。
- **入队时**立刻设置距离，避免同一格子被重复入队。
- 遇到障碍、越界或已访问的格子直接跳过。
- 终点第一次出队或第一次入队时即可返回，取决于代码的检查位置。
- 多源 BFS：把所有起点都以距离 `0` 入队，再按同一模板扩散。适用于腐烂的橘子、01 矩阵、地图中的最高点等题。

## BFS 题单

### 基础最短路

1. [1926. 迷宫中离入口最近的出口](https://leetcode.cn/problems/nearest-exit-from-entrance-in-maze/) · 1638
2. [1091. 二进制矩阵中的最短路径](https://leetcode.cn/problems/shortest-path-in-binary-matrix/) · 1658
3. [1162. 地图分析](https://leetcode.cn/problems/as-far-from-land-as-possible/) · 1666
4. [542. 01 矩阵](https://leetcode.cn/problems/01-matrix/)
5. [994. 腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/) · 做到 `O(mn)`
6. [3905. 多源图像渲染](https://leetcode.cn/problems/multi-source-flood-fill/) · 1671
7. [1765. 地图中的最高点](https://leetcode.cn/problems/map-of-highest-peak/) · 1783
8. [934. 最短的桥](https://leetcode.cn/problems/shortest-bridge/) · 1826
9. [2146. 价格范围内最高排名的 K 样物品](https://leetcode.cn/problems/k-highest-ranked-items-within-a-price-range/) · 1837
10. [1293. 网格中的最短路径](https://leetcode.cn/problems/shortest-path-in-a-grid-with-obstacles-elimination/) · 1967
11. [909. 蛇梯棋](https://leetcode.cn/problems/snakes-and-ladders/) · 2020
12. [1210. 穿过迷宫的最少移动次数](https://leetcode.cn/problems/minimum-moves-to-reach-target-with-rotations/) · 2022
13. [675. 为高尔夫比赛砍树](https://leetcode.cn/problems/cut-off-trees-for-golf-event/)
14. [2812. 找出最安全路径](https://leetcode.cn/problems/find-the-safest-path-in-a-grid/) · 2154
15. [749. 隔离病毒](https://leetcode.cn/problems/contain-virus/) · 2277

### 会员题

16. [1730. 获取食物的最短路径](https://leetcode.cn/problems/shortest-path-to-get-food/)（会员题）
17. [286. 墙与门](https://leetcode.cn/problems/walls-and-gates/)（会员题）
18. [490. 迷宫](https://leetcode.cn/problems/the-maze/)（会员题）
19. [505. 迷宫 II](https://leetcode.cn/problems/the-maze-ii/)（会员题）
20. [499. 迷宫 III](https://leetcode.cn/problems/the-maze-iii/)（会员题）
21. [1197. 进击的骑士](https://leetcode.cn/problems/minimum-knight-moves/)（会员题）
22. [317. 离建筑物最近的距离](https://leetcode.cn/problems/shortest-distance-from-all-buildings/)（会员题）
23. [2814. 避免淹死并到达目的地的最短时间](https://leetcode.cn/problems/minimum-time-takes-to-reach-destination-without-drowning/)（会员题）

## 刷题提示

| 题目特征 | 常见做法 |
| --- | --- |
| 一个起点，所有移动代价相同 | 单源 BFS |
| 多个起点同时扩散 | 多源 BFS |
| 状态除了坐标还包含剩余次数、方向或钥匙集合 | 将完整状态放入队列，并用对应状态去重 |
| 边权只有 0 和 1 | 0-1 BFS |
| 边权不相同 | Dijkstra，而非普通 BFS |

> 普通 BFS 的前提是每条边权相同。不要把“能走到”误当作“最短路一定能用 BFS”。

## 来源

作者：灵茶山艾府  
原帖：[网格图（DFS / BFS / 综合应用）](https://leetcode.cn/discuss/post/YiXPXW/)  
来源：力扣（LeetCode）

> 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
