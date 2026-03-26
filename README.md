# AI知识图谱项目总览

## 🎯 项目状态

**✅ 项目已全部完成** - 2026年3月26日

所有核心目标均已达成并超过要求：

- ✅ 实体数量：272个 （要求≥200，达成率136%）
- ✅ 关系三元组：358个 （要求≥300，达成率119%）
- ✅ RDF/OWL知识表示完成
- ✅ 图数据库部署完成
- ✅ 查询应用开发完成
- ✅ 测试验证全部通过（10/10）

## 📁 项目文件结构

```
ai-knowledge-graph/
├── 📖 README.md                      # 项目说明（从这里开始）
├── 📊 PROJECT_REPORT.md              # 详细项目报告
├── 📚 USAGE_GUIDE.md                 # 使用指南
├── 🔧 NEO4J_GUIDE.md                 # Neo4j部署指南（可选）
├── 🚀 run_all.sh                     # 一键启动脚本
├── 📋 requirements.txt               # Python依赖
│
├── 🧠 kg_core.py                     # 知识图谱核心类（209行）
│
├── ontology/                         # 本体设计
│   └── ai_ontology.md               # 本体设计文档
│
├── data/                             # 数据文件
│   └── ai_knowledge_data.json       # AI知识数据（272实体，358关系）
│
├── rdf/                              # RDF/OWL文件
│   ├── ai_ontology.ttl              # OWL本体定义
│   ├── ai_knowledge_graph.ttl       # Turtle格式（推荐）
│   ├── ai_knowledge_graph.rdf       # RDF/XML格式
│   ├── ai_knowledge_graph.nt        # N-Triples格式
│   └── ai_knowledge_graph.n3        # N3格式
│
├── database/                         # 图数据库
│   └── knowledge_graph.pkl          # 序列化图数据库
│
├── scripts/                          # 脚本工具
│   ├── build_knowledge_graph.py     # 构建RDF图谱（123行）
│   ├── load_knowledge_graph.py      # 加载到数据库（56行）
│   ├── test_knowledge_graph.py      # 测试验证（284行）
│   ├── demo_auto.py                 # 自动演示（180行）
│   ├── demo.py                      # 交互式演示（220行）
│   └── visualize.py                 # 可视化生成（272行）
│
├── app/                              # 应用程序
│   └── query_app.py                 # 交互式查询应用（210行）
│
└── 📊 viz_*.png                      # 可视化结果（5个文件）
    ├── viz_entity_types.png         # 实体类型分布
    ├── viz_relation_types.png       # 关系类型分布
    ├── viz_timeline.png             # AI发展时间线
    ├── viz_deeplearning_subgraph.png # 深度学习子图
    └── viz_gpt_subgraph.png         # GPT相关子图
```

## 🚀 快速启动（3种方式）

### 方式1：一键运行（推荐）

```bash
./run_all.sh
```

### 方式2：分步执行

```bash
# 步骤1：构建RDF知识图谱
python3 scripts/build_knowledge_graph.py

# 步骤2：加载到数据库
python3 scripts/load_knowledge_graph.py

# 步骤3：运行测试（可选）
python3 scripts/test_knowledge_graph.py

# 步骤4：查看演示
python3 scripts/demo_auto.py

# 步骤5：生成可视化（可选）
python3 scripts/visualize.py
```

### 方式3：交互式查询

```bash
python3 app/query_app.py
```

## 📊 项目成果数据

### 知识图谱规模

```
总计：1549个三元组
├── 实体：272个
│   ├── AI_Field（领域）: 11个
│   ├── Algorithm（算法）: 56个
│   ├── Model（模型）: 44个
│   ├── Technique（技术）: 37个
│   ├── Application（应用）: 28个
│   ├── Person（人物）: 14个
│   ├── Organization（组织）: 10个
│   ├── Tool（工具）: 22个
│   └── Concept（概念）: 50个
│
└── 关系：358个
    ├── belongsTo（属于）: 81个
    ├── appliedIn（应用于）: 64个
    ├── relatedTo（相关）: 62个
    ├── isPartOf（组成）: 49个
    ├── usesAlgorithm（使用算法）: 30个
    ├── basedon（基于）: 29个
    ├── developedBy（开发者）: 24个
    ├── usesTool（使用工具）: 7个
    ├── worksAt（工作于）: 7个
    └── proposes（提出）: 5个
```

## 🔧 核心功能

### 查询功能（7种）

1. ⭐ 实体搜索 - 关键词检索
2. ⭐ 实体详情 - ID/名称查找
3. ⭐ 关系查询 - 出入边遍历
4. ⭐ 关系类型查询 - 按关系筛选
5. ⭐ 实体类型查询 - 按类型浏览
6. ⭐ 路径查找 - 最短路径算法
7. ⭐ 统计分析 - 图谱概览

### 可视化功能（5种）

1. 📊 实体类型分布
2. 📊 关系类型分布
3. 📈 AI发展时间线
4. 🕸️ 领域知识子图
5. 🕸️ 模型关系子图

## 💡 典型应用场景

### 1️⃣ 技术选型

```
问：开发图像分类应用用什么模型？
答：AlexNet、ResNet、VGG、ViT、CLIP
查询：推荐模型及其年份、特点
```

### 2️⃣ 学习规划

```
问：学习深度学习的知识路径？
答：神经网络 -> CNN/RNN -> Transformer -> GPT
查询：技术依赖关系和学习顺序
```

### 3️⃣ 技术调研

```
问：Transformer如何影响AI发展？
答：衍生出GPT、BERT、ViT等数十个模型
查询：技术演进树和影响范围
```

### 4️⃣ 工具选择

```
问：深度学习框架选PyTorch还是TensorFlow？
答：查看开发者、生态和主流使用情况
查询：工具对比和使用案例
```
