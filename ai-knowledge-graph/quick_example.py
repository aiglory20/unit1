#!/usr/bin/env python3
"""
快速查询示例
展示如何使用知识图谱API
"""

import sys
sys.path.insert(0, '.')

from kg_core import KnowledgeGraph

# 加载知识图谱
print("正在加载AI知识图谱...")
kg = KnowledgeGraph()
kg.load('database/knowledge_graph.pkl')
print("✓ 加载完成\n")

# ================== 示例查询 ==================

print("="*70)
print("【示例1：搜索实体】")
print("="*70)
print("查询：搜索'GPT'相关实体\n")
results = kg.search_entity('GPT')
for i, entity in enumerate(results[:5], 1):
    print(f"{i}. {entity['name']} ({entity['type']}) - {entity.get('year', 'N/A')}")

print("\n" + "="*70)
print("【示例2：查看实体详情和关系】")
print("="*70)
print("查询：GPT模型的详细信息和关系网络\n")
gpt = kg.get_entity_by_name('GPT')
print(f"名称：{gpt['name']}")
print(f"类型：{gpt['type']}")
print(f"描述：{gpt['description']}")
print(f"年份：{gpt['year']}")

relations = kg.get_relations(gpt['id'])
print(f"\n关系网络：")
print(f"  出边：{len(relations['outgoing'])}个")
for rel in relations['outgoing']:
    print(f"    • GPT --[{rel['predicate']}]--> {rel['object_name']}")

print(f"\n  入边：{len(relations['incoming'])}个")
for rel in relations['incoming'][:3]:
    print(f"    • {rel['subject_name']} --[{rel['predicate']}]--> GPT")

print("\n" + "="*70)
print("【示例3：按关系类型查询】")
print("="*70)
print("查询：查找所有由OpenAI开发的产品\n")
openai = kg.get_entity_by_name('OpenAI')
results = kg.query_by_relation('developedBy', obj=openai['id'])
print(f"OpenAI开发的产品（共{len(results)}个）：")
for i, triple in enumerate(results, 1):
    model = kg.get_entity_by_id(triple['subject'])
    print(f"  {i}. {triple['subject_name']} ({model.get('year', 'N/A')})")

print("\n" + "="*70)
print("【示例4：按实体类型查询】")
print("="*70)
print("查询：所有AI研究领域\n")
fields = kg.get_entities_by_type('AI_Field')
for i, field in enumerate(fields, 1):
    print(f"  {i}. {field['name']} ({field.get('year', 'N/A')})")

print("\n" + "="*70)
print("【示例5：技术演进分析】")
print("="*70)
print("查询：基于Transformer发展的技术\n")
transformer = kg.get_entity_by_name('Transformer')
results = kg.query_by_relation('basedon', obj=transformer['id'])
print(f"基于Transformer的技术（共{len(results)}个）：")
for i, triple in enumerate(results[:10], 1):
    tech = kg.get_entity_by_id(triple['subject'])
    print(f"  {i}. {triple['subject_name']} ({tech['type']}, {tech.get('year', 'N/A')})")

print("\n" + "="*70)
print("【示例6：应用场景分析】")
print("="*70)
print("查询：图像分类可以使用哪些模型？\n")
image_class = kg.get_entity_by_name('图像分类')
results = kg.query_by_relation('appliedIn', obj=image_class['id'])
print(f"适用于图像分类的模型（共{len(results)}个）：")
for i, triple in enumerate(results, 1):
    model = kg.get_entity_by_id(triple['subject'])
    print(f"  {i}. {triple['subject_name']} ({model.get('year', 'N/A')})")

print("\n" + "="*70)
print("【示例7：统计分析】")
print("="*70)
stats = kg.get_statistics()
print(f"知识图谱统计：")
print(f"  • 实体总数：{stats['total_entities']}")
print(f"  • 关系总数：{stats['total_relations']}")

print("\n" + "="*70)
print("✨ 更多功能请运行：python3 app/query_app.py")
print("="*70)
