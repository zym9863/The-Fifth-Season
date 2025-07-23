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
        for word in words:
            if word in self.emotion_dict:
                emotion = self.emotion_dict[word]
                emotion_scores[emotion] += 1.0
        
        # 模糊匹配 - 检查是否包含情感关键词
        for word in words:
            for emotion, keywords in self.emotion_keywords.items():
                for keyword in keywords:
                    if keyword in word or word in keyword:
                        emotion_scores[emotion] += 0.5
        
        # 使用TextBlob进行情感极性分析作为补充
        text = ' '.join(words)
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                emotion_scores['喜悦'] += polarity * 2
                emotion_scores['温暖'] += polarity * 1.5
            elif polarity < -0.1:
                emotion_scores['忧伤'] += abs(polarity) * 2
                emotion_scores['失落'] += abs(polarity) * 1.5
            else:
                emotion_scores['平静'] += 1.0
        except:
            # 如果TextBlob分析失败，使用默认值
            emotion_scores['平静'] += 0.5
        
        # 归一化权重
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_scores = {
                emotion: score / total_score 
                for emotion, score in emotion_scores.items()
            }
        
        return dict(emotion_scores)
    
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
