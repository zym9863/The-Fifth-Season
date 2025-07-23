"""
第五个季节 - 主应用界面
Streamlit Web应用的主入口
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any
import time

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.settings import APP_TITLE, APP_DESCRIPTION
from src.emotion_analyzer.analyzer import EmotionAnalyzer
from src.emotion_analyzer.visualizer import EmotionVisualizer
from src.story_generator.generator import MemoryStoryGenerator


class FifthSeasonApp:
    """第五个季节主应用类"""
    
    def __init__(self):
        """初始化应用"""
        self.emotion_analyzer = EmotionAnalyzer()
        self.emotion_visualizer = EmotionVisualizer()
        self.story_generator = MemoryStoryGenerator()
        
        # 初始化session state
        self.init_session_state()
    
    def init_session_state(self):
        """初始化会话状态"""
        if 'emotion_history' not in st.session_state:
            st.session_state.emotion_history = []
        if 'story_history' not in st.session_state:
            st.session_state.story_history = []
        if 'current_analysis' not in st.session_state:
            st.session_state.current_analysis = None
        if 'current_story' not in st.session_state:
            st.session_state.current_story = None
    
    def render_header(self):
        """渲染页面头部"""
        st.set_page_config(
            page_title="第五个季节",
            page_icon="🌈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title(APP_TITLE)
        st.markdown(APP_DESCRIPTION)
        st.divider()
    
    def render_sidebar(self):
        """渲染侧边栏"""
        with st.sidebar:
            st.header("🎛️ 功能选择")
            
            # 功能选择
            function_choice = st.radio(
                "选择功能",
                ["🌈 情感光谱分析器", "📖 记忆碎片故事生成器"],
                index=0
            )
            
            st.divider()
            
            # 历史记录
            st.header("📚 历史记录")
            
            if function_choice == "🌈 情感光谱分析器":
                if st.session_state.emotion_history:
                    st.write(f"共有 {len(st.session_state.emotion_history)} 条分析记录")
                    if st.button("清空情感分析历史"):
                        st.session_state.emotion_history = []
                        st.rerun()
                else:
                    st.write("暂无分析记录")
            
            else:
                if st.session_state.story_history:
                    st.write(f"共有 {len(st.session_state.story_history)} 个故事")
                    if st.button("清空故事生成历史"):
                        st.session_state.story_history = []
                        st.rerun()
                else:
                    st.write("暂无故事记录")
            
            st.divider()
            
            # 应用信息
            st.header("ℹ️ 关于应用")
            st.markdown("""
            **第五个季节** 是一个探索内心情感世界的创意应用：
            
            - 🌈 **情感光谱分析**: 深度解析文本情感
            - 📖 **故事生成**: 将记忆碎片编织成故事
            - 🎨 **可视化**: 多种图表展示分析结果
            - 💾 **历史记录**: 保存和回顾分析历史
            """)
        
        return function_choice
    
    def render_emotion_analyzer(self):
        """渲染情感分析器界面"""
        st.header("🌈 情感光谱分析器")
        st.markdown("输入一段文字，探索其中蕴含的复杂情感光谱")
        
        # 输入区域
        col1, col2 = st.columns([3, 1])
        
        with col1:
            input_text = st.text_area(
                "请输入要分析的文本",
                height=150,
                placeholder="在这里输入您想要分析的文字...\n例如：明明暗暗、零零散散，回忆情节重合明显，模糊了从前..."
            )
        
        with col2:
            st.markdown("### 分析选项")
            
            # 分析按钮
            analyze_btn = st.button("🔍 开始分析", type="primary", use_container_width=True)
            
            # 高级选项
            with st.expander("高级选项"):
                save_to_history = st.checkbox("保存到历史记录", value=True)
                show_details = st.checkbox("显示详细信息", value=True)
        
        # 执行分析
        if analyze_btn and input_text.strip():
            with st.spinner("正在分析情感光谱..."):
                analysis_result = self.emotion_analyzer.analyze_text(input_text)
                st.session_state.current_analysis = analysis_result
                
                if save_to_history:
                    st.session_state.emotion_history.append({
                        'text': input_text,
                        'result': analysis_result,
                        'timestamp': time.time()
                    })
        
        # 显示分析结果
        if st.session_state.current_analysis:
            self.display_emotion_analysis_results(
                st.session_state.current_analysis, 
                show_details
            )
    
    def display_emotion_analysis_results(self, analysis_result: Dict[str, Any], show_details: bool = True):
        """显示情感分析结果"""
        st.divider()
        st.header("📊 分析结果")
        
        # 情感摘要
        summary = self.emotion_analyzer.get_emotion_summary(analysis_result)
        st.success(f"**情感摘要**: {summary}")
        
        # 可视化结果
        emotion_weights = analysis_result['emotion_weights']
        
        if emotion_weights:
            # 创建三列布局
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("雷达图")
                radar_fig = self.emotion_visualizer.create_emotion_radar_chart(emotion_weights)
                st.plotly_chart(radar_fig, use_container_width=True)
            
            with col2:
                st.subheader("柱状图")
                bar_fig = self.emotion_visualizer.create_emotion_bar_chart(emotion_weights)
                st.plotly_chart(bar_fig, use_container_width=True)
            
            with col3:
                st.subheader("饼图")
                pie_fig = self.emotion_visualizer.create_emotion_pie_chart(emotion_weights)
                st.plotly_chart(pie_fig, use_container_width=True)
            
            # 词云
            st.subheader("情感词云")
            emotion_keywords = analysis_result['emotion_keywords']
            wordcloud_img = self.emotion_visualizer.create_wordcloud(emotion_keywords, emotion_weights)
            
            if wordcloud_img:
                st.image(f"data:image/png;base64,{wordcloud_img}", use_column_width=True)
            else:
                st.info("未能生成词云图，可能是因为情感关键词较少")
        
        # 详细信息
        if show_details:
            with st.expander("📋 详细分析信息", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("情感权重")
                    if emotion_weights:
                        df_weights = pd.DataFrame(
                            list(emotion_weights.items()),
                            columns=['情感类型', '权重']
                        ).sort_values('权重', ascending=False)
                        st.dataframe(df_weights, use_container_width=True)
                    else:
                        st.info("未检测到明显情感")
                
                with col2:
                    st.subheader("情感关键词")
                    emotion_keywords = analysis_result['emotion_keywords']
                    if emotion_keywords:
                        for emotion, keywords in emotion_keywords.items():
                            if keywords:
                                st.write(f"**{emotion}**: {', '.join(keywords)}")
                    else:
                        st.info("未提取到情感关键词")
                
                # 统计信息
                st.subheader("统计信息")
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                
                with stats_col1:
                    st.metric("词语数量", analysis_result['word_count'])
                
                with stats_col2:
                    st.metric("主导情感", analysis_result['dominant_emotion'] or "无")
                
                with stats_col3:
                    diversity = analysis_result['emotion_diversity']
                    st.metric("情感多样性", f"{diversity:.3f}")
    
    def render_story_generator(self):
        """渲染故事生成器界面"""
        st.header("📖 记忆碎片故事生成器")
        st.markdown("输入记忆碎片关键词，让AI为您编织成连贯的故事")
        
        # 输入区域
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 记忆碎片输入
            st.subheader("记忆碎片")
            
            # 方式1：文本输入
            fragments_text = st.text_area(
                "输入记忆碎片（用逗号或换行分隔）",
                height=100,
                placeholder="例如：夕阳西下, 老槐树, 蝉鸣声, 奶奶的摇椅, 冰棍的甜味..."
            )
            
            # 方式2：标签输入
            st.markdown("或者使用标签输入：")
            fragment_tags = st.text_input(
                "添加记忆碎片标签",
                placeholder="输入一个记忆碎片，按回车添加"
            )
            
            # 显示已添加的碎片
            if 'memory_fragments' not in st.session_state:
                st.session_state.memory_fragments = []
            
            if fragment_tags and st.button("➕ 添加碎片"):
                if fragment_tags not in st.session_state.memory_fragments:
                    st.session_state.memory_fragments.append(fragment_tags)
                    st.rerun()
            
            if st.session_state.memory_fragments:
                st.write("**已添加的记忆碎片：**")
                for i, fragment in enumerate(st.session_state.memory_fragments):
                    col_frag, col_del = st.columns([4, 1])
                    with col_frag:
                        st.write(f"• {fragment}")
                    with col_del:
                        if st.button("🗑️", key=f"del_{i}"):
                            st.session_state.memory_fragments.pop(i)
                            st.rerun()
        
        with col2:
            st.subheader("生成设置")
            
            # 故事风格
            story_style = st.selectbox(
                "故事风格",
                ["小说风格", "电影桥段", "诗意散文", "日记体", "回忆录", "梦境叙述"]
            )
            
            # 情感基调
            emotional_tone = st.selectbox(
                "情感基调",
                ["温暖", "忧伤", "思念", "期待", "失落", "平静", "喜悦", "无助"]
            )
            
            # 故事长度
            story_length = st.selectbox(
                "故事长度",
                ["短", "中等", "长"]
            )
            
            # 自定义要求
            custom_requirements = st.text_area(
                "自定义要求（可选）",
                height=80,
                placeholder="例如：希望故事发生在秋天，主人公是一个小女孩..."
            )
            
            # 生成选项
            num_versions = st.slider("生成版本数", 1, 3, 1)
            
            # 生成按钮
            generate_btn = st.button("✨ 生成故事", type="primary", use_container_width=True)
        
        # 处理记忆碎片
        final_fragments = []
        if fragments_text:
            # 从文本区域解析碎片
            text_fragments = [f.strip() for f in fragments_text.replace('\n', ',').split(',') if f.strip()]
            final_fragments.extend(text_fragments)
        
        final_fragments.extend(st.session_state.memory_fragments)
        final_fragments = list(set(final_fragments))  # 去重
        
        # 生成故事
        if generate_btn and final_fragments:
            with st.spinner("正在编织您的记忆故事..."):
                if num_versions == 1:
                    story_result = self.story_generator.generate_story(
                        memory_fragments=final_fragments,
                        story_style=story_style,
                        emotional_tone=emotional_tone,
                        story_length=story_length,
                        custom_requirements=custom_requirements
                    )
                    
                    if story_result['success']:
                        st.session_state.current_story = [story_result]
                        st.session_state.story_history.append(story_result)
                    else:
                        st.error(f"故事生成失败：{story_result['error']}")
                
                else:
                    story_versions = self.story_generator.generate_multiple_versions(
                        memory_fragments=final_fragments,
                        story_style=story_style,
                        emotional_tone=emotional_tone,
                        story_length=story_length,
                        num_versions=num_versions
                    )
                    
                    if story_versions:
                        st.session_state.current_story = story_versions
                        st.session_state.story_history.extend(story_versions)
                    else:
                        st.error("故事生成失败，请稍后重试")
        
        elif generate_btn and not final_fragments:
            st.warning("请至少输入一个记忆碎片")
        
        # 显示生成的故事
        if st.session_state.current_story:
            self.display_generated_stories(st.session_state.current_story)
    
    def display_generated_stories(self, stories: List[Dict[str, Any]]):
        """显示生成的故事"""
        st.divider()
        st.header("📚 生成的故事")
        
        for i, story_data in enumerate(stories):
            if story_data['success']:
                # 故事标题
                version_text = f" - 版本 {story_data.get('version', i+1)}" if len(stories) > 1 else ""
                st.subheader(f"故事{version_text}")
                
                # 故事内容
                st.markdown(f"""
                <div style="
                    background-color: #f8f9fa;
                    color: #2c3e50;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #007bff;
                    margin: 10px 0;
                    line-height: 1.8;
                    font-size: 16px;
                    font-weight: 400;
                ">
                {story_data['story'].replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # 故事元数据
                with st.expander("📋 故事信息"):
                    metadata = story_data['metadata']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**风格**: {metadata.get('story_style', '未知')}")
                        st.write(f"**基调**: {metadata.get('emotional_tone', '未知')}")
                    
                    with col2:
                        st.write(f"**长度**: {metadata.get('story_length', '未知')}")
                        st.write(f"**字数**: {metadata.get('word_count', 0)}")
                    
                    with col3:
                        st.write(f"**记忆碎片**: {len(metadata.get('memory_fragments', []))}")
                        if metadata.get('custom_requirements'):
                            st.write(f"**自定义要求**: {metadata['custom_requirements']}")
                    
                    st.write("**使用的记忆碎片**:")
                    fragments = metadata.get('memory_fragments', [])
                    if fragments:
                        st.write(", ".join(fragments))
                
                # 故事操作
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"💾 保存故事 {i+1}", key=f"save_{i}"):
                        # 这里可以添加保存到文件的功能
                        st.success("故事已保存到历史记录")
                
                with col2:
                    if st.button(f"🔄 重新生成 {i+1}", key=f"regen_{i}"):
                        # 重新生成当前故事
                        st.info("功能开发中...")
                
                with col3:
                    if st.button(f"✨ 增强故事 {i+1}", key=f"enhance_{i}"):
                        # 增强故事内容
                        st.info("功能开发中...")
                
                if i < len(stories) - 1:
                    st.divider()
    
    def run(self):
        """运行应用"""
        self.render_header()
        function_choice = self.render_sidebar()
        
        # 根据选择渲染对应功能
        if function_choice == "🌈 情感光谱分析器":
            self.render_emotion_analyzer()
        else:
            self.render_story_generator()


def main():
    """主函数"""
    app = FifthSeasonApp()
    app.run()


if __name__ == "__main__":
    main()
