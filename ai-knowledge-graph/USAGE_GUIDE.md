# AI知识图谱系统使用指南

## 目录
1. [环境准备](#环境准备)
2. [快速开始](#快速开始)
3. [功能详解](#功能详解)
4. [应用场景](#应用场景)
5. [常见问题](#常见问题)

---

## 环境准备

### 系统要求
- Python 3.8+
- Linux/MacOS/Windows
- 4GB+ 内存

### 安装依赖

```bash
cd ai-knowledge-graph
pip3 install -r requirements.txt
```

或手动安装：
```bash
pip3 install rdflib networkx matplotlib
```

---

## 快速开始

### 第一步：构建知识图谱

```bash
# 从JSON数据生成RDF知识图谱
python3 scripts/build_knowledge_graph.py
```

**输出**：
- `rdf/ai_knowledge_graph.ttl` - Turtle格式
- `rdf/ai_knowledge_graph.rdf` - RDF/XML格式
- `rdf/ai_knowledge_graph.nt` - N-Triples格式
- `rdf/ai_knowledge_graph.n3` - N3格式

### 第二步：加载到数据库

```bash
# 加载知识图谱到图数据库
python3 scripts/load_knowledge_graph.py
```

**输出**：
- `database/knowledge_graph.pkl` - 图数据库文件

### 第三步：运行测试

```bash
# 验证知识图谱功能
python3 scripts/test_knowledge_graph.py
```

**预期结果**：10/10测试通过

### 第四步：查看演示

```bash
# 运行自动演示
python3 scripts/demo_auto.py
```

### 第五步：生成可视化

```bash
# 生成可视化图表
python3 scripts/visualize.py
```

**输出**：5个PNG可视化文件

---

## 功能详解

### 1. 实体搜索

#### 方式1：交互式应用
```bash
python3 app/query_app.py
# 选择 1 - 实体搜索
# 输入关键词，如：Transformer
```

#### 方式2：Python API
```python
from kg_core import KnowledgeGraph

kg = KnowledgeGraph()
kg.load('database/knowledge_graph.pkl')

# 搜索实体
results = kg.search_entity('Transformer')
for entity in results:
    print(f"{entity['name']} ({entity['type']})")
```

### 2. 实体详情查询

#### Python API
```python
# 按ID查找
entity = kg.get_entity_by_id('E023')

# 按名称查找
entity = kg.get_entity_by_name('GPT')

# 查看详情
print(f"名称：{entity['name']}")
print(f"类型：{entity['type']}")
print(f"描述：{entity['description']}")
print(f"年份：{entity['year']}")
```

### 3. 关系查询

#### 查看实体的所有关系
```python
relations = kg.get_relations('E023')  # GPT

# 出边（主语）
for rel in relations['outgoing']:
    print(f"{rel['predicate']} -> {rel['object_name']}")

# 入边（宾语）
for rel in relations['incoming']:
    print(f"{rel['subject_name']} -> {rel['predicate']}")
```

#### 按关系类型查询
```python
# 查找所有"developedBy"关系
results = kg.query_by_relation('developedBy')

# 查找OpenAI开发的所有产品
openai_products = kg.query_by_relation('developedBy', obj='E074')

# 查找使用Transformer算法的模型
transformer_models = kg.query_by_relation('usesAlgorithm', obj='E012')
```

### 4. 类型查询

```python
# 获取所有Person类型实体
persons = kg.get_entities_by_type('Person')

# 获取所有Model类型实体
models = kg.get_entities_by_type('Model')

# 遍历结果
for model in models:
    print(f"{model['name']} ({model.get('year', 'N/A')})")
```

### 5. 路径查找

```python
# 查找两个实体间的最短路径
path = kg.get_shortest_path('E009', 'E023')  # 神经网络 -> GPT

if path:
    for entity_id in path:
        entity = kg.get_entity_by_id(entity_id)
        print(entity['name'])
```

### 6. 邻居查询

```python
# 获取1跳邻居
neighbors = kg.get_neighbors('E003', depth=1)  # 深度学习

for neighbor_id, data in neighbors.items():
    entity = data['entity']
    depth = data['depth']
    print(f"{entity['name']} (深度={depth})")
```

### 7. 统计分析

```python
# 获取图谱统计信息
stats = kg.get_statistics()

print(f"实体总数：{stats['total_entities']}")
print(f"关系总数：{stats['total_relations']}")
print(f"实体类型分布：{stats['entity_types']}")
print(f"关系类型分布：{stats['relation_types']}")
```

---

## 应用场景

### 场景1：技术选型

**问题**：我要开发一个机器翻译系统，应该使用什么模型？

**查询步骤**：
```python
# 1. 找到机器翻译实体
mt = kg.get_entity_by_name('机器翻译')

# 2. 查找应用于机器翻译的技术
results = kg.query_by_relation('appliedIn', obj=mt['id'])

# 3. 查看推荐模型
for triple in results:
    model = kg.get_entity_by_id(triple['subject'])
    print(f"{model['name']} ({model.get('year', 'N/A')})")
```

**答案**：Transformer、BERT、GPT等模型

### 场景2：学习路径规划

**问题**：学习深度学习需要掌握哪些内容？

**查询步骤**：
```python
# 1. 找到深度学习领域
dl = kg.get_entity_by_name('深度学习')

# 2. 查找属于深度学习的算法和技术
algorithms = kg.query_by_relation('belongsTo', obj=dl['id'])

# 3. 按年份排序，了解学习顺序
sorted_algos = sorted(algorithms,
                      key=lambda x: kg.get_entity_by_id(x['subject']).get('year', '9999'))
```

**学习路径**：
1. 基础（1943-1986）：神经网络、反向传播
2. 进阶（1997-2014）：CNN、RNN、LSTM
3. 前沿（2014-2023）：Transformer、GAN、扩散模型

### 场景3：技术演进分析

**问题**：Transformer对AI发展有什么影响？

**查询步骤**：
```python
# 1. 找到Transformer
transformer = kg.get_entity_by_name('Transformer')

# 2. 查找基于Transformer的技术
evolution = kg.query_by_relation('basedon', obj=transformer['id'])

# 3. 分析影响范围
for triple in evolution:
    tech = kg.get_entity_by_id(triple['subject'])
    print(f"{tech['name']} ({tech['type']}, {tech.get('year')})")
```

**影响分析**：
- NLP：GPT、BERT、T5等
- CV：ViT、CLIP等
- 多模态：DALL-E、Stable Diffusion等

### 场景4：研究机构调研

**问题**：了解OpenAI的技术产出？

**查询步骤**：
```python
# 1. 找到OpenAI
openai = kg.get_entity_by_name('OpenAI')

# 2. 查找OpenAI开发的产品
products = kg.query_by_relation('developedBy', obj=openai['id'])

# 3. 按年份展示
for triple in products:
    product = kg.get_entity_by_id(triple['subject'])
    print(f"{product['name']} ({product.get('year')})")
```

**产出列表**：
- 2018: GPT
- 2019: GPT-2
- 2020: GPT-3
- 2021: CLIP, DALL-E, Codex, GitHub Copilot
- 2022: Whisper
- 2023: GPT-4

---

## 常见问题

### Q1: 如何添加新实体？

**答**：编辑 `data/ai_knowledge_data.json`，添加新实体和关系，然后重新运行构建脚本：

```json
{
  "id": "E999",
  "name": "新实体名称",
  "type": "Model",
  "description": "描述信息",
  "year": "2024"
}
```

然后运行：
```bash
python3 scripts/build_knowledge_graph.py
python3 scripts/load_knowledge_graph.py
```

### Q2: 如何修改本体定义？

**答**：编辑 `rdf/ai_ontology.ttl` 和 `ontology/ai_ontology.md`，添加新的类或属性定义。

### Q3: 如何导出查询结果？

**答**：修改代码保存为文件，例如：

```python
import json

results = kg.search_entity('深度学习')
with open('search_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### Q4: 可以迁移到Neo4j吗？

**答**：可以。提供两种方式：

**方式1：使用py2neo**
```python
from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# 导入实体
for entity_id, entity in kg.entities.items():
    node = Node(entity['type'], **entity)
    graph.create(node)

# 导入关系
for u, v, data in kg.graph.edges(data=True):
    rel = Relationship(nodes[u], data['relation'], nodes[v])
    graph.create(rel)
```

**方式2：使用Cypher CSV导入**

### Q5: 如何提高查询性能？

**答**：对于大规模图谱：
1. 使用Neo4j等专业图数据库
2. 建立索引：`CREATE INDEX ON :Entity(name)`
3. 优化查询语句
4. 使用缓存

### Q6: 中文显示乱码怎么办？

**答**：安装中文字体：
```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei

# 然后在代码中设置
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
```

### Q7: 如何验证RDF文件的正确性？

**答**：使用在线工具或命令行工具：

**在线验证**：
- http://www.easyrdf.org/converter
- http://rdfvalidator.mybluemix.net/

**命令行验证**：
```bash
rapper -i turtle rdf/ai_knowledge_graph.ttl
```

### Q8: 可以查询SPARQL吗？

**答**：可以。使用rdflib的SPARQL功能：

```python
from rdflib import Graph

g = Graph()
g.parse('rdf/ai_knowledge_graph.ttl', format='turtle')

# SPARQL查询
query = """
PREFIX ai: <http://www.ai-kg.org/ontology#>
SELECT ?name ?type WHERE {
    ?entity ai:name ?name .
    ?entity rdf:type ?type .
}
LIMIT 10
"""

results = g.query(query)
for row in results:
    print(f"{row.name}: {row.type}")
```

---

## 交互式应用使用指南

运行 `python3 app/query_app.py` 后的菜单：

```
==========================================
AI知识图谱查询系统
==========================================
1. 实体搜索（关键词搜索）
2. 查看实体详情
3. 查询实体关系
4. 按关系类型查询
5. 按实体类型查询
6. 查找实体间路径
7. 查看图谱统计
0. 退出
==========================================
```

### 使用示例

#### 示例1：搜索实体
```
请选择操作：1
请输入搜索关键词：深度学习

找到 24 个匹配的实体：
1. [E003] 深度学习 (AI_Field)
   描述：基于多层神经网络的机器学习方法
   年份：2006
...
```

#### 示例2：查看实体详情
```
请选择操作：2
请输入实体ID或名称：GPT

实体详情：GPT
====================
ID：E023
类型：Model
描述：生成式预训练Transformer模型
年份：2018

【出边关系】：
  → basedon → Transformer
  → developedBy → OpenAI
  → appliedIn → 文本生成
...
```

#### 示例3：按关系查询
```
请选择操作：4
请输入关系类型：developedBy

找到 24 个 [developedBy] 关系：
1. GPT --[developedBy]--> OpenAI
2. BERT --[developedBy]--> Google AI
3. ResNet --[developedBy]--> Microsoft Research
...
```

#### 示例4：按类型查询
```
请选择操作：5
请输入实体类型：Person

找到 14 个 [Person] 类型的实体：
1. Alan Turing
2. Geoffrey Hinton
3. Yoshua Bengio
...
```

---

## 数据说明

### 实体ID编码规则
- E001-E050: AI领域、应用、人物、组织
- E051-E150: 算法和模型
- E151-E272: 概念、技术、工具

### 关系说明

| 关系 | 示例 | 说明 |
|------|------|------|
| belongsTo | CNN belongsTo 深度学习 | 算法属于某领域 |
| basedon | GPT basedon Transformer | 技术演进关系 |
| developedBy | BERT developedBy Google | 开发归属 |
| appliedIn | CNN appliedIn 图像分类 | 应用场景 |
| usesAlgorithm | GPT usesAlgorithm Transformer | 使用的算法 |
| usesTool | GPT usesTool PyTorch | 使用的工具 |
| isPartOf | 神经元 isPartOf 神经网络 | 组成关系 |
| relatedTo | AI relatedTo 认知科学 | 相关关系 |
| worksAt | Hinton worksAt Google | 任职关系 |
| proposes | Hinton proposes 反向传播 | 提出贡献 |

---

## 高级使用

### 自定义查询

创建自己的查询脚本：

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from kg_core import KnowledgeGraph

kg = KnowledgeGraph()
kg.load('database/knowledge_graph.pkl')

# 自定义查询：找出所有2020年后的模型
models = kg.get_entities_by_type('Model')
recent_models = [m for m in models if m.get('year', '0') >= '2020']

for model in recent_models:
    print(f"{model['name']} ({model['year']})")

    # 查看这些模型使用的算法
    rels = kg.get_relations(model['id'])
    algos = [r['object_name'] for r in rels['outgoing']
             if r['predicate'] == 'usesAlgorithm']
    if algos:
        print(f"  使用算法：{', '.join(algos)}")
```

### 数据导出

#### 导出为CSV
```python
import csv

# 导出所有实体
with open('entities.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'type', 'description', 'year'])
    writer.writeheader()
    for entity in kg.entities.values():
        writer.writerow({
            'id': entity['id'],
            'name': entity['name'],
            'type': entity['type'],
            'description': entity.get('description', ''),
            'year': entity.get('year', '')
        })

# 导出所有关系
with open('relations.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['subject', 'predicate', 'object'])
    for u, v, data in kg.graph.edges(data=True):
        writer.writerow([u, data['relation'], v])
```

#### 导出为GraphML
```python
import networkx as nx

# 导出为GraphML格式（可用Gephi可视化）
nx.write_graphml(kg.graph, 'knowledge_graph.graphml')
```

---

## 可视化说明

### 1. 实体类型分布图 (viz_entity_types.png)
- 柱状图展示9种实体类型的数量分布
- 用于了解图谱的整体结构

### 2. 关系类型分布图 (viz_relation_types.png)
- 水平柱状图展示10种关系的数量
- 用于分析关系的丰富程度

### 3. AI发展时间线 (viz_timeline.png)
- 散点图展示AI技术的历史发展
- 按年份排列，了解技术演进

### 4. 深度学习子图 (viz_deeplearning_subgraph.png)
- 以"深度学习"为中心的1跳邻居网络
- 展示深度学习的技术生态

### 5. GPT子图 (viz_gpt_subgraph.png)
- 以"GPT"为中心的关系网络
- 展示GPT的技术基础和应用

---

## 性能优化建议

### 对于小规模图谱（<1000实体）
- 当前方案已足够快速
- 无需额外优化

### 对于中等规模图谱（1000-10000实体）
- 考虑使用SQLite存储实体数据
- 为常用查询添加缓存
- 使用索引加速查找

### 对于大规模图谱（>10000实体）
- 迁移到Neo4j等专业图数据库
- 使用Cypher查询语言
- 分布式存储和查询

---

## 开发扩展

### 添加新的查询功能

在 `kg_core.py` 中添加新方法：

```python
def find_experts_by_field(self, field_name: str) -> List[Dict]:
    """查找某领域的专家"""
    field = self.get_entity_by_name(field_name)
    if not field:
        return []

    experts = []
    persons = self.get_entities_by_type('Person')

    for person in persons:
        if person.get('field') == field_name:
            experts.append(person)

    return experts
```

### 添加统计图表

在 `scripts/visualize.py` 中添加新函数：

```python
def visualize_network_metrics(kg, output_file='viz_metrics.png'):
    """可视化网络指标"""
    # 计算度中心性
    degree_centrality = nx.degree_centrality(kg.graph)

    # 找出最重要的节点
    top_nodes = sorted(degree_centrality.items(),
                      key=lambda x: x[1], reverse=True)[:10]

    # 绘制柱状图
    names = [kg.entities[node_id]['name'] for node_id, _ in top_nodes]
    values = [score for _, score in top_nodes]

    plt.figure(figsize=(12, 6))
    plt.bar(names, values)
    plt.xlabel('实体')
    plt.ylabel('中心性分数')
    plt.title('最重要的实体（按度中心性）')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
```

---

## 最佳实践

### 1. 数据维护
- 定期验证数据完整性
- 保持实体描述的准确性
- 及时更新新技术

### 2. 查询优化
- 使用ID查询比名称查询更快
- 缓存频繁查询的结果
- 限制返回结果数量

### 3. 代码规范
- 遵循PEP 8编码规范
- 添加类型注解
- 编写单元测试

### 4. 文档更新
- 保持README与代码同步
- 记录重要的设计决策
- 提供充足的示例代码

---

## 参考资源

### 技术文档
- [RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/)
- [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)

### 相关库
- [rdflib Documentation](https://rdflib.readthedocs.io/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)

### 工具
- [Protégé](https://protege.stanford.edu/) - 本体编辑器
- [Gephi](https://gephi.org/) - 图可视化工具
- [Neo4j Desktop](https://neo4j.com/download/) - 图数据库

---

## 联系与反馈

如有问题或建议，欢迎：
- 查看项目文档
- 运行测试验证
- 提出改进建议

---

**最后更新**：2026年3月26日
