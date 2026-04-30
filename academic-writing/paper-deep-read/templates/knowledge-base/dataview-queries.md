# Dataview 常用查询汇总

> 本文件收录论文笔记知识库中最常用的 Dataview 查询，按功能分类。

---

## 一、按域列出所有论文

### 1.1 基础论文列表
```dataview
TABLE title as 标题, authors as 作者, year as 年份, journal as 期刊
FROM ""
WHERE type = "paper" AND note_version > 0
SORT year DESC
```

### 1.2 指定领域论文
```dataview
TABLE title as 标题, year as 年份, paper_type as 类型, read_depth as 阅读深度
FROM "01-Bioinformatics"
WHERE note_version > 0
SORT year DESC
```

### 1.3 跨领域论文搜索
```dataview
TABLE title as 标题, domains as 领域, year as 年份
FROM ""
WHERE contains(domains, "bioinformatics") OR contains(domains, "ai-ml")
SORT year DESC
```

---

## 二、按方法筛选

### 2.1 单方法筛选
```dataview
TABLE title as 标题, year as 年份, domains as 领域, databases as 数据库
FROM ""
WHERE contains(methods, "RNA-seq")
SORT year DESC
```

### 2.2 多方法组合筛选
```dataview
TABLE title as 标题, year as 年份, methods as 方法
FROM ""
WHERE contains(methods, "scRNA-seq") AND contains(methods, "trajectory analysis")
SORT year DESC
```

### 2.3 方法排除筛选
```dataview
TABLE title as 标题, year as 年份, methods as 方法
FROM ""
WHERE contains(methods, "machine learning") AND !contains(methods, "deep learning")
SORT year DESC
```

---

## 三、按日期范围筛选

### 3.1 按年份范围
```dataview
TABLE title as 标题, journal as 期刊, year as 年份
FROM ""
WHERE year >= 2020 AND year <= 2024
SORT year DESC
```

### 3.2 按阅读日期
```dataview
TABLE title as 标题, read_date as 阅读日期, read_depth as 深度
FROM ""
WHERE read_date >= 2024-01-01
SORT read_date DESC
```

### 3.3 本月阅读
```dataview
TABLE title as 标题, read_date as 阅读日期, read_depth as 深度
FROM ""
WHERE read_date >= date(today) - dur(30 days)
SORT read_date DESC
```

### 3.4 近一年阅读
```dataview
TABLE title as 标题, read_date as 阅读日期, read_depth as 深度
FROM ""
WHERE read_date >= date(today) - dur(365 days)
SORT read_date DESC
```

---

## 四、按工具筛选

### 4.1 使用特定工具的论文
```dataview
TABLE title as 标题, year as 年份, tools as 工具, domains as 领域
FROM ""
WHERE contains(tools, "Seurat")
SORT year DESC
```

### 4.2 工具版本记录
```dataview
TABLE title as 标题, tools as 工具, databases as 数据库
FROM ""
WHERE contains(tools, "Python")
FLATTEN tools
GROUP BY tools
```

---

## 五、统计仪表板

### 5.1 论文总数统计
```dataview
TABLE length(file.list) as 论文总数
FROM ""
WHERE type = "paper" AND note_version > 0
GROUP BY true
```

### 5.2 各领域论文数量
```dataview
TABLE domain as 领域, length(files) as 论文数
FROM ""
WHERE type = "paper"
FLATTEN domains as domain
GROUP BY domain
SORT length(files) DESC
```

### 5.3 方法使用频率排行
```dataview
TABLE method as 方法, count(*) as 使用次数
FROM ""
WHERE type = "paper"
FLATTEN methods as method
GROUP BY method
SORT count(*) DESC
LIMIT 15
```

### 5.4 工具使用频率排行
```dataview
TABLE tool as 工具, count(*) as 使用次数
FROM ""
WHERE type = "paper"
FLATTEN tools as tool
GROUP BY tool
SORT count(*) DESC
LIMIT 15
```

### 5.5 数据库使用频率
```dataview
TABLE database as 数据库, count(*) as 使用次数
FROM ""
WHERE type = "paper"
FLATTEN databases as database
GROUP BY database
SORT count(*) DESC
```

### 5.6 年度发表统计
```dataview
TABLE year as 年份, length(files) as 论文数
FROM ""
WHERE type = "paper"
GROUP BY year
SORT year DESC
```

---

## 六、近期阅读列表

### 6.1 本周新增
```dataview
TABLE title as 标题, read_date as 阅读日期, read_depth as 深度
FROM ""
WHERE read_date >= date(today) - dur(7 days)
SORT read_date DESC
```

### 6.2 未读论文
```dataview
TABLE title as 标题, journal as 期刊, year as 年份
FROM ""
WHERE read_depth = "overview" AND type = "paper"
SORT year DESC
```

### 6.3 阅读进度概览
```dataview
TABLE read_depth as 阅读深度, length(files) as 论文数
FROM ""
WHERE type = "paper"
GROUP BY read_depth
```

---

## 七、高评分论文

### 7.1 指定评分以上
```dataview
TABLE title as 标题, year as 年份, rating as 评分, journal as 期刊
FROM ""
WHERE rating >= 4 AND type = "paper"
SORT rating DESC
```

### 7.2 领域内高分论文
```dataview
TABLE title as 标题, year as 年份, rating as 评分, domains as 领域
FROM ""
WHERE rating >= 4 AND contains(domains, "bioinformatics")
SORT rating DESC
LIMIT 10
```

---

## 八、未完成笔记

### 8.1 草稿状态
```dataview
TABLE title as 标题, read_date as 阅读日期, note_version as 版本
FROM ""
WHERE note_version < 1 AND type = "paper"
SORT read_date DESC
```

### 8.2 缺少关键词
```dataview
TABLE title as 标题, read_date as 阅读日期
FROM ""
WHERE length(keywords) < 3 AND type = "paper"
SORT read_date DESC
```

### 8.3 需要补充的论文
```dataview
TABLE title as 标题, year as 年份
FROM ""
WHERE !contains(file.tags, "method") AND type = "paper"
SORT year DESC
```

---

## 九、相关文献网络

### 9.1 同作者论文
```dataview
TABLE title as 标题, year as 年份, journal as 期刊
FROM ""
WHERE contains(authors, "{{作者名}}")
SORT year DESC
```

### 9.2 同期刊论文
```dataview
TABLE title as 标题, year as 年份, authors as 作者
FROM ""
WHERE contains(journal, "{{期刊名}}")
SORT year DESC
```

### 9.3 引用关系追溯
```dataview
TABLE title as 标题, year as 年份, related_links as 相关链接
FROM ""
WHERE contains(related_links, "{{论文标题}}")
SORT year DESC
```

### 9.4 同方法论文
```dataview
TABLE title as 标题, year as 年份, methods as 方法, rating as 评分
FROM ""
WHERE contains(methods, "{{方法}}")
SORT rating DESC
```

---

## 十、方法使用频率排行

### 10.1 方法组合分析
```dataview
TABLE method_pair as 方法组合, count(*) as 论文数
FROM ""
WHERE type = "paper"
FLATTEN methods as m1
FLATTEN methods as m2
WHERE m1 < m2
GROUP BY m1 + " + " + m2 as method_pair
SORT count(*) DESC
LIMIT 10
```

### 10.2 趋势分析方法
```dataview
TABLE year as 年份, method as 方法, count(*) as 使用次数
FROM ""
WHERE type = "paper"
FLATTEN methods as method
WHERE method = "scRNA-seq" OR method = "RNA-seq" OR method = "ATAC-seq"
GROUP BY year, method
SORT year ASC
```

### 10.3 新兴方法检测
```dataview
TABLE method as 方法, year as 首次使用年份
FROM ""
WHERE type = "paper"
FLATTEN methods as method
GROUP BY method
SORT year ASC
LIMIT 10
```

---

## 十一、自定义查询模板

### 11.1 综合搜索查询
```dataview
TABLE title as 标题, year as 年份, journal as 期刊, paper_type as 类型, read_depth as 深度
FROM ""
WHERE type = "paper"
    AND year >= {{起始年}}
    AND contains(domains, "{{领域}}")
    AND (contains(methods, "{{方法1}}") OR contains(methods, "{{方法2}}"))
SORT year DESC
```

### 11.2 复现优先级
```dataview
TABLE title as 标题, year as 年份, read_depth as 阅读深度, tools as 工具
FROM ""
WHERE type = "paper"
    AND read_depth = "reproduction"
    AND contains(tools, "{{工具}}")
SORT year DESC
```

### 11.3 论文对比集
```dataview
TABLE title as 标题, year as 年份, paper_type as 类型, methods as 方法
FROM ""
WHERE contains(title, "{{关键词}}")
SORT year DESC
```

---

## 查询使用技巧

### 参数说明
| 参数 | 说明 | 示例 |
|------|------|------|
| `TABLE` | 选择显示的列 | `TABLE title, year` |
| `FROM` | 指定搜索范围 | `FROM "01-Bioinformatics"` |
| `WHERE` | 筛选条件 | `WHERE year >= 2020` |
| `SORT` | 排序方式 | `SORT year DESC` |
| `LIMIT` | 限制返回数量 | `LIMIT 10` |
| `FLATTEN` | 展开数组字段 | `FLATTEN methods` |
| `GROUP BY` | 分组统计 | `GROUP BY year` |

### 常用字段
| 字段 | 说明 | 示例值 |
|------|------|--------|
| `title` | 论文标题 | "Title" |
| `year` | 发表年份 | 2023 |
| `journal` | 期刊名 | "Nature" |
| `authors` | 作者列表 | [author1, author2] |
| `paper_type` | 论文类型 | "discovery" |
| `domains` | 研究领域 | [bioinformatics] |
| `methods` | 使用方法 | [RNA-seq, DE] |
| `tools` | 使用工具 | [Seurat, Python] |
| `databases` | 相关数据库 | [GEO, PDB] |
| `read_date` | 阅读日期 | 2024-01-15 |
| `read_depth` | 阅读深度 | "reproduction" |
| `note_version` | 笔记版本 | 1 |
| `rating` | 评分 | 4.5 |

### 高级技巧
- 使用 `contains()` 检查数组字段是否包含值
- 使用 `date(today)` 获取当前日期
- 使用 `dur()` 创建时间跨度
- 使用 `FLATTEN` 展开数组后可用 `GROUP BY` 统计
