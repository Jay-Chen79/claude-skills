#!/usr/bin/env python3
"""
PubMed 检索脚本
用于科研头脑风暴 skill 的实时查重功能
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Optional


class PubMedSearcher:
    """PubMed E-utilities 检索器"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: Optional[str] = None):
        if api_key:
            self.api_key = api_key
        else:
            # 尝试从 config 导入，失败则从环境变量读取
            try:
                from config import PUBMED_API_KEY
                self.api_key = PUBMED_API_KEY
            except ImportError:
                self.api_key = os.environ.get("PUBMED_API_KEY", "6e303ed20473be7df617f33487f494ec4708")
    
    def search(self, query: str, max_results: int = 20) -> dict:
        """
        执行检索并返回结果
        
        Args:
            query: 检索式
            max_results: 最大返回数量
            
        Returns:
            包含检索结果的字典
        """
        # Step 1: ESearch 获取 ID 列表
        search_results = self._esearch(query, max_results)
        
        if search_results["count"] == 0:
            return {
                "query": query,
                "count": 0,
                "articles": [],
                "year_distribution": {},
                "study_types": {},
                "novelty_signal": "🟢",
                "novelty_reason": "未找到匹配文献"
            }
        
        # Step 2: EFetch 获取详细信息
        articles = self._efetch(search_results["ids"])
        
        # Step 3: 分析结果
        analysis = self._analyze_results(articles, search_results["count"])
        
        return {
            "query": query,
            "count": search_results["count"],
            "articles": articles[:10],  # 只返回前10篇
            "year_distribution": analysis["year_distribution"],
            "study_types": analysis["study_types"],
            "novelty_signal": analysis["novelty_signal"],
            "novelty_reason": analysis["novelty_reason"],
            "has_recent": analysis["has_recent"],
            "has_meta": analysis["has_meta"]
        }
    
    def _esearch(self, query: str, max_results: int) -> dict:
        """执行 ESearch"""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance"
        }
        if self.api_key:
            params["api_key"] = self.api_key
        
        url = f"{self.BASE_URL}/esearch.fcgi?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode())
                result = data.get("esearchresult", {})
                return {
                    "count": int(result.get("count", 0)),
                    "ids": result.get("idlist", [])
                }
        except Exception as e:
            print(f"ESearch 错误: {e}", file=sys.stderr)
            return {"count": 0, "ids": []}
    
    def _efetch(self, ids: list) -> list:
        """执行 EFetch 获取文章详情"""
        if not ids:
            return []
        
        params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml",
            "rettype": "abstract"
        }
        if self.api_key:
            params["api_key"] = self.api_key
        
        url = f"{self.BASE_URL}/efetch.fcgi?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                xml_data = response.read().decode()
                return self._parse_xml(xml_data)
        except Exception as e:
            print(f"EFetch 错误: {e}", file=sys.stderr)
            return []
    
    def _parse_xml(self, xml_data: str) -> list:
        """简单解析 XML 提取文章信息"""
        import re
        
        articles = []
        
        # 提取每篇文章
        article_pattern = r'<PubmedArticle>(.*?)</PubmedArticle>'
        for match in re.finditer(article_pattern, xml_data, re.DOTALL):
            article_xml = match.group(1)
            
            # 提取 PMID
            pmid_match = re.search(r'<PMID[^>]*>(\d+)</PMID>', article_xml)
            pmid = pmid_match.group(1) if pmid_match else ""
            
            # 提取标题
            title_match = re.search(r'<ArticleTitle>(.*?)</ArticleTitle>', article_xml, re.DOTALL)
            title = self._clean_text(title_match.group(1)) if title_match else ""
            
            # 提取年份
            year_match = re.search(r'<PubDate>.*?<Year>(\d{4})</Year>', article_xml, re.DOTALL)
            if not year_match:
                year_match = re.search(r'<DateCompleted>.*?<Year>(\d{4})</Year>', article_xml, re.DOTALL)
            year = int(year_match.group(1)) if year_match else None
            
            # 提取摘要
            abstract_match = re.search(r'<Abstract>(.*?)</Abstract>', article_xml, re.DOTALL)
            if abstract_match:
                abstract_text = re.sub(r'<[^>]+>', ' ', abstract_match.group(1))
                abstract = self._clean_text(abstract_text)[:500]  # 截取前500字符
            else:
                abstract = ""
            
            # 提取作者
            authors = []
            author_pattern = r'<Author[^>]*>.*?<LastName>(.*?)</LastName>.*?<ForeName>(.*?)</ForeName>.*?</Author>'
            for author_match in re.finditer(author_pattern, article_xml, re.DOTALL):
                authors.append(f"{author_match.group(1)} {author_match.group(2)}")
            
            # 提取出版类型
            pub_types = []
            pub_type_pattern = r'<PublicationType[^>]*>(.*?)</PublicationType>'
            for pt_match in re.finditer(pub_type_pattern, article_xml):
                pub_types.append(self._clean_text(pt_match.group(1)))
            
            articles.append({
                "pmid": pmid,
                "title": title,
                "year": year,
                "authors": authors[:3],  # 只取前3个作者
                "abstract": abstract,
                "pub_types": pub_types
            })
        
        return articles
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        import re
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def _analyze_results(self, articles: list, total_count: int) -> dict:
        """分析检索结果，判断新颖性"""
        current_year = datetime.now().year
        
        # 年份分布
        year_distribution = {}
        for article in articles:
            if article["year"]:
                year_distribution[article["year"]] = year_distribution.get(article["year"], 0) + 1
        
        # 研究类型分布
        study_types = {}
        for article in articles:
            for pt in article["pub_types"]:
                study_types[pt] = study_types.get(pt, 0) + 1
        
        # 判断是否有近期文献（近2年）
        has_recent = any(
            article["year"] and article["year"] >= current_year - 2 
            for article in articles
        )
        
        # 判断是否有 Meta 分析或系统综述
        meta_keywords = ["meta-analysis", "systematic review", "meta analysis"]
        has_meta = any(
            any(kw in pt.lower() for kw in meta_keywords)
            for article in articles
            for pt in article["pub_types"]
        )
        
        # 判断新颖性信号
        if total_count > 10 and has_recent and has_meta:
            novelty_signal = "🔴"
            novelty_reason = f"高度饱和：{total_count}篇匹配，近期有发表，已有Meta分析"
        elif total_count > 10 and has_recent:
            novelty_signal = "🔴"
            novelty_reason = f"较为饱和：{total_count}篇匹配，近期仍有发表"
        elif 1 <= total_count <= 10:
            if has_recent:
                novelty_signal = "🟡"
                novelty_reason = f"部分覆盖：{total_count}篇匹配，有差异化空间"
            else:
                novelty_signal = "🟡"
                novelty_reason = f"部分覆盖：{total_count}篇匹配，但文献较老，可能有更新机会"
        else:
            novelty_signal = "🟢"
            novelty_reason = "相对空白：匹配文献很少，需验证生物学合理性"
        
        return {
            "year_distribution": year_distribution,
            "study_types": study_types,
            "has_recent": has_recent,
            "has_meta": has_meta,
            "novelty_signal": novelty_signal,
            "novelty_reason": novelty_reason
        }


def generate_search_query(concepts: list, operator: str = "AND") -> str:
    """
    根据概念列表生成检索式
    
    Args:
        concepts: 概念列表，每个概念可以是字符串或同义词列表
        operator: 概念间的逻辑运算符
        
    Returns:
        检索式字符串
    """
    terms = []
    for concept in concepts:
        if isinstance(concept, list):
            # 同义词用 OR 连接
            term = "(" + " OR ".join(concept) + ")"
        else:
            term = concept
        terms.append(term)
    
    return f" {operator} ".join(terms)


def main():
    parser = argparse.ArgumentParser(description="PubMed 检索工具")
    parser.add_argument("--query", "-q", required=True, help="检索式")
    parser.add_argument("--api_key", "-k", help="PubMed API Key")
    parser.add_argument("--max_results", "-n", type=int, default=20, help="最大返回数量")
    parser.add_argument("--output", "-o", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    searcher = PubMedSearcher(api_key=args.api_key)
    results = searcher.search(args.query, args.max_results)
    
    if args.output == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"检索式: {results['query']}")
        print(f"匹配数量: {results['count']}")
        print(f"新颖性信号: {results['novelty_signal']}")
        print(f"判断理由: {results['novelty_reason']}")
        print(f"{'='*60}\n")
        
        if results["articles"]:
            print("相关文献:\n")
            for i, article in enumerate(results["articles"], 1):
                authors_str = ", ".join(article["authors"]) if article["authors"] else "Unknown"
                print(f"{i}. [{article['year'] or 'N/A'}] {article['title']}")
                print(f"   作者: {authors_str}")
                print(f"   PMID: {article['pmid']}")
                if article["abstract"]:
                    print(f"   摘要: {article['abstract'][:200]}...")
                print()
        
        if results["year_distribution"]:
            print("年份分布:", dict(sorted(results["year_distribution"].items())))
        
        if results["study_types"]:
            print("研究类型:", results["study_types"])


if __name__ == "__main__":
    main()
