#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目安装脚本
自动设置虚拟环境和安装依赖
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """运行命令并显示进度"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ 需要Python 3.8或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def create_virtual_environment():
    """创建虚拟环境"""
    if os.path.exists("venv"):
        print("发现已存在的虚拟环境")
        choice = input("是否重新创建？(y/N): ").strip().lower()
        if choice != 'y':
            print("使用现有虚拟环境")
            return True
    
    return run_command("python -m venv venv", "创建虚拟环境")

def activate_virtual_environment():
    """激活虚拟环境"""
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        pip_path = os.path.join("venv", "bin", "pip")
    
    # 设置环境变量
    os.environ['VIRTUAL_ENV'] = os.path.abspath("venv")
    if platform.system() == "Windows":
        os.environ['PATH'] = os.path.join(os.path.abspath("venv"), "Scripts") + os.pathsep + os.environ['PATH']
    else:
        os.environ['PATH'] = os.path.join(os.path.abspath("venv"), "bin") + os.pathsep + os.environ['PATH']
    
    return pip_path

def install_dependencies(pip_path):
    """安装项目依赖"""
    # 升级pip
    run_command(f'"{pip_path}" install --upgrade pip', "升级pip")
    
    # 安装依赖
    return run_command(f'"{pip_path}" install -r requirements.txt', "安装项目依赖")

def create_directories():
    """创建必要的目录"""
    directories = ["data", "data/books", "data/analysis"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ 创建数据目录完成")

def main():
    """主安装流程"""
    print("=" * 60)
    print("图灵图书数据抓取与分析系统 - 安装程序")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 创建虚拟环境
    if not create_virtual_environment():
        print("虚拟环境创建失败，请检查Python安装")
        sys.exit(1)
    
    # 激活虚拟环境并获取pip路径
    pip_path = activate_virtual_environment()
    
    # 安装依赖
    if not install_dependencies(pip_path):
        print("依赖安装失败，请检查网络连接和requirements.txt文件")
        sys.exit(1)
    
    # 创建目录
    create_directories()
    
    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("=" * 60)
    print("\n下一步操作:")
    print("1. 激活虚拟环境:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("\n2. 运行测试:")
    print("   python test_project.py")
    print("\n3. 开始使用:")
    print("   python main.py --max-pages 3  # 小规模测试")
    print("   python main.py                 # 完整运行")
    print("\n4. 查看帮助:")
    print("   python main.py --help")
    print("=" * 60)

if __name__ == "__main__":
    main() 