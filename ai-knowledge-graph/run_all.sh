#!/bin/bash
# AI知识图谱系统 - 一键启动脚本

echo "======================================================================="
echo "                   AI知识图谱系统 - 一键启动"
echo "======================================================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到python3，请先安装Python 3.8+"
    exit 1
fi

echo "✓ Python版本：$(python3 --version)"

# 检查依赖
echo -e "\n检查依赖..."
python3 -c "import rdflib, networkx, matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 依赖未安装，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动安装：pip3 install rdflib networkx matplotlib"
        exit 1
    fi
    echo "✓ 依赖安装成功"
else
    echo "✓ 依赖已安装"
fi

# 步骤1：构建RDF知识图谱
echo -e "\n======================================================================="
echo "步骤 1/5：构建RDF知识图谱"
echo "======================================================================="
python3 scripts/build_knowledge_graph.py
if [ $? -ne 0 ]; then
    echo "❌ RDF构建失败"
    exit 1
fi

# 步骤2：加载到数据库
echo -e "\n======================================================================="
echo "步骤 2/5：加载到图数据库"
echo "======================================================================="
python3 scripts/load_knowledge_graph.py
if [ $? -ne 0 ]; then
    echo "❌ 数据库加载失败"
    exit 1
fi

# 步骤3：运行测试
echo -e "\n======================================================================="
echo "步骤 3/5：运行测试验证"
echo "======================================================================="
python3 scripts/test_knowledge_graph.py
if [ $? -ne 0 ]; then
    echo "⚠️  测试未全部通过，但系统可以继续使用"
fi

# 步骤4：生成可视化
echo -e "\n======================================================================="
echo "步骤 4/5：生成可视化"
echo "======================================================================="
python3 scripts/visualize.py
if [ $? -ne 0 ]; then
    echo "⚠️  可视化生成失败，但不影响核心功能"
fi

# 步骤5：运行演示
echo -e "\n======================================================================="
echo "步骤 5/5：运行功能演示"
echo "======================================================================="
python3 scripts/demo_auto.py

# 总结
echo -e "\n======================================================================="
echo "                         启动完成！"
echo "======================================================================="
echo ""
echo "📊 已生成文件："
echo "  • RDF文件：rdf/ai_knowledge_graph.{ttl,rdf,nt,n3}"
echo "  • 数据库文件：database/knowledge_graph.pkl"
echo "  • 可视化图表：viz_*.png (5个文件)"
echo ""
echo "💻 下一步操作："
echo "  • 查看可视化：打开 viz_*.png 文件"
echo "  • 交互式查询：python3 app/query_app.py"
echo "  • 查看报告：cat PROJECT_REPORT.md"
echo "  • 阅读文档：cat README.md"
echo ""
echo "📖 文档位置："
echo "  • README.md - 项目说明"
echo "  • PROJECT_REPORT.md - 详细报告"
echo "  • USAGE_GUIDE.md - 使用指南"
echo "  • ontology/ai_ontology.md - 本体设计"
echo ""
echo "======================================================================="
