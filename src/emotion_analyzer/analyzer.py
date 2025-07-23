"""
情感光谱分析器核心模块
实现文本的多维情感分析功能
"""

import re
import jieba
import numpy as np
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
from textblob import TextBlob

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import EMOTION_CATEGORIES, CHINESE_STOPWORDS


class EmotionAnalyzer:
    """情感光谱分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.emotion_keywords = EMOTION_CATEGORIES
        self.stopwords = set(CHINESE_STOPWORDS)
        self._build_emotion_dict()
    
    def _build_emotion_dict(self):
        """构建情感词典"""
        self.emotion_dict = {}
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                self.emotion_dict[keyword] = emotion
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        文本预处理
        
        Args:
            text: 输入文本
            
        Returns:
            处理后的词语列表
        """
        # 清理文本
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
        
        # 中文分词
        words = list(jieba.cut(text))
        
        # 过滤停用词和短词
        filtered_words = [
            word.strip() for word in words 
            if word.strip() and len(word.strip()) > 1 and word.strip() not in self.stopwords
        ]
        
        return filtered_words
    
    def calculate_emotion_weights(self, words: List[str]) -> Dict[str, float]:
        """
        计算情感权重
        
        Args:
            words: 词语列表
            
        Returns:
            情感权重字典
        """
        emotion_scores = defaultdict(float)
        word_count = len(words)
        
        if word_count == 0:
            return dict(emotion_scores)
        
        # 直接匹配情感关键词
        direct_matches = 0
        for word in words:
            if word in self.emotion_dict:
                emotion = self.emotion_dict[word]
                emotion_scores[emotion] += 1.5  # 直接匹配权重更高
                direct_matches += 1
        
        # 增强模糊匹配 - 检查是否包含情感关键词
        fuzzy_matches = 0
        for word in words:
            for emotion, keywords in self.emotion_keywords.items():
                for keyword in keywords:
                    # 更精确的模糊匹配
                    if len(keyword) >= 2:  # 只对长度>=2的关键词进行模糊匹配
                        if keyword in word and len(word) <= len(keyword) + 2:
                            emotion_scores[emotion] += 0.8
                            fuzzy_matches += 1
                        elif word in keyword and len(keyword) <= len(word) + 2:
                            emotion_scores[emotion] += 0.6
                            fuzzy_matches += 1
        
        # 语义匹配 - 基于词汇的语义相关性
        semantic_matches = self._semantic_emotion_analysis(words)
        for emotion, score in semantic_matches.items():
            emotion_scores[emotion] += score
        
        # 使用TextBlob进行情感极性分析作为补充（仅在其他匹配较少时使用）
        text = ' '.join(words)
        total_matches = direct_matches + fuzzy_matches + sum(semantic_matches.values())
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # 只有在匹配较少且文本有情感倾向时才使用TextBlob结果
            if total_matches < 2 and subjectivity > 0.3:
                if polarity > 0.2:
                    emotion_scores['喜悦'] += polarity * 1.5
                    emotion_scores['温暖'] += polarity * 1.0
                elif polarity < -0.2:
                    emotion_scores['忧伤'] += abs(polarity) * 1.5
                    emotion_scores['失落'] += abs(polarity) * 1.0
                elif abs(polarity) <= 0.1 and subjectivity > 0.5:
                    # 主观但中性的文本可能包含复杂情感
                    emotion_scores['思念'] += 0.3
                    emotion_scores['平静'] += 0.2
            
            # 避免完全没有情感的情况
            if sum(emotion_scores.values()) == 0:
                if subjectivity > 0.3:
                    emotion_scores['平静'] += 0.3
                else:
                    emotion_scores['平静'] += 0.1
        except:
            # TextBlob分析失败时的处理
            if sum(emotion_scores.values()) == 0:
                emotion_scores['平静'] += 0.1
        
        # 改进的归一化权重 - 保持情感多样性
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            # 对权重进行平滑处理，避免单一情感权重过高
            smoothed_scores = {}
            for emotion, score in emotion_scores.items():
                if score > 0:
                    # 使用平方根来平滑高权重
                    smoothed_scores[emotion] = np.sqrt(score)
            
            # 重新计算总分并归一化
            smoothed_total = sum(smoothed_scores.values())
            if smoothed_total > 0:
                emotion_scores = {
                    emotion: score / smoothed_total 
                    for emotion, score in smoothed_scores.items()
                }
        
        return dict(emotion_scores)
    
    def _semantic_emotion_analysis(self, words: List[str]) -> Dict[str, float]:
        """
        基于语义的情感分析
        
        Args:
            words: 词语列表
            
        Returns:
            语义情感权重字典
        """
        semantic_scores = defaultdict(float)
        
        # 定义语义规则
        semantic_rules = {
            '思念': ['过去', '从前', '以前', '当年', '那时', '曾经', '记得', '还记得'],
            '失落': ['不再', '失去', '没有了', '结束', '完了', '破碎', '散了'],
            '期待': ['未来', '明天', '将来', '希冀', '但愿', '如果', '要是'],
            '无助': ['不知道', '怎么办', '不懂', '不会', '不能', '无法'],
            '温暖': ['家', '妈妈', '爸爸', '朋友', '陪伴', '一起', '拥抱'],
            '忧伤': ['眼泪', '哭', '痛', '伤', '苦', '难受', '心碎'],
            '喜悦': ['笑', '哈哈', '开心', '棒', '好', '赞', '太好了'],
            '平静': ['静', '安', '稳', '缓', '慢', '轻', '淡']
        }
        
        # 检查语义规则匹配
        for word in words:
            for emotion, semantic_words in semantic_rules.items():
                for semantic_word in semantic_words:
                    if semantic_word in word or word in semantic_word:
                        semantic_scores[emotion] += 0.4
        
        return dict(semantic_scores)
    
    def extract_emotion_keywords(self, words: List[str]) -> Dict[str, List[str]]:
        """
        提取情感关键词
        
        Args:
            words: 词语列表
            
        Returns:
            按情感分类的关键词字典
        """
        emotion_keywords = defaultdict(list)
        
        for word in words:
            # 直接匹配
            if word in self.emotion_dict:
                emotion = self.emotion_dict[word]
                emotion_keywords[emotion].append(word)
            
            # 模糊匹配
            for emotion, keywords in self.emotion_keywords.items():
                for keyword in keywords:
                    if keyword in word or word in keyword:
                        if word not in emotion_keywords[emotion]:
                            emotion_keywords[emotion].append(word)
        
        return dict(emotion_keywords)
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        分析文本情感
        
        Args:
            text: 输入文本
            
        Returns:
            分析结果字典
        """
        if not text or not text.strip():
            return {
                'emotion_weights': {},
                'emotion_keywords': {},
                'dominant_emotion': None,
                'emotion_diversity': 0.0,
                'processed_words': [],
                'word_count': 0
            }
        
        # 预处理文本
        words = self.preprocess_text(text)
        
        # 计算情感权重
        emotion_weights = self.calculate_emotion_weights(words)
        
        # 提取情感关键词
        emotion_keywords = self.extract_emotion_keywords(words)
        
        # 找出主导情感
        dominant_emotion = max(emotion_weights.items(), key=lambda x: x[1])[0] if emotion_weights else None
        
        # 计算情感多样性（熵）
        emotion_diversity = self._calculate_emotion_diversity(emotion_weights)
        
        return {
            'emotion_weights': emotion_weights,
            'emotion_keywords': emotion_keywords,
            'dominant_emotion': dominant_emotion,
            'emotion_diversity': emotion_diversity,
            'processed_words': words,
            'word_count': len(words)
        }
    
    def _calculate_emotion_diversity(self, emotion_weights: Dict[str, float]) -> float:
        """
        计算情感多样性（使用香农熵）
        
        Args:
            emotion_weights: 情感权重字典
            
        Returns:
            情感多样性分数
        """
        if not emotion_weights:
            return 0.0
        
        weights = list(emotion_weights.values())
        weights = [w for w in weights if w > 0]
        
        if len(weights) <= 1:
            return 0.0
        
        # 计算香农熵
        entropy = -sum(w * np.log2(w) for w in weights if w > 0)
        
        # 归一化到0-1范围
        max_entropy = np.log2(len(weights))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return normalized_entropy
    
    def get_emotion_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        生成情感分析摘要
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            情感摘要文本
        """
        emotion_weights = analysis_result['emotion_weights']
        dominant_emotion = analysis_result['dominant_emotion']
        emotion_diversity = analysis_result['emotion_diversity']
        
        if not emotion_weights:
            return "未检测到明显的情感倾向。"
        
        # 排序情感权重
        sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)
        top_emotions = sorted_emotions[:3]
        
        summary_parts = []
        
        # 主导情感
        if dominant_emotion:
            dominant_weight = emotion_weights[dominant_emotion]
            summary_parts.append(f"主导情感是**{dominant_emotion}**（权重: {dominant_weight:.2f}）")
        
        # 次要情感
        if len(top_emotions) > 1:
            secondary_emotions = [f"{emotion}({weight:.2f})" for emotion, weight in top_emotions[1:]]
            summary_parts.append(f"次要情感包括: {', '.join(secondary_emotions)}")
        
        # 情感复杂度
        if emotion_diversity > 0.7:
            summary_parts.append("情感状态较为复杂多样")
        elif emotion_diversity > 0.4:
            summary_parts.append("情感状态中等复杂")
        else:
            summary_parts.append("情感状态相对单一")
        
        return "；".join(summary_parts) + "。"
