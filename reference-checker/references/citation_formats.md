# 参考文献格式规范

## 常用引用格式标准

### 1. GB/T 7714-2015（中国国家标准）

#### 期刊文章 [J]
```
[序号] 主要责任者. 文献题名[J]. 刊名, 年, 卷(期): 起止页码.

例：[1] 张三, 李四. 人工智能在医学中的应用[J]. 中华医学杂志, 2023, 103(5): 345-350.
```

#### 专著（书籍）[M]
```
[序号] 主要责任者. 书名[M]. 版本项. 出版地: 出版者, 出版年: 起止页码.

例：[2] 王五. 深度学习原理[M]. 2版. 北京: 清华大学出版社, 2022: 120-150.
```

#### 会议论文 [C]
```
[序号] 主要责任者. 题名[C]//会议名称. 出版地: 出版者, 出版年: 起止页码.

例：[3] 赵六. 新型算法研究[C]//第十二届全国计算机学术会议. 上海: 上海科技出版社, 2023: 45-50.
```

#### 学位论文 [D]
```
[序号] 主要责任者. 题名[D]. 保存地: 保存单位, 年份.

例：[4] 孙七. 基于深度学习的图像识别研究[D]. 北京: 北京大学, 2022.
```

#### 电子文献 [EB/OL]
```
[序号] 主要责任者. 题名[EB/OL]. (发布日期)[引用日期]. 获取路径.

例：[5] 周八. 机器学习入门教程[EB/OL]. (2023-01-15)[2023-06-20]. http://example.com/ml.
```

---

### 2. APA格式（第7版）

#### 期刊文章
```
作者姓, 名首字母. (年份). 文章标题. 期刊名, 卷号(期号), 页码. https://doi.org/xxxx

例：Smith, J. A., & Jones, M. B. (2023). The impact of AI on healthcare. Journal of Medical Informatics, 45(2), 112-128. https://doi.org/10.xxxx/jmi.2023.001
```

#### 书籍
```
作者姓, 名首字母. (年份). 书名(版次). 出版社.

例：Johnson, R. T. (2022). Artificial intelligence fundamentals (3rd ed.). Academic Press.
```

---

### 3. Vancouver格式（医学常用）

#### 期刊文章
```
作者. 文章标题. 期刊名. 年份;卷(期):页码.

例：Smith JA, Jones MB. The impact of AI on healthcare. J Med Inform. 2023;45(2):112-8.
```

#### 书籍
```
作者. 书名. 版次. 出版地: 出版社; 年份.

例：Johnson RT. Artificial intelligence fundamentals. 3rd ed. New York: Academic Press; 2022.
```

---

## 验证标识符

### DOI（数字对象标识符）
- **格式**：`10.xxxx/xxxxxx`
- **示例**：`10.1038/s41586-021-03819-2`
- **验证**：https://doi.org/{DOI}
- **搜索**：`doi:10.1038/s41586-021-03819-2` 或 `site:doi.org 10.1038/...`

### PubMed ID (PMID)
- **格式**：纯数字，1-8位
- **示例**：`12345678`
- **验证**：https://pubmed.ncbi.nlm.nih.gov/{PMID}/
- **搜索**：`PMID 12345678 pubmed`

### ISBN（国际标准书号）
- **ISBN-10**：10位数字
- **ISBN-13**：13位数字，通常以978或979开头
- **示例**：`978-3-16-148410-0`
- **验证**：Google Books、WorldCat、OpenLibrary

### ISSN（国际标准期刊编号）
- **格式**：8位数字，中间连字符
- **示例**：`1234-5678`
- **验证**：ISSN Portal https://portal.issn.org/

---

## 常见错误类型

### 1. 格式错误
- 缺少必要的标点符号
- 作者姓名格式不统一（中英文混用）
- 页码格式错误（应使用"123-125"）
- 缺少出版信息

### 2. 引用与参考文献不对应
- 文中引用了[5]，但参考文献列表只有4条
- 参考文献有[6]，但文中从未引用
- 同一文献被多个不同序号引用

### 3. 顺序错误
- 参考文献未按文中首次出现顺序编号
- 跳号（如从[3]直接跳到[5]）

### 4. 信息缺失
- 缺少DOI（期刊文章应尽量提供）
- 缺少出版社和出版地（书籍）
- 缺少访问日期（网页引用）

### 5. 真实性问题
- 虚构的DOI或PMID
- 错误的作者信息
- 不存在的期刊或会议
- 篡改的出版年份
- AI生成的虚假文献

---

## 验证资源

### 学术数据库
| 名称 | 链接 | 用途 |
|------|------|------|
| PubMed | https://pubmed.ncbi.nlm.nih.gov/ | 生物医学 |
| Google Scholar | https://scholar.google.com/ | 综合 |
| CNKI | https://www.cnki.net/ | 中文文献 |
| 万方 | https://www.wanfangdata.com.cn/ | 中文文献 |
| Web of Science | 需订阅 | 权威引文索引 |
| Scopus | 需订阅 | 综合引文索引 |

### DOI解析
| 名称 | 链接 |
|------|------|
| DOI.org | https://doi.org/ |
| CrossRef | https://search.crossref.org/ |

### 书籍搜索
| 名称 | 链接 |
|------|------|
| Google Books | https://books.google.com/ |
| WorldCat | https://www.worldcat.org/ |
| OpenLibrary | https://openlibrary.org/ |
| 国家图书馆 | http://www.nlc.cn/ |

### 期刊信息
| 名称 | 链接 | 用途 |
|------|------|------|
| UlrichsWeb | https://ulrichsweb.serialssolutions.com/ | 期刊权威数据库 |
| DOAJ | https://doaj.org/ | 开放获取期刊 |
| JCR | 需订阅 | 期刊影响因子 |
