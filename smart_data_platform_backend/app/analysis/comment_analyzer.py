import re
from collections import Counter
from typing import List, Dict


class CommentAnalyzer:
    """
    评论分析类
    用于分析用户差评并生成词云
    """

    def __init__(self, comments: List[str]):
        self.comments = comments

    def _clean_text(self, text: str) -> str:
        """
        清洗评论文本
        """
        text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9 ]+", "", text)
        text = re.sub(r" +", " ", text)
        return text.strip()

    def negative_wordcloud(self, top_n: int = 30) -> List[Dict]:
        """
        生成差评词云
        """
        negative_keywords = [
            "坏", "瑕疵", "掉漆", "发烫", "卡顿",
            "退", "黄屏", "绿屏", "问题", "故障"
        ]

        negative_comments = [
            c for c in self.comments
            if any(k in c for k in negative_keywords)
        ]

        words = " ".join(
            [self._clean_text(c) for c in negative_comments]
        ).split()

        counter = Counter(words)

        return [
            {"name": w, "value": v}
            for w, v in counter.most_common(top_n)
        ]