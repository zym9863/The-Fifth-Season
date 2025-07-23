"""
测试Pollinations API连接
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.story_generator.generator import MemoryStoryGenerator


def test_api_connection():
    """测试API连接"""
    print("测试Pollinations API连接...")
    
    generator = MemoryStoryGenerator()
    
    # 简单的测试提示
    test_prompt = "请写一个关于春天的短句。"
    
    try:
        result = generator.call_pollinations_api(test_prompt)
        
        if result:
            print("✓ API连接成功！")
            print(f"返回结果: {result[:100]}...")
            return True
        else:
            print("✗ API连接失败 - 返回空结果")
            return False
            
    except Exception as e:
        print(f"✗ API连接失败: {e}")
        return False


def test_story_generation():
    """测试完整故事生成"""
    print("\n测试完整故事生成...")
    
    generator = MemoryStoryGenerator()
    
    memory_fragments = ["春天", "樱花", "微风"]
    
    try:
        result = generator.generate_story(
            memory_fragments=memory_fragments,
            story_style="诗意散文",
            emotional_tone="温暖",
            story_length="短"
        )
        
        if result['success']:
            print("✓ 故事生成成功！")
            print(f"故事内容: {result['story'][:200]}...")
            return True
        else:
            print(f"✗ 故事生成失败: {result['error']}")
            return False
            
    except Exception as e:
        print(f"✗ 故事生成失败: {e}")
        return False


if __name__ == "__main__":
    print("第五个季节 - API连接测试")
    print("=" * 40)
    
    # 测试基础API连接
    api_ok = test_api_connection()
    
    if api_ok:
        # 测试完整故事生成
        story_ok = test_story_generation()
        
        if story_ok:
            print("\n🎉 所有API测试通过！")
            print("💡 现在可以在Web界面中使用完整的故事生成功能了")
        else:
            print("\n⚠️ 故事生成测试失败，但基础API连接正常")
    else:
        print("\n❌ API连接测试失败")
        print("💡 请检查网络连接，或稍后重试")
        print("💡 即使API不可用，情感分析功能仍然可以正常使用")
