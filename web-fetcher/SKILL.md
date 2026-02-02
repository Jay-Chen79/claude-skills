---
name: web-fetcher
description: "使用 curl/Python 替代 WebSearch 获取网页内容。当 WebSearch 或 webReader 达到配额限制时使用，或者用户主动要求用 fetch 方式获取网页内容。触发词：'用fetch'、'用curl'、'抓取网页'、'绕过搜索限制'等。"
---

# Web Fetcher - 无联网限制的网页获取工具

当 WebSearch/webReader 达到配额限制时，使用 curl + Python 替代方案获取网页内容。

## 核心原理

```
WebSearch/webReader: 有月度配额限制，受限时返回 429 错误
curl + Python: 无限制，直接通过系统命令获取网页
```

## 适用场景

1. **WebSearch 配额已满** - 收到 "Usage limit reached" 错误
2. **webReader 配额已满** - 收到 "MCP error -429" 错误
3. **用户明确要求** - 用户说"用 fetch"、"用 curl" 等
4. **需要大量请求** - 批量抓取多个页面
5. **需要原始 HTML** - 需要完整网页源码进行分析

## 可用功能

### 1. 新闻热点抓取

```python
# 搜狐新闻
curl -s "https://news.sohu.com" | 解析标题

# 网易新闻
curl -s "https://news.163.com"

# 新浪新闻
curl -s "https://news.sina.com.cn"
```

### 2. 天气信息

```bash
# wttr.in API（无限制）
curl -s "https://wttr.in/城市名?lang=zh"
curl -s "https://wttr.in/Beijing?lang=zh&format=3"
```

### 3. 网页内容提取

```python
# 提取页面标题和正文
curl -s "URL" | grep/Python解析
```

### 4. API 调用

```bash
# 直接调用公开 API
curl -s "API_URL"
```

## 执行流程

### Step 1: 判断需求

当用户请求需要联网时，首先判断：

```
用户请求 → 需要联网获取信息？
         ↓ Yes
    WebSearch 可用？
         ↓ No (配额已满/错误)
    使用 web-fetcher skill
```

### Step 2: 确定目标

明确要获取的内容类型：

| 内容类型 | 推荐方法 |
|---------|---------|
| 新闻热点 | 解析新闻网站首页 |
| 天气信息 | wttr.in API |
| 搜索结果 | 直接访问新闻聚合网站 |
| 特定网页 | curl + 解析 HTML |
| API 数据 | 直接 curl API |

### Step 3: 执行抓取

#### 方法 A: 直接 curl（适合简单输出）

```bash
# 天气
curl -s "https://wttr.in/温州?lang=zh&format=3"

# 简单网页
curl -s "URL" | grep 关键词
```

#### 方法 B: Python 解析（适合复杂页面）

```python
python3 << 'EOF'
import urllib.request
import re
import html

url = '目标URL'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req, timeout=10)
html_content = response.read().decode('utf-8')

# 解析逻辑
titles = re.findall(r'pattern', html_content)
# 处理并输出
EOF
```

#### 方法 C: 保存后解析（适合大页面）

```bash
# 先保存
curl -s "URL" > /tmp/page.html

# 再解析
grep -o 'pattern' /tmp/page.html | head -N
```

### Step 4: 清理输出

将抓取的原始数据整理成易读格式：

```
原始数据 → 提取关键信息 → 格式化展示
```

## 常用网站解析模板

### 搜狐新闻

```bash
curl -s "https://news.sohu.com" | Python解析链接和标题
```

### 163 网易

```bash
curl -s "https://news.163.com" | 提取新闻列表
```

### 微博热搜

```bash
# 直接访问微博热搜页面或 API
curl -s "微博热搜URL"
```

### 知乎热榜

```bash
curl -s "https://www.zhihu.com/hot" | 解析热榜
```

### 天气查询

```bash
# wttr.in
curl -s "https://wttr.in/城市?lang=zh"

# 中国天气网（备用）
curl -s "http://www.weather.com.cn/weather/城市代码.shtml"
```

## 注意事项

1. **编码问题** - 中文网页需指定 UTF-8 解码
2. **User-Agent** - 某些网站需要模拟浏览器
3. **动态内容** - JavaScript 渲染的内容可能抓取不到
4. **请求频率** - 避免过快请求导致被封 IP
5. **数据验证** - 抓取结果需要验证是否有效

## 错误处理

### 如果 curl 失败

```bash
# 尝试添加 headers
curl -s -H "User-Agent: Mozilla/5.0" "URL"

# 尝试其他镜像/备用 URL
curl -s "备用URL"
```

### 如果解析失败

```bash
# 保存 HTML 到文件，检查结构
curl -s "URL" > /tmp/debug.html

# 调整解析 pattern
```

## 示例对话

**用户**: "看看今天有什么热点新闻"

**AI 处理**:
1. 尝试 WebSearch → 发现配额已满
2. 切换到 web-fetcher
3. 执行: `curl + Python` 抓取搜狐/网易首页
4. 解析并整理热点列表
5. 输出格式化的新闻热点

---

## 总结

当遇到联网限制时，不要放弃！

| 限制方案 | 替代方案 |
|---------|---------|
| WebSearch | curl + 新闻网站解析 |
| webReader | curl + Python/HTML解析 |
| MCP 工具 | 原生 Bash + curl |

这个 skill 让你永不掉线！
