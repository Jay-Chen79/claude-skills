#!/usr/bin/env python3
"""
PubMed E-utilities API 检索引擎
支持大规模文献检索、摘要提取、MeSH 分析
"""

import urllib.request
import urllib.parse
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional

class PubMedSearcher:
    """PubMed 文献检索器"""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    API_KEY = ""  # 可选: 添加你的 NCBI API key 提高配额
    EMAIL = ""  # NCBI 要求提供 email
    TOOL = "Medical_Research_AI"

    def __init__(self, api_key: str = "", email: str = ""):
        self.api_key = api_key or self.API_KEY
        self.email = email or self.EMAIL
        self.retmax = 500  # 每次返回最大数量
        self.tool = self.TOOL

    def _build_url(self, endpoint: str, params: Dict) -> str:
        """构建请求 URL"""
        params.update({
            "tool": self.tool,
            "email": self.email,
        })
        if self.api_key:
            params["api_key"] = self.api_key

        query_string = urllib.parse.urlencode(params)
        return f"{self.BASE_URL}{endpoint}?{query_string}"

    def _make_request(self, url: str) -> str:
        """发起 HTTP 请求"""
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; MedicalResearchAI/1.0)"
            }
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8")

    def search(self, query: str, max_results: int = 1000,
               days_ago: int = None) -> List[str]:
        """
        检索文献，返回 PMIDs

        Args:
            query: 检索式（支持 MeSH 词和关键词）
            max_results: 最大返回数量
            days_ago: 限制最近 N 天的文献

        Returns:
            PMID 列表
        """
        # 构建检索式
        search_query = query
        if days_ago:
            today = datetime.now().strftime('%Y/%m/%d')
            date_limit = f"({today}[Date Entry]:{days_ago})"
            search_query = f"{query} AND {date_limit}"

        params = {
            "db": "pubmed",
            "term": search_query,
            "retmax": str(max_results),
            "retmode": "json",
            "sort": "relevance",
        }

        url = self._build_url("esearch.fcgi", params)
        response_data = json.loads(self._make_request(url))

        pmids = response_data.get("esearchresult", {}).get("idlist", [])

        if len(pmids) >= max_results:
            print(f"⚠️  检索结果超过 {max_results} 篇，可能需要更精确的检索式")

        return pmids

    def fetch_summaries(self, pmids: List[str]) -> List[Dict]:
        """
        批量获取文献摘要

        Args:
            pmids: PMID 列表（最多 200 个）

        Returns:
            文献摘要列表
        """
        if not pmids:
            return []

        # PubMed 每次最多处理 200 个 ID
        if len(pmids) > 200:
            results = []
            for i in range(0, len(pmids), 200):
                batch = pmids[i:i+200]
                results.extend(self.fetch_summaries(batch))
                time.sleep(0.34)  # NCBI 要求每秒最多 3 次请求
            return results

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
        }

        url = self._build_url("esummary.fcgi", params)
        response_data = json.loads(self._make_request(url))

        result = response_data.get("result", {})
        summaries = []

        for pmid in pmids:
            if pmid in result:
                article_data = result[pmid]
                summary = {
                    "pmid": pmid,
                    "title": article_data.get("title", ""),
                    "authors": [a.get("name", "") for a in article_data.get("authors", [])],
                    "journal": article_data.get("source", ""),
                    "pubdate": article_data.get("pubdate", ""),
                    "abstract": self._extract_abstract(article_data),
                    "mesh": article_data.get("mesh", []),
                    "publication_types": article_data.get("pubtype", []),
                    "doi": article_data.get("elocationid", "").replace("doi: ", ""),
                }
                summaries.append(summary)

        time.sleep(0.34)
        return summaries

    def _extract_abstract(self, article_data: Dict) -> str:
        """提取摘要文本"""
        abstract_data = article_data.get("abstract", "")
        if isinstance(abstract_data, str):
            return abstract_data

        if isinstance(abstract_data, dict):
            parts = abstract_data.get("AbstractText", [])
            if isinstance(parts, list):
                return " ".join(parts)
            return str(parts)

        return ""

    def analyze_publication_dates(self, summaries: List[Dict]) -> Dict:
        """分析发表时间趋势"""
        years = []
        for s in summaries:
            pubdate = s.get("pubdate", "")
            year_match = re.search(r"(\d{4})", pubdate)
            if year_match:
                years.append(int(year_match.group(1)))

        if not years:
            return {}

        year_counts = {}
        for year in years:
            year_counts[year] = year_counts.get(year, 0) + 1

        return {
            "total": len(summaries),
            "year_range": f"{min(years)}-{max(years)}",
            "year_distribution": dict(sorted(year_counts.items())),
            "recent_5_years": sum(1 for y in years if y >= datetime.now().year - 5),
        }

    def analyze_study_types(self, summaries: List[Dict]) -> Dict:
        """分析研究类型"""
        type_counts = {}

        for s in summaries:
            pubtypes = s.get("publication_types", [])
            for pt in pubtypes:
                type_counts[pt] = type_counts.get(pt, 0) + 1

        # 归类
        categories = {
            "RCT": 0,
            "队列研究": 0,
            "病例对照": 0,
            "横断面": 0,
            "病例系列": 0,
            "综述": 0,
            "Meta分析": 0,
            "其他": 0,
        }

        for pt, count in type_counts.items():
            pt_lower = pt.lower()
            if "randomized" in pt_lower or "clinical trial" in pt_lower:
                categories["RCT"] += count
            elif "cohort" in pt_lower:
                categories["队列研究"] += count
            elif "case-control" in pt_lower:
                categories["病例对照"] += count
            elif "cross-sectional" in pt_lower:
                categories["横断面"] += count
            elif "case series" in pt_lower:
                categories["病例系列"] += count
            elif "review" in pt_lower and "meta-analysis" not in pt_lower:
                categories["综述"] += count
            elif "meta-analysis" in pt_lower:
                categories["Meta分析"] += count
            else:
                categories["其他"] += count

        return categories

    def build_ophthalmology_query(self, keywords: List[str],
                                   mesh_terms: List[str] = None,
                                   study_type: str = None) -> str:
        """
        构建眼科专业检索式

        Args:
            keywords: 关键词列表
            mesh_terms: MeSH 词列表
            study_type: 研究类型限制

        Returns:
            PubMed 检索式
        """
        parts = []

        # 关键词检索
        if keywords:
            keyword_query = " OR ".join([f'"{kw}"[Title/Abstract]' for kw in keywords])
            parts.append(f"({keyword_query})")

        # MeSH 词检索
        if mesh_terms:
            mesh_query = " OR ".join([f'"{mesh}"[MeSH Terms]' for mesh in mesh_terms])
            parts.append(f"({mesh_query})")

        # 研究类型过滤
        if study_type:
            type_filters = {
                "RCT": "randomized controlled trial[pt]",
                "cohort": "cohort studies",
                "case-control": "case-control studies",
                "cross-sectional": "cross-sectional studies",
                "systematic review": "systematic review[pt]",
            }
            if study_type in type_filters:
                parts.append(f"AND {type_filters[study_type]}")

        # 结合各部分
        query = " AND ".join(parts)

        return query


def demo_usage():
    """使用示例"""

    searcher = PubMedSearcher()

    # 示例: 检索干眼症相关文献
    query = searcher.build_ophthalmology_query(
        keywords=["dry eye", "dry eye syndrome", "keratoconjunctivitis sicca"],
        mesh_terms=["Dry Eye Syndromes"]
    )

    print(f"检索式: {query}")

    # 执行检索
    pmids = searcher.search(query, max_results=100)
    print(f"找到 {len(pmids)} 篇文献")

    # 获取摘要
    summaries = searcher.fetch_summaries(pmids[:20])  # 先获取前 20 篇
    print(f"获取了 {len(summaries)} 篇摘要")

    # 分析
    pub_trend = searcher.analyze_publication_dates(summaries)
    study_types = searcher.analyze_study_types(summaries)

    print(f"\n发表时间分析:")
    print(json.dumps(pub_trend, indent=2, ensure_ascii=False))

    print(f"\n研究类型分析:")
    print(json.dumps(study_types, indent=2, ensure_ascii=False))

    # 显示第一篇
    if summaries:
        print(f"\n示例文献:")
        s = summaries[0]
        print(f"标题: {s['title']}")
        print(f"作者: {', '.join(s['authors'][:3])} 等")
        print(f"期刊: {s['journal']} ({s['pubdate']})")
        print(f"摘要: {s['abstract'][:200]}...")


if __name__ == "__main__":
    demo_usage()
