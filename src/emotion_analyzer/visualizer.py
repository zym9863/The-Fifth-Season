"""
情感光谱可视化模块
创建情感分析结果的可视化图表
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import io
import base64

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import EMOTION_COLORS, WORDCLOUD_CONFIG


class EmotionVisualizer:
    """情感可视化器"""
    
    def __init__(self):
        """初始化可视化器"""
        self.emotion_colors = EMOTION_COLORS
        self.wordcloud_config = WORDCLOUD_CONFIG
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def create_emotion_radar_chart(self, emotion_weights: Dict[str, float]) -> go.Figure:
        """
        创建情感雷达图
        
        Args:
            emotion_weights: 情感权重字典
            
        Returns:
            Plotly图表对象
        """
        if not emotion_weights:
            # 创建空图表
            fig = go.Figure()
            fig.add_annotation(
                text="暂无情感数据",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16)
            )
            fig.update_layout(
                title="情感光谱雷达图",
                showlegend=False,
                height=400
            )
            return fig
        
        # 准备数据
        emotions = list(emotion_weights.keys())
        values = list(emotion_weights.values())
        colors = [self.emotion_colors.get(emotion, '#888888') for emotion in emotions]
        
        # 创建雷达图
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=emotions,
            fill='toself',
            fillcolor='rgba(135, 206, 235, 0.3)',
            line=dict(color='rgb(135, 206, 235)', width=2),
            marker=dict(size=8, color=colors),
            name='情感强度'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.1] if values else [0, 1],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            title=dict(
                text="情感光谱雷达图",
                x=0.5,
                font=dict(size=16)
            ),
            showlegend=False,
            height=400,
            margin=dict(t=60, b=40, l=40, r=40)
        )
        
        return fig
    
    def create_emotion_bar_chart(self, emotion_weights: Dict[str, float]) -> go.Figure:
        """
        创建情感柱状图
        
        Args:
            emotion_weights: 情感权重字典
            
        Returns:
            Plotly图表对象
        """
        if not emotion_weights:
            # 创建空图表
            fig = go.Figure()
            fig.add_annotation(
                text="暂无情感数据",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16)
            )
            fig.update_layout(
                title="情感强度分布",
                showlegend=False,
                height=400
            )
            return fig
        
        # 排序情感权重
        sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)
        emotions = [item[0] for item in sorted_emotions]
        values = [item[1] for item in sorted_emotions]
        colors = [self.emotion_colors.get(emotion, '#888888') for emotion in emotions]
        
        # 创建柱状图
        fig = go.Figure(data=[
            go.Bar(
                x=emotions,
                y=values,
                marker_color=colors,
                text=[f'{v:.3f}' for v in values],
                textposition='auto',
                textfont=dict(size=10)
            )
        ])
        
        fig.update_layout(
            title=dict(
                text="情感强度分布",
                x=0.5,
                font=dict(size=16)
            ),
            xaxis=dict(
                title="情感类型",
                tickangle=45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title="强度权重",
                tickfont=dict(size=10)
            ),
            height=400,
            margin=dict(t=60, b=100, l=60, r=40)
        )
        
        return fig
    
    def create_emotion_pie_chart(self, emotion_weights: Dict[str, float]) -> go.Figure:
        """
        创建情感饼图
        
        Args:
            emotion_weights: 情感权重字典
            
        Returns:
            Plotly图表对象
        """
        if not emotion_weights:
            # 创建空图表
            fig = go.Figure()
            fig.add_annotation(
                text="暂无情感数据",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16)
            )
            fig.update_layout(
                title="情感比例分布",
                showlegend=False,
                height=400
            )
            return fig
        
        # 过滤掉权重为0的情感
        filtered_emotions = {k: v for k, v in emotion_weights.items() if v > 0}
        
        if not filtered_emotions:
            return self.create_emotion_pie_chart({})
        
        emotions = list(filtered_emotions.keys())
        values = list(filtered_emotions.values())
        colors = [self.emotion_colors.get(emotion, '#888888') for emotion in emotions]
        
        # 创建饼图
        fig = go.Figure(data=[
            go.Pie(
                labels=emotions,
                values=values,
                marker_colors=colors,
                textinfo='label+percent',
                textfont=dict(size=10),
                hovertemplate='<b>%{label}</b><br>权重: %{value:.3f}<br>占比: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text="情感比例分布",
                x=0.5,
                font=dict(size=16)
            ),
            height=400,
            margin=dict(t=60, b=40, l=40, r=40)
        )
        
        return fig
    
    def create_wordcloud(self, emotion_keywords: Dict[str, List[str]], 
                        emotion_weights: Dict[str, float]) -> str:
        """
        创建情感词云
        
        Args:
            emotion_keywords: 情感关键词字典
            emotion_weights: 情感权重字典
            
        Returns:
            词云图片的base64编码字符串
        """
        if not emotion_keywords:
            return None
        
        # 准备词频数据
        word_freq = {}
        for emotion, keywords in emotion_keywords.items():
            emotion_weight = emotion_weights.get(emotion, 0.1)
            for keyword in keywords:
                # 词频 = 情感权重 * 基础频率
                word_freq[keyword] = word_freq.get(keyword, 0) + emotion_weight * 10
        
        if not word_freq:
            return None
        
        try:
            # 寻找合适的中文字体
            import platform
            font_path = None
            
            if platform.system() == "Windows":
                # Windows系统字体路径
                possible_fonts = [
                    "C:/Windows/Fonts/simhei.ttf",  # 黑体
                    "C:/Windows/Fonts/simsun.ttc",  # 宋体
                    "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
                    "C:/Windows/Fonts/simkai.ttf",  # 楷体
                ]
            elif platform.system() == "Linux":
                # Linux系统字体路径
                possible_fonts = [
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                ]
            else:  # macOS
                possible_fonts = [
                    "/System/Library/Fonts/PingFang.ttc",
                    "/System/Library/Fonts/Hiragino Sans GB.ttc",
                    "/Library/Fonts/Arial Unicode MS.ttf",
                ]
            
            # 查找可用字体
            for font in possible_fonts:
                if os.path.exists(font):
                    font_path = font
                    break
            
            # 创建词云
            wordcloud_config = {
                'width': self.wordcloud_config['width'],
                'height': self.wordcloud_config['height'],
                'background_color': self.wordcloud_config['background_color'],
                'max_words': self.wordcloud_config['max_words'],
                'colormap': self.wordcloud_config['colormap'],
                'relative_scaling': 0.5,
                'min_font_size': 12,
                'max_font_size': 100,
                'prefer_horizontal': 0.9,
                'scale': 1,
                'collocations': False,
            }
            
            # 如果找到字体，添加字体路径
            if font_path:
                wordcloud_config['font_path'] = font_path
            
            wordcloud = WordCloud(**wordcloud_config).generate_from_frequencies(word_freq)
            
            # 转换为base64
            img_buffer = io.BytesIO()
            wordcloud.to_image().save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            return img_base64
            
        except Exception as e:
            print(f"词云生成失败: {e}")
            # 尝试创建简单版本的词云
            try:
                # 简化配置，不使用字体
                simple_wordcloud = WordCloud(
                    width=800,
                    height=400,
                    background_color='white',
                    max_words=50,
                    relative_scaling=0.5,
                    min_font_size=12,
                    collocations=False
                ).generate_from_frequencies(word_freq)
                
                img_buffer = io.BytesIO()
                simple_wordcloud.to_image().save(img_buffer, format='PNG')
                img_buffer.seek(0)
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                
                return img_base64
            except Exception as e2:
                print(f"简化词云生成也失败: {e2}")
                return None
    
    def create_emotion_timeline(self, emotion_data_list: List[Dict[str, Any]]) -> go.Figure:
        """
        创建情感时间线图（用于多次分析的对比）
        
        Args:
            emotion_data_list: 情感数据列表
            
        Returns:
            Plotly图表对象
        """
        if not emotion_data_list:
            fig = go.Figure()
            fig.add_annotation(
                text="暂无时间线数据",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font=dict(size=16)
            )
            fig.update_layout(
                title="情感变化时间线",
                showlegend=False,
                height=400
            )
            return fig
        
        # 准备数据
        all_emotions = set()
        for data in emotion_data_list:
            all_emotions.update(data.get('emotion_weights', {}).keys())
        
        fig = go.Figure()
        
        for emotion in all_emotions:
            values = []
            timestamps = []
            for i, data in enumerate(emotion_data_list):
                values.append(data.get('emotion_weights', {}).get(emotion, 0))
                timestamps.append(f"分析 {i+1}")
            
            fig.add_trace(go.Scatter(
                x=timestamps,
                y=values,
                mode='lines+markers',
                name=emotion,
                line=dict(color=self.emotion_colors.get(emotion, '#888888'), width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title=dict(
                text="情感变化时间线",
                x=0.5,
                font=dict(size=16)
            ),
            xaxis=dict(title="时间点"),
            yaxis=dict(title="情感强度"),
            height=400,
            margin=dict(t=60, b=60, l=60, r=40)
        )
        
        return fig
