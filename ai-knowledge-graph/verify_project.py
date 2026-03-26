#!/usr/bin/env python3
"""
项目完成验证脚本
快速验证项目的完整性和正确性
"""

import os
import sys


def check_files():
    """检查文件完整性"""
    print("="*70)
    print("【1/5】检查文件完整性")
    print("="*70)

    required_files = [
        # 核心文件
        ('kg_core.py', '核心类'),
        ('requirements.txt', '依赖配置'),
        ('run_all.sh', '启动脚本'),

        # 数据文件
        ('data/ai_knowledge_data.json', '原始数据'),
        ('database/knowledge_graph.pkl', '图数据库'),

        # RDF文件
        ('rdf/ai_ontology.ttl', 'OWL本体'),
        ('rdf/ai_knowledge_graph.ttl', 'RDF图谱'),

        # 脚本
        ('scripts/build_knowledge_graph.py', '构建脚本'),
        ('scripts/load_knowledge_graph.py', '加载脚本'),
        ('scripts/test_knowledge_graph.py', '测试脚本'),
        ('scripts/visualize.py', '可视化脚本'),

        # 应用
        ('app/query_app.py', '查询应用'),

        # 文档
        ('README.md', '项目说明'),
        ('PROJECT_REPORT.md', '项目报告'),
        ('USAGE_GUIDE.md', '使用指南'),
        ('PROJECT_OVERVIEW.md', '项目总览'),
        ('CHECKLIST.md', '检查清单'),

        # 可视化（至少应该存在）
        ('viz_entity_types.png', '实体分布图'),
        ('viz_relation_types.png', '关系分布图'),
    ]

    missing = []
    total = len(required_files)
    found = 0

    for file_path, description in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            size_str = f"{size/1024:.1f}KB" if size < 1024 * \
                1024 else f"{size/1024/1024:.1f}MB"
            print(f"  ✓ {description:20s} {file_path:40s} ({size_str})")
            found += 1
        else:
            print(f"  ✗ {description:20s} {file_path:40s} (缺失)")
            missing.append(file_path)

    print(f"\n文件完整性：{found}/{total} ({found*100//total}%)")

    if missing:
        print(f"\n⚠️  缺失文件：{len(missing)}个")
        for f in missing:
            print(f"  - {f}")
        return False

    print("✓ 所有核心文件完整")
    return True


def check_dependencies():
    """检查依赖"""
    print("\n" + "="*70)
    print("【2/5】检查依赖库")
    print("="*70)

    dependencies = [
        ('rdflib', 'RDF处理'),
        ('networkx', '图算法'),
        ('matplotlib', '可视化'),
    ]

    all_ok = True
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"  ✓ {description:15s} {module}")
        except ImportError:
            print(f"  ✗ {description:15s} {module} (未安装)")
            all_ok = False

    if all_ok:
        print("\n✓ 所有依赖已安装")
    else:
        print("\n⚠️  请运行：pip3 install -r requirements.txt")

    return all_ok


def check_data_quality():
    """检查数据质量"""
    print("\n" + "="*70)
    print("【3/5】检查数据质量")
    print("="*70)

    try:
        import json

        # 检查JSON数据
        with open('data/ai_knowledge_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        entities = data['entities']
        relations = data['relations']

        print(f"  实体数量：{len(entities)}")
        print(f"  关系数量：{len(relations)}")

        # 检查要求
        if len(entities) >= 200:
            print(f"  ✓ 实体数量达标 (要求≥200)")
        else:
            print(f"  ✗ 实体数量不足 (要求≥200)")
            return False

        if len(relations) >= 300:
            print(f"  ✓ 关系数量达标 (要求≥300)")
        else:
            print(f"  ✗ 关系数量不足 (要求≥300)")
            return False

        # 检查数据完整性
        entity_ids = {e['id'] for e in entities}
        invalid_relations = []

        for rel in relations:
            if rel['subject'] not in entity_ids or rel['object'] not in entity_ids:
                invalid_relations.append(rel)

        if invalid_relations:
            print(f"  ✗ 发现{len(invalid_relations)}个无效关系")
            return False
        else:
            print(f"  ✓ 所有关系引用有效")

        print("\n✓ 数据质量检查通过")
        return True

    except Exception as e:
        print(f"  ✗ 数据检查失败：{e}")
        return False


def check_rdf_files():
    """检查RDF文件"""
    print("\n" + "="*70)
    print("【4/5】检查RDF文件")
    print("="*70)

    rdf_files = [
        ('rdf/ai_ontology.ttl', 'turtle'),
        ('rdf/ai_knowledge_graph.ttl', 'turtle'),
        ('rdf/ai_knowledge_graph.rdf', 'xml'),
        ('rdf/ai_knowledge_graph.nt', 'nt'),
    ]

    all_ok = True
    for file_path, format_name in rdf_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✓ {file_path:40s} ({size:>8d} bytes)")
        else:
            print(f"  ✗ {file_path:40s} (缺失)")
            all_ok = False

    if all_ok:
        print("\n✓ 所有RDF文件存在")
        return True
    else:
        print("\n⚠️  部分RDF文件缺失")
        return False


def check_functionality():
    """检查功能可用性"""
    print("\n" + "="*70)
    print("【5/5】检查功能可用性")
    print("="*70)

    try:
        sys.path.insert(0, '.')
        from kg_core import KnowledgeGraph

        # 加载知识图谱
        print("  正在加载知识图谱...")
        kg = KnowledgeGraph()
        kg.load('database/knowledge_graph.pkl')
        print("  ✓ 知识图谱加载成功")

        # 测试基本功能
        print("\n  测试基本功能：")

        # 1. 搜索
        results = kg.search_entity('GPT')
        print(f"    ✓ 实体搜索：找到{len(results)}个结果")

        # 2. 查询
        gpt = kg.get_entity_by_name('GPT')
        if gpt:
            print(f"    ✓ 实体查询：{gpt['name']}")
        else:
            print(f"    ✗ 实体查询失败")
            return False

        # 3. 关系
        relations = kg.get_relations(gpt['id'])
        print(
            f"    ✓ 关系查询：{len(relations['outgoing'])}出边，{len(relations['incoming'])}入边")

        # 4. 统计
        stats = kg.get_statistics()
        print(
            f"    ✓ 统计信息：{stats['total_entities']}实体，{stats['total_relations']}关系")

        print("\n✓ 所有功能正常")
        return True

    except Exception as e:
        print(f"\n✗ 功能检查失败：{e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*70)
    print(" "*20 + "项目完成验证系统")
    print("="*70)
    print()

    results = []

    # 运行检查
    results.append(('文件完整性', check_files()))
    results.append(('依赖库', check_dependencies()))
    results.append(('数据质量', check_data_quality()))
    results.append(('RDF文件', check_rdf_files()))
    results.append(('功能可用性', check_functionality()))

    # 总结
    print("\n" + "="*70)
    print("验证总结")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {check_name:20s} {status}")

    print(f"\n总计：{passed}/{total} 项检查通过")

    if passed == total:
        print("\n" + "="*70)
        print("🎉🎉🎉 项目验证通过！所有检查均正常！ 🎉🎉🎉")
        print("="*70)
        print("\n✅ 项目已完成，可以提交！")
        print("\n📚 快速开始：")
        print("  • 查看总览：cat PROJECT_OVERVIEW.md")
        print("  • 运行演示：python3 scripts/demo_auto.py")
        print("  • 交互查询：python3 app/query_app.py")
        print("  • 查看报告：cat PROJECT_REPORT.md")
        print("="*70)
    else:
        print("\n⚠️  部分检查未通过，请检查上述问题")

    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
