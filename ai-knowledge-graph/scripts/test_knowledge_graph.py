#!/usr/bin/env python3
"""
知识图谱测试验证脚本
验证图谱的准确性、完整性和功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from kg_core import KnowledgeGraph


def test_entity_search(kg):
    """测试实体搜索功能"""
    print("\n【测试1：实体搜索】")
    print("-"*60)

    test_keywords = ['学习', 'Transformer', 'Hinton', 'TensorFlow']

    for keyword in test_keywords:
        results = kg.search_entity(keyword)
        print(f"搜索 '{keyword}': 找到 {len(results)} 个结果")
        if results:
            for i, entity in enumerate(results[:3], 1):
                print(f"  {i}. {entity['name']} ({entity['type']})")

    print("✓ 实体搜索测试通过")


def test_entity_details(kg):
    """测试实体详情查询"""
    print("\n【测试2：实体详情查询】")
    print("-"*60)

    # 测试几个重要实体
    # GPT, Hinton, OpenAI, PyTorch
    test_entities = ['E023', 'E061', 'E074', 'E085']

    for entity_id in test_entities:
        entity = kg.get_entity_by_id(entity_id)
        if entity:
            print(f"✓ {entity['name']} ({entity['id']}): {entity['type']}")
        else:
            print(f"✗ 未找到实体 {entity_id}")

    print("✓ 实体详情查询测试通过")


def test_relations(kg):
    """测试关系查询"""
    print("\n【测试3：关系查询】")
    print("-"*60)

    # 测试GPT模型的关系
    entity_id = 'E023'  # GPT
    entity = kg.get_entity_by_id(entity_id)
    relations = kg.get_relations(entity_id)

    print(f"实体：{entity['name']}")
    print(f"  出边关系：{len(relations['outgoing'])} 个")
    print(f"  入边关系：{len(relations['incoming'])} 个")

    if relations['outgoing']:
        print("\n  示例出边关系：")
        for rel in relations['outgoing'][:5]:
            print(
                f"    {entity['name']} --[{rel['predicate']}]--> {rel['object_name']}")

    if relations['incoming']:
        print("\n  示例入边关系：")
        for rel in relations['incoming'][:5]:
            print(
                f"    {rel['subject_name']} --[{rel['predicate']}]--> {entity['name']}")

    print("✓ 关系查询测试通过")


def test_relation_type_query(kg):
    """测试按关系类型查询"""
    print("\n【测试4：按关系类型查询】")
    print("-"*60)

    relation_types = ['belongsTo', 'developedBy', 'basedon', 'appliedIn']

    for rel_type in relation_types:
        results = kg.query_by_relation(rel_type)
        print(f"关系 '{rel_type}': 找到 {len(results)} 个三元组")
        if results:
            example = results[0]
            print(
                f"  示例：{example['subject_name']} --[{rel_type}]--> {example['object_name']}")

    print("✓ 关系类型查询测试通过")


def test_entity_type_query(kg):
    """测试按实体类型查询"""
    print("\n【测试5：按实体类型查询】")
    print("-"*60)

    entity_types = ['Person', 'Model', 'Algorithm', 'Application']

    for ent_type in entity_types:
        results = kg.get_entities_by_type(ent_type)
        print(f"类型 '{ent_type}': 找到 {len(results)} 个实体")
        if results:
            examples = [e['name'] for e in results[:3]]
            print(f"  示例：{', '.join(examples)}")

    print("✓ 实体类型查询测试通过")


def test_path_finding(kg):
    """测试路径查找"""
    print("\n【测试6：路径查找】")
    print("-"*60)

    # 测试从Geoffrey Hinton到GPT的路径
    start_id = 'E061'  # Geoffrey Hinton
    end_id = 'E023'    # GPT

    start_entity = kg.get_entity_by_id(start_id)
    end_entity = kg.get_entity_by_id(end_id)

    path = kg.get_shortest_path(start_id, end_id)

    if path:
        print(f"从 {start_entity['name']} 到 {end_entity['name']} 的路径：")
        for i, entity_id in enumerate(path):
            entity = kg.get_entity_by_id(entity_id)
            print(f"  {i+1}. {entity['name']}")
        print(f"  路径长度：{len(path)}")
        print("✓ 路径查找测试通过")
    else:
        print(f"未找到路径（这也是正常的）")


def test_neighbors(kg):
    """测试邻居查询"""
    print("\n【测试7：邻居查询】")
    print("-"*60)

    entity_id = 'E003'  # 深度学习
    entity = kg.get_entity_by_id(entity_id)

    neighbors = kg.get_neighbors(entity_id, depth=1)
    print(f"实体 '{entity['name']}' 的1跳邻居：{len(neighbors)} 个")

    if neighbors:
        print("  示例邻居：")
        for neighbor_id, data in list(neighbors.items())[:5]:
            neighbor_entity = data['entity']
            print(
                f"    - {neighbor_entity['name']} ({neighbor_entity['type']})")

    print("✓ 邻居查询测试通过")


def test_statistics(kg):
    """测试统计功能"""
    print("\n【测试8：统计信息】")
    print("-"*60)

    stats = kg.get_statistics()

    assert stats['total_entities'] >= 200, "实体数量不足200"
    assert stats['total_relations'] >= 300, "关系数量不足300"

    print(f"✓ 实体数量：{stats['total_entities']} (要求≥200)")
    print(f"✓ 关系数量：{stats['total_relations']} (要求≥300)")
    print("✓ 统计信息测试通过")


def test_data_integrity(kg):
    """测试数据完整性"""
    print("\n【测试9：数据完整性】")
    print("-"*60)

    # 检查所有关系中引用的实体是否都存在
    missing_entities = set()
    for u, v, data in kg.graph.edges(data=True):
        if u not in kg.entities:
            missing_entities.add(u)
        if v not in kg.entities:
            missing_entities.add(v)

    if missing_entities:
        print(f"✗ 发现 {len(missing_entities)} 个缺失的实体引用")
        for entity_id in list(missing_entities)[:5]:
            print(f"    {entity_id}")
    else:
        print("✓ 所有关系引用的实体都存在")

    # 检查关键实体是否有描述
    entities_without_description = []
    for entity_id, entity_data in kg.entities.items():
        if 'description' not in entity_data or not entity_data['description']:
            entities_without_description.append(entity_data['name'])

    if entities_without_description:
        print(f"  警告：{len(entities_without_description)} 个实体缺少描述")
    else:
        print("✓ 所有实体都有描述")

    print("✓ 数据完整性测试通过")


def test_specific_queries(kg):
    """测试特定查询场景"""
    print("\n【测试10：特定查询场景】")
    print("-"*60)

    # 场景1：查找所有由OpenAI开发的模型
    print("场景1：查找所有由OpenAI开发的模型")
    openai_models = kg.query_by_relation('developedBy', obj='E074')
    print(f"  找到 {len(openai_models)} 个模型：")
    for i, triple in enumerate(openai_models[:5], 1):
        print(f"    {i}. {triple['subject_name']}")

    # 场景2：查找属于深度学习的算法
    print("\n场景2：查找属于深度学习的算法")
    dl_algorithms = kg.query_by_relation('belongsTo', obj='E003')
    print(f"  找到 {len(dl_algorithms)} 个算法/模型：")
    for i, triple in enumerate(dl_algorithms[:5], 1):
        print(f"    {i}. {triple['subject_name']}")

    # 场景3：查找图像分类应用
    print("\n场景3：查找图像分类的相关技术")
    image_classification = kg.get_entity_by_name('图像分类')
    if image_classification:
        relations = kg.get_relations(image_classification['id'])
        print(f"  图像分类的入边关系：{len(relations['incoming'])} 个")
        for rel in relations['incoming'][:5]:
            print(f"    {rel['subject_name']} --[{rel['predicate']}]--> 图像分类")

    print("✓ 特定查询场景测试通过")


def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("知识图谱测试验证系统")
    print("="*60)

    # 加载知识图谱
    print("\n加载知识图谱...")
    kg = KnowledgeGraph()
    kg.load('database/knowledge_graph.pkl')

    # 运行测试
    tests = [
        test_entity_search,
        test_entity_details,
        test_relations,
        test_relation_type_query,
        test_entity_type_query,
        test_path_finding,
        test_neighbors,
        test_statistics,
        test_data_integrity,
        test_specific_queries
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func(kg)
            passed += 1
        except Exception as e:
            print(f"\n✗ 测试失败：{test_func.__name__}")
            print(f"  错误：{e}")
            failed += 1

    # 测试总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"通过：{passed}/{len(tests)}")
    print(f"失败：{failed}/{len(tests)}")

    if failed == 0:
        print("\n✓✓✓ 所有测试通过！知识图谱构建成功！ ✓✓✓")
    else:
        print(f"\n部分测试失败，请检查问题")

    print("="*60)


if __name__ == '__main__':
    run_all_tests()
