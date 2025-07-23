"""
简单的情感分析器测试脚本
用于验证修复效果
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.emotion_analyzer.analyzer import EmotionAnalyzer

def test_emotion_analysis():
    """测试情感分析器的修复效果"""
    print("=" * 60)
    print("情感分析器修复效果测试")
    print("=" * 60)
    
    analyzer = EmotionAnalyzer()
    
    # 测试用例
    test_cases = [
        {
            "text": "明明暗暗、零零散散，回忆情节重合明显，模糊了从前。滴滴点点、圆圆圈圈，像断了线。",
            "expected_emotions": ["思念", "失落"]
        },
        {
            "text": "今天阳光很好，心情特别开心，笑容满面地走在路上。",
            "expected_emotions": ["喜悦", "温暖"]
        },
        {
            "text": "一个人坐在房间里，感到很孤独，不知道该怎么办。",
            "expected_emotions": ["失落", "无助"]
        },
        {
            "text": "看着夕阳西下，想起了远方的家人，心中充满思念。",
            "expected_emotions": ["思念", "温暖"]
        },
        {
            "text": "明天就要考试了，好紧张，希望能够顺利通过。",
            "expected_emotions": ["期待", "无助"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"文本: {test_case['text']}")
        
        # 执行分析
        result = analyzer.analyze_text(test_case['text'])
        
        # 显示结果
        print(f"主导情感: {result['dominant_emotion']}")
        print(f"情感多样性: {result['emotion_diversity']:.3f}")
        
        print("情感权重分布:")
        sorted_emotions = sorted(result['emotion_weights'].items(), key=lambda x: x[1], reverse=True)
        for emotion, weight in sorted_emotions[:3]:  # 显示前3个情感
            print(f"  {emotion}: {weight:.3f}")
        
        # 生成摘要
        summary = analyzer.get_emotion_summary(result)
        print(f"情感摘要: {summary}")
        
        # 检查是否包含预期情感
        detected_emotions = [emotion for emotion, weight in result['emotion_weights'].items() if weight > 0.1]
        expected_found = any(emotion in detected_emotions for emotion in test_case['expected_emotions'])
        
        if expected_found:
            print("[成功] 检测到预期的情感类型")
        else:
            print(f"[注意] 未检测到预期情感 {test_case['expected_emotions']}")
            print(f"       实际检测到: {detected_emotions}")
        
        print("-" * 50)

def main():
    """主函数"""
    try:
        test_emotion_analysis()
        print("\n" + "=" * 60)
        print("测试完成")
        print("如果能看到多种不同的情感分析结果，说明修复成功！")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()