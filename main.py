"""
第五个季节 - 主入口文件
启动Streamlit应用
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.ui.main_app import main

if __name__ == "__main__":
    main()
