#!/usr/bin/env python3
"""
知识抽取和融合脚本
将JSON格式的AI知识数据转换为RDF三元组
"""

import json
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD, OWL

# 定义命名空间
AI = Namespace("http://www.ai-kg.org/ontology#")
ENTITY = Namespace("http://www.ai-kg.org/entity#")

def load_json_data(json_file):
    """加载JSON数据文件"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_knowledge_graph(data):
    """创建知识图谱RDF表示"""
    g = Graph()

    # 绑定命名空间
    g.bind('ai', AI)
    g.bind('entity', ENTITY)
    g.bind('owl', OWL)

    # 加载本体定义
    print("正在加载本体定义...")
    try:
        g.parse('rdf/ai_ontology.ttl', format='turtle')
        print("本体定义加载成功")
    except Exception as e:
        print(f"警告：无法加载本体文件，将继续处理数据。错误：{e}")

    # 处理实体
    print(f"\n正在处理 {len(data['entities'])} 个实体...")
    entity_count = 0
    for entity in data['entities']:
        entity_uri = ENTITY[entity['id']]
        entity_type = AI[entity['type']]

        # 添加实体类型
        g.add((entity_uri, RDF.type, entity_type))

        # 添加名称
        g.add((entity_uri, AI.name, Literal(entity['name'], lang='zh')))

        # 添加描述
        if 'description' in entity:
            g.add((entity_uri, AI.description, Literal(entity['description'], lang='zh')))

        # 添加年份
        if 'year' in entity:
            g.add((entity_uri, AI.year, Literal(entity['year'], datatype=XSD.gYear)))

        # 添加特定属性
        if 'parameters' in entity:
            g.add((entity_uri, AI.parameters, Literal(entity['parameters'], lang='zh')))

        if 'nationality' in entity:
            g.add((entity_uri, AI.nationality, Literal(entity['nationality'], lang='zh')))

        if 'field' in entity:
            g.add((entity_uri, AI.field, Literal(entity['field'], lang='zh')))

        if 'founded' in entity:
            g.add((entity_uri, AI.founded, Literal(entity['founded'], datatype=XSD.gYear)))

        entity_count += 1
        if entity_count % 50 == 0:
            print(f"  已处理 {entity_count} 个实体")

    print(f"✓ 实体处理完成：共 {entity_count} 个实体")

    # 处理关系
    print(f"\n正在处理 {len(data['relations'])} 个关系三元组...")
    relation_count = 0
    for relation in data['relations']:
        subject_uri = ENTITY[relation['subject']]
        predicate_uri = AI[relation['predicate']]
        object_uri = ENTITY[relation['object']]

        g.add((subject_uri, predicate_uri, object_uri))
        relation_count += 1

        if relation_count % 50 == 0:
            print(f"  已处理 {relation_count} 个关系")

    print(f"✓ 关系处理完成：共 {relation_count} 个三元组")

    return g

def save_rdf_formats(graph, base_path):
    """保存多种RDF格式"""
    formats = {
        'turtle': 'ttl',
        'xml': 'rdf',
        'nt': 'nt',
        'n3': 'n3'
    }

    print(f"\n正在保存RDF文件...")
    for format_name, extension in formats.items():
        output_file = f"{base_path}.{extension}"
        try:
            graph.serialize(destination=output_file, format=format_name, encoding='utf-8')
            print(f"✓ 保存 {format_name} 格式：{output_file}")
        except Exception as e:
            print(f"✗ 保存 {format_name} 格式失败：{e}")

def print_statistics(graph):
    """打印知识图谱统计信息"""
    print("\n" + "="*60)
    print("知识图谱统计信息")
    print("="*60)

    # 统计三元组总数
    total_triples = len(graph)
    print(f"三元组总数: {total_triples}")

    # 统计实体数量（按类型）
    entity_types = [
        ('AI_Field', '领域'),
        ('Algorithm', '算法'),
        ('Model', '模型'),
        ('Technique', '技术'),
        ('Application', '应用'),
        ('Person', '人物'),
        ('Organization', '组织'),
        ('Tool', '工具'),
        ('Concept', '概念')
    ]

    print("\n实体类型分布:")
    total_entities = 0
    for type_name, chinese_name in entity_types:
        type_uri = AI[type_name]
        count = len(list(graph.subjects(RDF.type, type_uri)))
        print(f"  {chinese_name} ({type_name}): {count}")
        total_entities += count

    print(f"\n实体总数: {total_entities}")

    # 统计关系类型
    print("\n关系类型分布:")
    relation_types = set()
    for s, p, o in graph:
        if str(p).startswith('http://www.ai-kg.org/ontology#'):
            pred_name = str(p).split('#')[-1]
            if pred_name not in ['name', 'description', 'year', 'parameters',
                                  'nationality', 'field', 'founded']:
                relation_types.add(pred_name)

    for rel_type in sorted(relation_types):
        rel_uri = AI[rel_type]
        count = len(list(graph.subject_objects(rel_uri)))
        print(f"  {rel_type}: {count}")

    print("="*60)

def main():
    """主函数"""
    print("="*60)
    print("AI知识图谱构建系统")
    print("知识抽取、融合与RDF转换")
    print("="*60)

    # 加载数据
    print("\n[1/3] 加载JSON数据...")
    data = load_json_data('data/ai_knowledge_data.json')
    print(f"✓ 数据加载成功：{len(data['entities'])} 实体，{len(data['relations'])} 关系")

    # 创建知识图谱
    print("\n[2/3] 构建RDF知识图谱...")
    graph = create_knowledge_graph(data)

    # 保存RDF文件
    print("\n[3/3] 保存RDF文件...")
    save_rdf_formats(graph, 'rdf/ai_knowledge_graph')

    # 打印统计信息
    print_statistics(graph)

    print("\n✓ 知识图谱构建完成！")
    print(f"输出文件位置：rdf/ai_knowledge_graph.*")

if __name__ == '__main__':
    main()
