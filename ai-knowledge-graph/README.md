# AI知识图谱系统

## 项目简介

本项目构建了一个**人工智能核心概念知识图谱**，涵盖AI领域的核心实体（算法、模型、技术、应用、人物、组织等）及其关系，实现了从知识表示到知识查询的完整流程。

## 项目成果

✅ **已达成所有核心目标**

- **272个实体** （要求≥200）
- **358个关系三元组** （要求≥300）
- **1549个总三元组** （包含数据属性）
- 完整的RDF/OWL知识表示
- 多功能查询应用
- 可视化分析

## 项目结构

```
ai-knowledge-graph/
├── ontology/               # 本体设计
│   └── ai_ontology.md     # 本体设计文档
├── data/                   # 原始数据
│   └── ai_knowledge_data.json  # AI知识数据集
├── rdf/                    # RDF/OWL文件
│   ├── ai_ontology.ttl    # OWL本体定义
│   ├── ai_knowledge_graph.ttl   # Turtle格式
│   ├── ai_knowledge_graph.rdf   # RDF/XML格式
│   ├── ai_knowledge_graph.nt    # N-Triples格式
│   └── ai_knowledge_graph.n3    # N3格式
├── database/               # 图数据库
│   └── knowledge_graph.pkl      # 序列化的知识图谱
├── scripts/                # 脚本工具
│   ├── build_knowledge_graph.py  # 构建RDF图谱
│   ├── load_knowledge_graph.py   # 加载到数据库
│   ├── test_knowledge_graph.py   # 测试验证
│   ├── demo_auto.py              # 自动演示
│   └── visualize.py              # 可视化生成
├── app/                    # 应用程序
│   └── query_app.py        # 交互式查询应用
├── kg_core.py              # 核心知识图谱类
└── viz_*.png               # 可视化结果
```

## 实体类型（9种）

| 类型 | 数量 | 说明 |
|------|------|------|
| Algorithm | 56 | AI算法（神经网络、Transformer等）|
| Model | 44 | AI模型（GPT、BERT、ResNet等）|
| Concept | 50 | 基础概念（神经元、激活函数等）|
| Technique | 37 | 技术方法（迁移学习、强化学习等）|
| Application | 28 | 应用场景（语音识别、图像分类等）|
| Tool | 22 | 开发工具（TensorFlow、PyTorch等）|
| Person | 14 | 重要人物（Hinton、LeCun、Bengio等）|
| AI_Field | 11 | 研究领域（机器学习、深度学习等）|
| Organization | 10 | 研究机构（OpenAI、DeepMind等）|

## 关系类型（10种）

| 关系 | 数量 | 说明 |
|------|------|------|
| belongsTo | 81 | 属于某领域/类别 |
| appliedIn | 64 | 应用于某场景 |
| relatedTo | 62 | 相关关系 |
| isPartOf | 49 | 是...的一部分 |
| basedon | 29 | 基于某技术发展 |
| usesAlgorithm | 30 | 使用某算法 |
| developedBy | 24 | 由...开发 |
| usesTool | 7 | 使用某工具 |
| worksAt | 7 | 工作于某组织 |
| proposes | 5 | 提出某概念 |

## 快速开始

### 1. 安装依赖

```bash
pip3 install rdflib networkx matplotlib
```

### 2. 构建知识图谱

```bash
# 构建RDF知识图谱
python3 scripts/build_knowledge_graph.py

# 加载到图数据库
python3 scripts/load_knowledge_graph.py
```

### 3. 运行测试

```bash
# 运行完整测试套件
python3 scripts/test_knowledge_graph.py
```

### 4. 查看演示

```bash
# 运行自动演示
python3 scripts/demo_auto.py

# 或启动交互式查询系统
python3 app/query_app.py
```

### 5. 生成可视化

```bash
# 生成可视化图表
python3 scripts/visualize.py
```

## 主要功能

### 1. 知识表示 (RDF/OWL)

- 符合RDF/OWL规范的本体定义
- 多格式输出（Turtle、RDF/XML、N-Triples、N3）
- 完整的实体属性和关系定义

### 2. 知识抽取与融合

- 从结构化数据提取实体和关系
- 实体消歧和融合
- 关系验证和完整性检查

### 3. 知识查询

#### 实体检索
- 关键词搜索
- 按ID或名称精确查找
- 按类型筛选

#### 关系查询
- 查看实体的所有关系
- 按关系类型查询三元组
- 关系路径查找

#### 高级查询
- K跳邻居查询
- 最短路径计算
- 子图提取

### 4. 知识应用

#### 技术选型辅助
```
场景：我想开发图像分类应用，应该使用什么技术？
答案：AlexNet、ResNet、VGG、ViT、CLIP等
```

#### 学习路径推荐
```
场景：学习深度学习需要了解哪些核心算法？
答案：CNN、RNN、Transformer、反向传播、注意力机制等
```

#### 技术演进追踪
```
场景：Transformer如何影响AI发展？
答案：GPT系列、BERT、T5、ViT、CLIP等都基于Transformer
```

## 可视化成果

项目生成了5个可视化图表：

1. **viz_entity_types.png** - 实体类型分布柱状图
2. **viz_relation_types.png** - 关系类型分布图
3. **viz_timeline.png** - AI技术发展时间线
4. **viz_deeplearning_subgraph.png** - 深度学习领域知识子图
5. **viz_gpt_subgraph.png** - GPT相关技术子图

## 技术栈

- **知识表示**：RDF/OWL、Turtle语法
- **图存储**：NetworkX（轻量级）
- **数据处理**：Python 3.10+
- **RDF处理**：rdflib
- **可视化**：matplotlib
- **序列化**：pickle

## 项目特点

### ✅ 符合规范
- 严格遵循RDF/OWL知识表示规范
- 清晰的本体设计和命名空间
- 支持多种RDF序列化格式

### ✅ 易于扩展
- 模块化设计，易于添加新实体和关系
- 支持增量更新
- 灵活的查询接口

### ✅ 实用性强
- 涵盖AI领域核心知识
- 支持多种实际应用场景
- 提供丰富的查询功能

### ✅ 轻量级
- 无需复杂的数据库部署
- 运行速度快
- 易于学习和演示

## 使用示例

### Python API使用

```python
from kg_core import KnowledgeGraph

# 加载知识图谱
kg = KnowledgeGraph()
kg.load('database/knowledge_graph.pkl')

# 搜索实体
results = kg.search_entity('Transformer')
for entity in results:
    print(entity['name'])

# 查询关系
gpt = kg.get_entity_by_name('GPT')
relations = kg.get_relations(gpt['id'])

# 按关系类型查询
openai_products = kg.query_by_relation('developedBy', obj='E074')

# 查找路径
path = kg.get_shortest_path('E061', 'E023')  # Hinton -> GPT
```

### 交互式查询

运行 `python3 app/query_app.py` 启动交互式系统，支持：

1. 关键词搜索实体
2. 查看实体详细信息
3. 探索实体关系网络
4. 按关系类型查询
5. 按实体类型浏览
6. 查找实体间路径
7. 查看统计信息

## 项目验证

运行测试脚本 `python3 scripts/test_knowledge_graph.py`：

- ✅ 10/10 测试通过
- ✅ 实体数量：272 （要求≥200）
- ✅ 关系数量：358 （要求≥300）
- ✅ 数据完整性验证通过
- ✅ 所有查询功能正常

## 知识图谱涵盖内容

### AI领域
机器学习、深度学习、自然语言处理、计算机视觉、强化学习、知识图谱、专家系统等

### 核心算法
神经网络、CNN、RNN、Transformer、反向传播、梯度下降、决策树、SVM、K-means等

### 重要模型
GPT系列、BERT、ResNet、YOLO、AlexNet、GAN、VAE、LSTM、AlphaGo等

### 技术方法
迁移学习、强化学习、注意力机制、对抗训练、数据增强、Fine-tuning、RLHF等

### 应用场景
语音识别、图像分类、机器翻译、推荐系统、自动驾驶、人脸识别、文本生成等

### 重要人物
图灵、Hinton、Bengio、LeCun、Andrew Ng、Ian Goodfellow等

### 研究机构
OpenAI、DeepMind、Google AI、MIT CSAIL、Stanford AI Lab、Meta AI等

### 开发工具
TensorFlow、PyTorch、Keras、scikit-learn、Hugging Face等

## 后续扩展

可以进一步扩展的方向：

1. **数据增强**：添加更多实体和关系
2. **Neo4j集成**：迁移到Neo4j专业图数据库
3. **推理引擎**：实现基于规则的知识推理
4. **API服务**：提供REST API接口
5. **Web界面**：构建可视化Web应用
6. **知识问答**：基于图谱的问答系统
7. **知识更新**：自动从论文和文档提取知识

## 贡献者

本项目作为人工智能基础及应用实践项目完成。

## 许可证

Educational Use Only
