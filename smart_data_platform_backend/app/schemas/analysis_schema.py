from pydantic import BaseModel
from typing import List, Dict


class ScatterPoint(BaseModel):
    price: float
    comment: int
    shop: str


class WordCloudItem(BaseModel):
    name: str
    value: int


class TagItem(BaseModel):
    name: str
    value: int


class ProductStats(BaseModel):
    scatter_points: List[ScatterPoint]
    price_distribution: Dict[str, int]
    shop_distribution: Dict[str, int]


class CommentAnalysis(BaseModel):
    negative_wordcloud: List[WordCloudItem]


class TagAnalysis(BaseModel):
    tags: List[TagItem]


class AnalysisData(BaseModel):
    product: ProductStats
    comments: CommentAnalysis
    tags: TagAnalysis