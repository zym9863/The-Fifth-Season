"""
记忆碎片故事生成器核心模块
基于Pollinations API实现文本生成功能
"""

import requests
import urllib.parse
import json
import time
from typing import List, Dict, Any, Optional
import random

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import POLLINATIONS_API_URL, DEFAULT_MODEL, DEFAULT_SEED


class MemoryStoryGenerator:
    """记忆碎片故事生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.api_url = POLLINATIONS_API_URL
        self.default_model = DEFAULT_MODEL
        self.default_seed = DEFAULT_SEED
        
        # 故事模板
        self.story_templates = [
            "小说风格",
            "电影桥段",
            "诗意散文",
            "日记体",
            "回忆录",
            "梦境叙述"
        ]
        
        # 情感基调
        self.emotional_tones = {
            "温暖": "温馨感人",
            "忧伤": "淡淡忧伤",
            "思念": "深深思念",
            "期待": "充满希望",
            "失落": "略带失落",
            "平静": "宁静安详",
            "喜悦": "欢快愉悦",
            "无助": "迷茫困顿"
        }
    
    def generate_story_prompt(self, memory_fragments: List[str], 
                            story_style: str = "小说风格",
                            emotional_tone: str = "温暖",
                            story_length: str = "中等") -> str:
        """
        生成故事创作提示词
        
        Args:
            memory_fragments: 记忆碎片列表
            story_style: 故事风格
            emotional_tone: 情感基调
            story_length: 故事长度
            
        Returns:
            生成的提示词
        """
        if not memory_fragments:
            return ""
        
        # 构建基础提示词
        fragments_text = "、".join(memory_fragments)
        
        length_guide = {
            "短": "200-300字",
            "中等": "400-600字", 
            "长": "800-1000字"
        }
        
        length_desc = length_guide.get(story_length, "400-600字")
        tone_desc = self.emotional_tones.get(emotional_tone, "温馨感人")
        
        prompt = f"""
请根据以下记忆碎片创作一个{story_style}的故事：

记忆碎片：{fragments_text}

创作要求：
1. 故事风格：{story_style}
2. 情感基调：{tone_desc}
3. 故事长度：{length_desc}
4. 将这些记忆碎片自然地融入到一个连贯的故事中
5. 故事要有明确的情节线索，体现"回忆情节 重合明显 模糊了从前"的意境
6. 语言要优美流畅，富有画面感
7. 结尾要有一定的意境和回味

请开始创作：
"""
        
        return prompt.strip()
    
    def call_pollinations_api(self, prompt: str, 
                            model: str = None,
                            seed: int = None,
                            system_prompt: str = None) -> Optional[str]:
        """
        调用Pollinations API生成文本
        
        Args:
            prompt: 输入提示词
            model: 模型名称
            seed: 随机种子
            system_prompt: 系统提示词
            
        Returns:
            生成的文本或None（如果失败）
        """
        if not prompt:
            return None
        
        try:
            # 设置参数
            params = {
                "model": model or self.default_model,
                "seed": seed or self.default_seed,
            }
            
            if system_prompt:
                params["system"] = system_prompt
            
            # URL编码
            encoded_prompt = urllib.parse.quote(prompt)
            encoded_system = urllib.parse.quote(params.get("system", "")) if "system" in params else None
            
            # 构建请求URL
            url = f"{self.api_url}/{encoded_prompt}"
            query_params = {k: v for k, v in params.items() if k != "system"}
            if encoded_system:
                query_params["system"] = encoded_system
            
            # 发送请求
            response = requests.get(url, params=query_params, timeout=30)
            response.raise_for_status()
            
            # 返回结果
            return response.text.strip()
            
        except requests.exceptions.RequestException as e:
            print(f"API请求失败: {e}")
            return None
        except Exception as e:
            print(f"生成故事时发生错误: {e}")
            return None
    
    def generate_story(self, memory_fragments: List[str],
                      story_style: str = "小说风格",
                      emotional_tone: str = "温暖", 
                      story_length: str = "中等",
                      custom_requirements: str = "") -> Dict[str, Any]:
        """
        生成完整故事
        
        Args:
            memory_fragments: 记忆碎片列表
            story_style: 故事风格
            emotional_tone: 情感基调
            story_length: 故事长度
            custom_requirements: 自定义要求
            
        Returns:
            生成结果字典
        """
        if not memory_fragments:
            return {
                'success': False,
                'error': '请提供至少一个记忆碎片',
                'story': '',
                'metadata': {}
            }
        
        # 生成提示词
        base_prompt = self.generate_story_prompt(
            memory_fragments, story_style, emotional_tone, story_length
        )
        
        # 添加自定义要求
        if custom_requirements:
            base_prompt += f"\n\n额外要求：{custom_requirements}"
        
        # 系统提示词
        system_prompt = """你是一位富有想象力的作家，擅长将零散的记忆碎片编织成动人的故事。
你的写作风格优美流畅，善于营造意境，能够准确把握情感基调。
请根据用户提供的记忆碎片和要求，创作出高质量的故事作品。"""
        
        # 调用API生成故事
        story_text = self.call_pollinations_api(
            prompt=base_prompt,
            system_prompt=system_prompt,
            seed=random.randint(1, 10000)  # 使用随机种子增加多样性
        )
        
        if story_text:
            return {
                'success': True,
                'story': story_text,
                'metadata': {
                    'memory_fragments': memory_fragments,
                    'story_style': story_style,
                    'emotional_tone': emotional_tone,
                    'story_length': story_length,
                    'custom_requirements': custom_requirements,
                    'word_count': len(story_text),
                    'generation_time': time.time()
                }
            }
        else:
            return {
                'success': False,
                'error': 'API调用失败，请稍后重试',
                'story': '',
                'metadata': {}
            }
    
    def generate_multiple_versions(self, memory_fragments: List[str],
                                 story_style: str = "小说风格",
                                 emotional_tone: str = "温暖",
                                 story_length: str = "中等",
                                 num_versions: int = 3) -> List[Dict[str, Any]]:
        """
        生成多个版本的故事
        
        Args:
            memory_fragments: 记忆碎片列表
            story_style: 故事风格
            emotional_tone: 情感基调
            story_length: 故事长度
            num_versions: 生成版本数量
            
        Returns:
            故事版本列表
        """
        versions = []
        
        for i in range(num_versions):
            # 为每个版本添加一些变化
            custom_req = f"这是第{i+1}个版本，请在保持核心情节的基础上，尝试不同的叙述角度或细节描写。"
            
            result = self.generate_story(
                memory_fragments=memory_fragments,
                story_style=story_style,
                emotional_tone=emotional_tone,
                story_length=story_length,
                custom_requirements=custom_req
            )
            
            if result['success']:
                result['version'] = i + 1
                versions.append(result)
            
            # 避免API调用过于频繁
            if i < num_versions - 1:
                time.sleep(1)
        
        return versions
    
    def enhance_story(self, original_story: str, enhancement_type: str = "细节丰富") -> Dict[str, Any]:
        """
        增强故事内容
        
        Args:
            original_story: 原始故事
            enhancement_type: 增强类型
            
        Returns:
            增强结果
        """
        if not original_story:
            return {
                'success': False,
                'error': '请提供原始故事内容',
                'enhanced_story': ''
            }
        
        enhancement_prompts = {
            "细节丰富": "请为这个故事添加更多生动的细节描写，包括环境、人物表情、动作等，使故事更加立体丰满。",
            "情感深化": "请深化故事中的情感表达，让人物的内心世界更加丰富，情感变化更加细腻。",
            "意境提升": "请提升故事的意境和文学性，使用更优美的语言和更深刻的意象。",
            "情节完善": "请完善故事的情节结构，添加必要的转折和高潮，使故事更加引人入胜。"
        }
        
        enhancement_prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["细节丰富"])
        
        full_prompt = f"""
原始故事：
{original_story}

增强要求：
{enhancement_prompt}

请在保持原故事核心内容和风格的基础上，按照要求进行增强改写：
"""
        
        system_prompt = "你是一位专业的文学编辑，擅长改进和完善故事内容，能够在保持原作风格的基础上进行有效的增强。"
        
        enhanced_text = self.call_pollinations_api(
            prompt=full_prompt,
            system_prompt=system_prompt
        )
        
        if enhanced_text:
            return {
                'success': True,
                'enhanced_story': enhanced_text,
                'enhancement_type': enhancement_type,
                'original_length': len(original_story),
                'enhanced_length': len(enhanced_text)
            }
        else:
            return {
                'success': False,
                'error': '故事增强失败，请稍后重试',
                'enhanced_story': ''
            }
