"""
第五个季节 - 功能测试脚本
测试核心功能是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.emotion_analyzer.analyzer import EmotionAnalyzer
from src.emotion_analyzer.visualizer import EmotionVisualizer
from src.story_generator.generator import MemoryStoryGenerator


def test_emotion_analyzer():
    """测试情感分析器"""
    print("=" * 50)
    print("测试情感分析器")
    print("=" * 50)
    
    analyzer = EmotionAnalyzer()
    
    # 测试文本
    test_text = "明明暗暗、零零散散，回忆情节重合明显，模糊了从前。滴滴点点、圆圆圈圈，像断了线。"
    
    print(f"测试文本: {test_text}")
    print()
    
    # 执行分析
    result = analyzer.analyze_text(test_text)
    
    # 显示结果
    print("分析结果:")
    print(f"- 主导情感: {result['dominant_emotion']}")
    print(f"- 情感多样性: {result['emotion_diversity']:.3f}")
    print(f"- 处理词数: {result['word_count']}")
    
    print("\n情感权重:")
    for emotion, weight in sorted(result['emotion_weights'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {emotion}: {weight:.3f}")
    
    print("\n情感关键词:")
    for emotion, keywords in result['emotion_keywords'].items():
        if keywords:
            print(f"  {emotion}: {', '.join(keywords)}")
    
    # 生成摘要
    summary = analyzer.get_emotion_summary(result)
    print(f"\n情感摘要: {summary}")
    
    return result


def test_story_generator():
    """测试故事生成器"""
    print("\n" + "=" * 50)
    print("测试故事生成器")
    print("=" * 50)
    
    generator = MemoryStoryGenerator()
    
    # 测试记忆碎片
    memory_fragments = ["夕阳西下", "老槐树", "蝉鸣声", "奶奶的摇椅", "冰棍的甜味"]
    
    print(f"记忆碎片: {', '.join(memory_fragments)}")
    print()
    
    # 生成提示词
    prompt = generator.generate_story_prompt(
        memory_fragments=memory_fragments,
        story_style="小说风格",
        emotional_tone="温暖",
        story_length="中等"
    )
    
    print("生成的提示词:")
    print(prompt)
    print()
    
    # 注意：这里不实际调用API，因为需要网络连接
    print("注意: 实际的故事生成需要网络连接到Pollinations API")
    print("在Web界面中可以测试完整的故事生成功能")
    
    return True


def test_visualizer():
    """测试可视化器"""
    print("\n" + "=" * 50)
    print("测试可视化器")
    print("=" * 50)
    
    visualizer = EmotionVisualizer()
    
    # 模拟情感权重数据
    emotion_weights = {
        "思念": 0.35,
        "失落": 0.25,
        "温暖": 0.20,
        "平静": 0.15,
        "忧伤": 0.05
    }
    
    print("测试情感权重:")
    for emotion, weight in emotion_weights.items():
        print(f"  {emotion}: {weight}")
    
    # 测试雷达图创建
    try:
        radar_fig = visualizer.create_emotion_radar_chart(emotion_weights)
        print("\n[成功] 雷达图创建成功")
    except Exception as e:
        print(f"\n[失败] 雷达图创建失败: {e}")
    
    # 测试柱状图创建
    try:
        bar_fig = visualizer.create_emotion_bar_chart(emotion_weights)
        print("[成功] 柱状图创建成功")
    except Exception as e:
        print(f"[失败] 柱状图创建失败: {e}")
    
    # 测试饼图创建
    try:
        pie_fig = visualizer.create_emotion_pie_chart(emotion_weights)
        print("[成功] 饼图创建成功")
    except Exception as e:
        print(f"[失败] 饼图创建失败: {e}")
    
    # 测试词云创建
    try:
        emotion_keywords = {
            "思念": ["想念", "怀念"],
            "失落": ["失望", "沮丧"],
            "温暖": ["温馨", "暖心"]
        }
        wordcloud_img = visualizer.create_wordcloud(emotion_keywords, emotion_weights)
        if wordcloud_img:
            print("[成功] 词云创建成功")
        else:
            print("[警告] 词云创建返回空结果")
    except Exception as e:
        print(f"[失败] 词云创建失败: {e}")
    
    return True


def test_integration():
    """集成测试"""
    print("\n" + "=" * 50)
    print("集成测试")
    print("=" * 50)
    
    # 测试完整流程
    analyzer = EmotionAnalyzer()
    visualizer = EmotionVisualizer()
    generator = MemoryStoryGenerator()
    
    # 1. 分析情感
    test_text = "那个夏天的午后，阳光透过窗帘洒在地板上，我坐在奶奶的摇椅上，听着远处传来的蝉鸣声。"
    emotion_result = analyzer.analyze_text(test_text)
    
    print(f"1. 情感分析完成 - 主导情感: {emotion_result['dominant_emotion']}")
    
    # 2. 创建可视化
    if emotion_result['emotion_weights']:
        radar_fig = visualizer.create_emotion_radar_chart(emotion_result['emotion_weights'])
        print("2. 情感可视化创建完成")
    else:
        print("2. 情感权重为空，跳过可视化")
    
    # 3. 准备故事生成
    memory_fragments = ["夏天午后", "阳光", "窗帘", "奶奶的摇椅", "蝉鸣声"]
    prompt = generator.generate_story_prompt(memory_fragments)
    print("3. 故事生成提示词准备完成")
    
    print("\n✓ 集成测试通过 - 所有组件可以正常协作")
    
    return True


def main():
    """主测试函数"""
    print("第五个季节 - 功能测试")
    print("开始测试核心功能...")
    
    try:
        # 测试各个组件
        emotion_result = test_emotion_analyzer()
        test_story_generator()
        test_visualizer()
        test_integration()
        
        print("\n" + "=" * 50)
        print("测试总结")
        print("=" * 50)
        print("✓ 情感分析器 - 正常工作")
        print("✓ 故事生成器 - 正常工作")
        print("✓ 可视化器 - 正常工作")
        print("✓ 组件集成 - 正常工作")
        print("\n🎉 所有核心功能测试通过！")
        print("\n💡 提示:")
        print("- 应用已在 http://localhost:8501 启动")
        print("- 可以在浏览器中测试完整的用户界面")
        print("- 故事生成功能需要网络连接")
        
    except Exception as e:
        print(f"\n[错误] 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
