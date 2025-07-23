"""
工具函数模块
提供各种辅助功能
"""

import re
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import streamlit as st


def clean_text(text: str) -> str:
    """
    清理文本内容
    
    Args:
        text: 输入文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    
    # 移除特殊字符（保留中文、英文、数字和基本标点）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s，。！？；：""''（）【】《》、]', '', text)
    
    return text


def format_timestamp(timestamp: float) -> str:
    """
    格式化时间戳
    
    Args:
        timestamp: Unix时间戳
        
    Returns:
        格式化的时间字符串
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def save_to_json(data: Any, filename: str) -> bool:
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
        
    Returns:
        是否保存成功
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False


def load_from_json(filename: str) -> Optional[Any]:
    """
    从JSON文件加载数据
    
    Args:
        filename: 文件名
        
    Returns:
        加载的数据或None
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载文件失败: {e}")
        return None


def split_text_into_fragments(text: str, separators: List[str] = None) -> List[str]:
    """
    将文本分割成碎片
    
    Args:
        text: 输入文本
        separators: 分隔符列表
        
    Returns:
        文本碎片列表
    """
    if not text:
        return []
    
    if separators is None:
        separators = [',', '，', '\n', ';', '；', '、']
    
    # 使用正则表达式分割
    pattern = '|'.join(re.escape(sep) for sep in separators)
    fragments = re.split(pattern, text)
    
    # 清理和过滤
    fragments = [fragment.strip() for fragment in fragments if fragment.strip()]
    
    return fragments


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本的相似度（简单的Jaccard相似度）
    
    Args:
        text1: 文本1
        text2: 文本2
        
    Returns:
        相似度分数 (0-1)
    """
    if not text1 or not text2:
        return 0.0
    
    # 转换为字符集合
    set1 = set(text1.lower())
    set2 = set(text2.lower())
    
    # 计算Jaccard相似度
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 输入文本
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        截断后的文本
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def validate_memory_fragments(fragments: List[str]) -> Dict[str, Any]:
    """
    验证记忆碎片的有效性
    
    Args:
        fragments: 记忆碎片列表
        
    Returns:
        验证结果
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'cleaned_fragments': []
    }
    
    if not fragments:
        result['valid'] = False
        result['errors'].append("记忆碎片列表为空")
        return result
    
    cleaned_fragments = []
    
    for i, fragment in enumerate(fragments):
        # 清理碎片
        cleaned = clean_text(fragment)
        
        if not cleaned:
            result['warnings'].append(f"第{i+1}个碎片为空或无效")
            continue
        
        if len(cleaned) < 2:
            result['warnings'].append(f"第{i+1}个碎片过短: '{cleaned}'")
            continue
        
        if len(cleaned) > 50:
            result['warnings'].append(f"第{i+1}个碎片过长，建议缩短: '{truncate_text(cleaned, 30)}'")
        
        cleaned_fragments.append(cleaned)
    
    result['cleaned_fragments'] = cleaned_fragments
    
    if not cleaned_fragments:
        result['valid'] = False
        result['errors'].append("没有有效的记忆碎片")
    
    return result


def create_download_link(content: str, filename: str, link_text: str = "下载") -> str:
    """
    创建下载链接
    
    Args:
        content: 文件内容
        filename: 文件名
        link_text: 链接文本
        
    Returns:
        HTML下载链接
    """
    import base64
    
    # 编码内容
    b64_content = base64.b64encode(content.encode('utf-8')).decode()
    
    # 创建下载链接
    href = f'<a href="data:text/plain;base64,{b64_content}" download="{filename}">{link_text}</a>'
    
    return href


def display_progress_bar(current: int, total: int, text: str = "处理中..."):
    """
    显示进度条
    
    Args:
        current: 当前进度
        total: 总数
        text: 显示文本
    """
    if total > 0:
        progress = current / total
        st.progress(progress, text=f"{text} ({current}/{total})")


def format_emotion_weights_table(emotion_weights: Dict[str, float]) -> str:
    """
    格式化情感权重为表格
    
    Args:
        emotion_weights: 情感权重字典
        
    Returns:
        格式化的表格字符串
    """
    if not emotion_weights:
        return "无情感数据"
    
    # 排序
    sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)
    
    # 创建表格
    table_lines = ["| 情感类型 | 权重 | 百分比 |", "|---------|------|--------|"]
    
    for emotion, weight in sorted_emotions:
        percentage = f"{weight * 100:.1f}%"
        table_lines.append(f"| {emotion} | {weight:.3f} | {percentage} |")
    
    return "\n".join(table_lines)


def get_color_by_emotion(emotion: str) -> str:
    """
    根据情感获取对应颜色
    
    Args:
        emotion: 情感名称
        
    Returns:
        颜色代码
    """
    from config.settings import EMOTION_COLORS
    return EMOTION_COLORS.get(emotion, "#888888")


def create_emotion_badge(emotion: str, weight: float) -> str:
    """
    创建情感徽章HTML
    
    Args:
        emotion: 情感名称
        weight: 权重
        
    Returns:
        HTML徽章代码
    """
    color = get_color_by_emotion(emotion)
    percentage = f"{weight * 100:.1f}%"
    
    return f"""
    <span style="
        background-color: {color};
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        margin: 2px;
        display: inline-block;
    ">
        {emotion} ({percentage})
    </span>
    """


def export_analysis_report(analysis_data: Dict[str, Any], format_type: str = "markdown") -> str:
    """
    导出分析报告
    
    Args:
        analysis_data: 分析数据
        format_type: 导出格式 (markdown, txt, json)
        
    Returns:
        格式化的报告内容
    """
    if format_type == "json":
        return json.dumps(analysis_data, ensure_ascii=False, indent=2)
    
    elif format_type == "markdown":
        report_lines = [
            "# 第五个季节 - 分析报告",
            f"\n**生成时间**: {format_timestamp(time.time())}",
            "\n## 情感分析结果\n"
        ]
        
        if 'emotion_weights' in analysis_data:
            report_lines.append(format_emotion_weights_table(analysis_data['emotion_weights']))
        
        if 'dominant_emotion' in analysis_data:
            report_lines.append(f"\n**主导情感**: {analysis_data['dominant_emotion']}")
        
        if 'emotion_diversity' in analysis_data:
            diversity = analysis_data['emotion_diversity']
            report_lines.append(f"**情感多样性**: {diversity:.3f}")
        
        return "\n".join(report_lines)
    
    else:  # txt format
        report_lines = [
            "第五个季节 - 分析报告",
            "=" * 30,
            f"生成时间: {format_timestamp(time.time())}",
            "\n情感分析结果:",
            "-" * 20
        ]
        
        if 'emotion_weights' in analysis_data:
            emotion_weights = analysis_data['emotion_weights']
            sorted_emotions = sorted(emotion_weights.items(), key=lambda x: x[1], reverse=True)
            
            for emotion, weight in sorted_emotions:
                percentage = f"{weight * 100:.1f}%"
                report_lines.append(f"{emotion}: {weight:.3f} ({percentage})")
        
        return "\n".join(report_lines)
