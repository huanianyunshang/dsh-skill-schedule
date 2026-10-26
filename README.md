# dsh-skill-schedule

一个 DeepSeek Harness skill：**周/月计划 + 周/月复盘**，并且强制和真实课表、真实训练计划咬合。

不是日历插件，是一套可执行的流程：月计划管方向，周计划管落地，复盘只改一件，训练块先占位。

## 它解决什么

大多数人的计划不是「不会排」，是排完之后第二周就废：

- 课表没核，排进去的时段其实在上课
- 训练排在课后碎片里，被「今天累了」吃掉
- 复盘一次改三件事，一件都没改
- 状态差的日子没有降级方案，只能断更

这个 skill 把这几条写成硬规则，排表时逐条过一遍。

## 安装

DSH 按以下顺序扫描 skill 目录（rank 越小优先级越高）：

| Rank | 来源 | 路径 |
|---|---|---|
| 100 | project-dsh | `<项目根>/.dsh/skills` |
| 200 | project-agents | `<项目根>/.agents/skills` |
| 300 | custom | `Config.customSkillDirs` |
| 400 | user-dsh | `<dshHome>/skills` |

**个人安装（推荐）**：把本仓库目录放到 `<dshHome>/skills/schedule-planner`，例如：

```powershell
git clone https://github.com/<you>/dsh-skill-schedule.git "$env:USERPROFILE\.dsh\skills\schedule-planner"
```

**项目级安装**：clone 到项目根 `.dsh/skills/schedule-planner`，只在该项目生效。

装完在会话里说「做下周计划」，skill 应被加载。

## 用法

首次建档（三份基线）：

```
按 schedule-planner 的流程，帮我建 schedule/ 基础档
```

然后会问你：作息、课表、训练计划、学习目标。给它课表截图或导出文件、训练执行表即可。

日常：

| 你说 | 产出 |
|---|---|
| 做下个月的计划 | `plans/monthly/YYYY-MM.md` |
| 做下周计划 | `weekly/YYYY-Www.md` |
| 本周复盘 | `reviews/weekly/YYYY-Www.md` |
| 本月复盘 | `reviews/monthly/YYYY-MM.md` |
| 今天怎么安排 | 从周计划里取当天 |

## 目录

```
SKILL.md                  skill 主文件（加载指令）
templates/                四类计划模板 + 三份基线模板
  monthly-plan.md
  weekly-plan.md
  weekly-review.md
  monthly-review.md
  profile.md
  study-plan.md
  fitness-diet.md
  timetable.md
scripts/carb_cycle.py     碳循环克数计算器
examples/                 脱敏示例
```

## 碳循环计算器

```bash
python scripts/carb_cycle.py --weight 85 --body endo --protein 1.5
```

```
== 碳循环克数（85kg / 内胚型（容易胖） / 蛋白 1.5g/kg）==

项            每天       每周
碳水         170 g     1190 g
脂肪          68 g      476 g
蛋白       127.5 g    892.5 g

碳档      天     碳水/天     脂肪/天     蛋白/天        热量
高碳      2   297.5 g     35.7 g   127.5 g    2021 kcal
中碳      3   138.8 g     55.5 g   127.5 g    1565 kcal
低碳      2    89.2 g      119 g   127.5 g    1938 kcal

[!] 三档热量差 456 kcal（最高 2021 / 最低 1565）。
  原方法说三档应接近，差额靠加蔬菜补 —— 尤其别让中碳日变成挨饿日。

注：蛋白按 0.8–1.5 g/kg 取，减脂保肌建议 ≥1.2；训练日配高碳，休息日配低碳。
```

无第三方依赖，只要 Python 3.9+。

## 设计取舍

- **只改一件**：复盘一次改三件 = 一件都改不了
- **训练块先占位**：反过来做，训练必然被学习挤掉
- **如实记缺**：排不进去就记缺，不挪用休息日补练（破坏碳档与恢复）
- **最低完成线**：状态差的降级动作，可判定，不是道德要求

## License

MIT
