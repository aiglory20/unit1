#!/usr/bin/env python3
"""
知识图谱导入和查询系统（轻量级版本）
使用networkx进行图存储和查询
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from kg_core import KnowledgeGraph


def main():
    """主函数：创建知识图谱并保存"""
    print("="*60)
    print("知识图谱导入系统（轻量级版本）")
    print("="*60)

    # 创建知识图谱
    kg = KnowledgeGraph()

    # 从JSON加载数据
    kg.load_from_json('data/ai_knowledge_data.json')

    # 保存知识图谱
    kg.save('database/knowledge_graph.pkl')

    # 打印统计信息
    print("\n" + "="*60)
    print("知识图谱统计信息")
    print("="*60)
    stats = kg.get_statistics()
    print(f"实体总数：{stats['total_entities']}")
    print(f"关系总数：{stats['total_relations']}")
    print("\n实体类型分布：")
    for entity_type, count in sorted(stats['entity_types'].items()):
        print(f"  {entity_type}: {count}")
    print("\n关系类型分布：")
    for relation_type, count in sorted(stats['relation_types'].items()):
        print(f"  {relation_type}: {count}")
    print("="*60)


if __name__ == '__main__':
    main()
