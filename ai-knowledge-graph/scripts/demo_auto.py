#!/usr/bin/env python3
"""
知识图谱自动演示脚本（无交互）
展示核心功能和查询示例
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kg_core import KnowledgeGraph


def main():
    """主函数"""
    print("="*70)
    print(" "*20 + "AI知识图谱系统演示")
    print("="*70)

    # 加载知识图谱
    print("\n正在加载知识图谱...")
    kg = KnowledgeGraph()
    kg.load('database/knowledge_graph.pkl')

    # 基本统计
    print("\n" + "="*70)
    print("【基本统计】")
    print("="*70)
    stats = kg.get_statistics()
    print(f"✓ 实体总数：{stats['total_entities']} 个")
    print(f"✓ 关系总数：{stats['total_relations']} 个")
    print(f"✓ 实体类型：{len(stats['entity_types'])} 种")
    print(f"✓ 关系类型：{len(stats['relation_types'])} 种")

    # 演示1：实体搜索
    print("\n" + "="*70)
    print("【演示1：实体搜索】")
    print("="*70)
    print("\n搜索关键词 'Transformer'：")
    results = kg.search_entity('Transformer')
    for i, entity in enumerate(results[:5], 1):
        print(f"  {i}. {entity['name']} ({entity['type']})")

    # 演示2：查看GPT详情
    print("\n" + "="*70)
    print("【演示2：实体详情查询】")
    print("="*70)
    gpt = kg.get_entity_by_name('GPT')
    print(f"\n实体：{gpt['name']}")
    print(f"类型：{gpt['type']}")
    print(f"描述：{gpt['description']}")
    print(f"年份：{gpt['year']}")

    relations = kg.get_relations(gpt['id'])
    print(f"\n出边关系（{len(relations['outgoing'])}个）：")
    for rel in relations['outgoing']:
        print(f"  • {gpt['name']} --[{rel['predicate']}]--> {rel['object_name']}")

    print(f"\n入边关系（{len(relations['incoming'])}个）：")
    for rel in relations['incoming'][:5]:
        print(f"  • {rel['subject_name']} --[{rel['predicate']}]--> {gpt['name']}")

    # 演示3：按关系查询
    print("\n" + "="*70)
    print("【演示3：按关系类型查询】")
    print("="*70)
    print("\n查询所有'developedBy'关系（前10个）：")
    results = kg.query_by_relation('developedBy')
    for i, triple in enumerate(results[:10], 1):
        print(f"  {i}. {triple['subject_name']} --[由...开发]--> {triple['object_name']}")

    # 演示4：按类型查询
    print("\n" + "="*70)
    print("【演示4：按实体类型查询】")
    print("="*70)
    print("\n所有AI研究领域：")
    fields = kg.get_entities_by_type('AI_Field')
    for i, field in enumerate(fields, 1):
        print(f"  {i}. {field['name']} ({field.get('year', 'N/A')})")

    print("\n\n重要人物（前5位）：")
    persons = kg.get_entities_by_type('Person')
    for i, person in enumerate(persons[:5], 1):
        print(f"  {i}. {person['name']} - {person['description'][:50]}...")

    # 演示5：应用场景查询
    print("\n" + "="*70)
    print("【演示5：应用场景分析】")
    print("="*70)
    print("\n查找所有应用于'图像分类'的模型：")
    image_class = kg.get_entity_by_name('图像分类')
    if image_class:
        results = kg.query_by_relation('appliedIn', obj=image_class['id'])
        for i, triple in enumerate(results, 1):
            model = kg.get_entity_by_id(triple['subject'])
            print(f"  {i}. {triple['subject_name']} ({model.get('year', 'N/A')})")

    # 演示6：技术栈分析
    print("\n" + "="*70)
    print("【演示6：技术栈分析】")
    print("="*70)
    print("\n深度学习领域的核心算法（前10个）：")
    dl = kg.get_entity_by_name('深度学习')
    results = kg.query_by_relation('belongsTo', obj=dl['id'])
    for i, triple in enumerate(results[:10], 1):
        algo = kg.get_entity_by_id(triple['subject'])
        print(f"  {i}. {triple['subject_name']} ({algo.get('year', 'N/A')})")

    # 演示7：组织生态
    print("\n" + "="*70)
    print("【演示7：组织生态分析】")
    print("="*70)
    orgs = kg.get_entities_by_type('Organization')
    print(f"\n发现 {len(orgs)} 个AI研究组织：")
    for org in orgs:
        print(f"\n• {org['name']} ({org.get('founded', 'N/A')})")
        print(f"  {org['description']}")

        # 查找该组织开发的产品
        results = kg.query_by_relation('developedBy', obj=org['id'])
        if results:
            products = [r['subject_name'] for r in results]
            print(f"  主要产品：{', '.join(products[:5])}")

    # 总结
    print("\n" + "="*70)
    print("【演示完成】")
    print("="*70)
    print("\n知识图谱系统已成功演示以下功能：")
    print("  ✓ 实体搜索和检索")
    print("  ✓ 实体详情查看")
    print("  ✓ 关系查询和探索")
    print("  ✓ 类型分类查询")
    print("  ✓ 应用场景分析")
    print("  ✓ 技术演进追踪")
    print("  ✓ 组织生态分析")
    print("\n📊 可视化文件已生成：")
    print("  • viz_entity_types.png")
    print("  • viz_relation_types.png")
    print("  • viz_timeline.png")
    print("  • viz_deeplearning_subgraph.png")
    print("  • viz_gpt_subgraph.png")
    print("\n💻 交互式查询：")
    print("  运行 'python3 app/query_app.py' 启动交互式查询系统")
    print("="*70)


if __name__ == '__main__':
    main()
