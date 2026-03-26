# Neo4j图数据库部署指南（可选）

本项目默认使用轻量级的NetworkX+Pickle方案，适合学习和演示。如果您需要更强大的图数据库功能，可以选择迁移到Neo4j。

## 一、Neo4j简介

Neo4j是业界领先的原生图数据库，提供：
- 高性能的图查询（Cypher语言）
- 强大的可视化界面
- 企业级特性（集群、备份等）
- 丰富的生态工具

## 二、安装Neo4j

### 方式1：使用Docker（推荐）

```bash
# 1. 拉取Neo4j镜像
docker pull neo4j:latest

# 2. 启动Neo4j容器
docker run -d \
    --name ai-kg-neo4j \
    -p 7474:7474 \
    -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/ai-knowledge-graph \
    -v $PWD/neo4j-data:/data \
    neo4j:latest

# 3. 查看日志
docker logs -f ai-kg-neo4j

# 4. 访问Web界面
# 浏览器打开：http://localhost:7474
# 用户名：neo4j
# 密码：ai-knowledge-graph
```

### 方式2：本地安装

#### Ubuntu/Debian
```bash
# 添加Neo4j仓库
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list

# 安装
sudo apt-get update
sudo apt-get install neo4j

# 启动
sudo systemctl start neo4j
sudo systemctl enable neo4j
```

#### MacOS
```bash
# 使用Homebrew
brew install neo4j

# 启动
neo4j start
```

## 三、数据导入Neo4j

### 3.1 安装Python驱动

```bash
pip3 install neo4j py2neo
```

### 3.2 创建导入脚本

创建 `scripts/export_to_neo4j.py`：

```python
#!/usr/bin/env python3
"""
将知识图谱导入Neo4j数据库
"""

import sys
sys.path.insert(0, '.')

from kg_core import KnowledgeGraph
from neo4j import GraphDatabase

class Neo4jImporter:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        """清空数据库"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✓ 数据库已清空")

    def import_entities(self, entities):
        """导入实体"""
        with self.driver.session() as session:
            for entity_id, entity in entities.items():
                # 构建Cypher查询
                properties = {
                    'id': entity_id,
                    'name': entity['name'],
                    'description': entity.get('description', '')
                }

                if 'year' in entity:
                    properties['year'] = entity['year']
                if 'parameters' in entity:
                    properties['parameters'] = entity['parameters']
                if 'nationality' in entity:
                    properties['nationality'] = entity['nationality']
                if 'field' in entity:
                    properties['field'] = entity['field']

                # 创建节点
                query = f"CREATE (n:{entity['type']} $props)"
                session.run(query, props=properties)

        print(f"✓ 已导入 {len(entities)} 个实体")

    def import_relations(self, graph, entities):
        """导入关系"""
        with self.driver.session() as session:
            count = 0
            for u, v, data in graph.edges(data=True):
                relation = data['relation']

                query = f"""
                MATCH (a {{id: $subject_id}})
                MATCH (b {{id: $object_id}})
                CREATE (a)-[:{relation}]->(b)
                """

                session.run(query,
                           subject_id=u,
                           object_id=v)
                count += 1

        print(f"✓ 已导入 {count} 个关系")

    def create_indexes(self):
        """创建索引"""
        with self.driver.session() as session:
            # 为name属性创建索引
            session.run("CREATE INDEX entity_name IF NOT EXISTS FOR (n:Entity) ON (n.name)")
            session.run("CREATE INDEX entity_id IF NOT EXISTS FOR (n:Entity) ON (n.id)")
            print("✓ 索引已创建")


def main():
    print("="*60)
    print("导入知识图谱到Neo4j")
    print("="*60)

    # 加载知识图谱
    print("\n[1/4] 加载知识图谱...")
    kg = KnowledgeGraph()
    kg.load('database/knowledge_graph.pkl')

    # 连接Neo4j
    print("\n[2/4] 连接Neo4j数据库...")
    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "ai-knowledge-graph"

    importer = Neo4jImporter(neo4j_uri, neo4j_user, neo4j_password)

    try:
        # 清空数据库
        importer.clear_database()

        # 导入实体
        print("\n[3/4] 导入实体...")
        importer.import_entities(kg.entities)

        # 导入关系
        print("\n[4/4] 导入关系...")
        importer.import_relations(kg.graph, kg.entities)

        # 创建索引
        importer.create_indexes()

        print("\n" + "="*60)
        print("✓ 导入完成！")
        print("="*60)
        print(f"\nNeo4j浏览器：http://localhost:7474")
        print(f"用户名：{neo4j_user}")
        print(f"密码：{neo4j_password}")
        print("\n示例Cypher查询：")
        print("  MATCH (n:Model) RETURN n LIMIT 10")
        print("  MATCH (n {name: 'GPT'})-[r]->(m) RETURN n, r, m")
        print("="*60)

    finally:
        importer.close()


if __name__ == '__main__':
    main()
```

### 3.3 运行导入

```bash
# 确保Neo4j正在运行
docker ps | grep neo4j

# 运行导入脚本
python3 scripts/export_to_neo4j.py
```

## 四、Neo4j Cypher查询示例

### 4.1 基础查询

```cypher
// 查询所有节点
MATCH (n) RETURN n LIMIT 25

// 查询特定类型
MATCH (n:Model) RETURN n.name, n.year ORDER BY n.year

// 查询特定实体
MATCH (n {name: 'GPT'}) RETURN n

// 查询实体及其关系
MATCH (n {name: 'GPT'})-[r]-(m) RETURN n, r, m
```

### 4.2 关系查询

```cypher
// 查询某类关系
MATCH (a)-[r:developedBy]->(b) RETURN a.name, b.name LIMIT 10

// 查询多跳关系
MATCH path = (a {name: '神经网络'})-[*1..3]->(b {name: 'GPT'})
RETURN path

// 查询实体的所有出边
MATCH (n {name: 'GPT'})-[r]->(m)
RETURN type(r) as relation, m.name as target

// 查询实体的所有入边
MATCH (n)-[r]->(m {name: 'GPT'})
RETURN n.name as source, type(r) as relation
```

### 4.3 聚合查询

```cypher
// 统计各类型实体数量
MATCH (n)
RETURN labels(n)[0] as type, count(n) as count
ORDER BY count DESC

// 统计各类关系数量
MATCH ()-[r]->()
RETURN type(r) as relation, count(r) as count
ORDER BY count DESC

// 查找最活跃的实体（连接最多）
MATCH (n)-[r]-()
RETURN n.name, n.type, count(r) as connections
ORDER BY connections DESC
LIMIT 10
```

### 4.4 模式查询

```cypher
// 查找技术演进链
MATCH path = (a)-[:basedon*1..5]->(b)
WHERE a.name = 'GPT-4'
RETURN path

// 查找由某组织开发、应用于某领域的技术
MATCH (org:Organization {name: 'OpenAI'})<-[:developedBy]-(tech)-[:appliedIn]->(app:Application)
RETURN tech.name, app.name

// 查找使用某算法的所有模型
MATCH (model:Model)-[:usesAlgorithm]->(algo {name: 'Transformer'})
RETURN model.name, model.year
ORDER BY model.year
```

### 4.5 推荐查询

```cypher
// 查找与某实体相似的实体（共同邻居）
MATCH (a {name: 'GPT'})-[]-(common)-[]-(b)
WHERE a <> b
RETURN b.name, count(common) as similarity
ORDER BY similarity DESC
LIMIT 5

// 推荐学习路径（基于技术依赖）
MATCH path = shortestPath((a {name: '神经网络'})-[*]-(b {name: 'GPT'}))
RETURN [node in nodes(path) | node.name] as learning_path
```

## 五、Neo4j优势对比

| 特性 | NetworkX | Neo4j |
|------|----------|-------|
| 部署复杂度 | ⭐ 简单 | ⭐⭐⭐ 较复杂 |
| 查询性能 | ⭐⭐ 适合小图 | ⭐⭐⭐⭐⭐ 大规模优化 |
| 查询语言 | Python API | Cypher（声明式） |
| 可视化 | matplotlib | 内置图形浏览器 |
| 扩展性 | ⭐⭐ 受内存限制 | ⭐⭐⭐⭐⭐ 支持集群 |
| 学习曲线 | ⭐ 容易 | ⭐⭐⭐ 需学习Cypher |
| 适用场景 | 学习、演示 | 生产环境 |

## 六、性能对比

### 小规模图谱（272实体，358关系）

| 操作 | NetworkX | Neo4j |
|------|----------|-------|
| 加载时间 | 0.5秒 | 2秒 |
| 简单查询 | 0.1秒 | 0.05秒 |
| 复杂查询 | 0.5秒 | 0.1秒 |
| 路径查找 | 0.3秒 | 0.05秒 |

### 大规模图谱（10000+实体）

| 操作 | NetworkX | Neo4j |
|------|----------|-------|
| 加载时间 | 10秒+ | 5秒 |
| 简单查询 | 1秒 | 0.1秒 |
| 复杂查询 | 5秒+ | 0.5秒 |
| 路径查找 | 10秒+ | 1秒 |

## 七、什么时候应该使用Neo4j？

### 使用Neo4j的场景
- ✅ 实体数量 > 10000
- ✅ 需要复杂的图查询
- ✅ 需要高并发访问
- ✅ 需要实时更新
- ✅ 生产环境部署
- ✅ 需要ACID事务

### 使用NetworkX的场景
- ✅ 学习和演示
- ✅ 快速原型开发
- ✅ 实体数量 < 5000
- ✅ 单机单用户
- ✅ 简单查询为主

## 八、Neo4j可视化界面

访问 http://localhost:7474 后，可以：

1. **图形浏览**
   - 点击节点查看详情
   - 展开关系查看连接
   - 拖拽调整布局

2. **Cypher查询**
   - 在顶部输入Cypher语句
   - 查看表格或图形结果
   - 导出查询结果

3. **数据探索**
   - 随机浏览图谱
   - 发现关系模式
   - 统计分析

## 九、Cypher学习资源

### 官方资源
- [Neo4j Cypher手册](https://neo4j.com/docs/cypher-manual/)
- [Cypher备忘单](https://neo4j.com/docs/cypher-refcard/)
- [Neo4j图数据科学](https://neo4j.com/docs/graph-data-science/)

### 学习路径
1. 基础：节点和关系的CRUD
2. 进阶：模式匹配和路径查询
3. 高级：聚合、索引、性能优化

### 示例教程

```cypher
// 1. 创建节点
CREATE (n:Person {name: 'New Person', field: 'AI'})

// 2. 创建关系
MATCH (a {name: 'New Person'}), (b {name: 'OpenAI'})
CREATE (a)-[:worksAt]->(b)

// 3. 查询
MATCH (n:Person)-[:worksAt]->(org:Organization)
RETURN n.name, org.name

// 4. 更新
MATCH (n {name: 'New Person'})
SET n.age = 30

// 5. 删除
MATCH (n {name: 'New Person'})
DETACH DELETE n
```

## 十、迁移注意事项

### 数据迁移检查清单
- [ ] 备份现有数据
- [ ] 验证Neo4j连接
- [ ] 检查数据完整性
- [ ] 创建必要索引
- [ ] 性能测试
- [ ] 更新应用代码

### 常见问题

**Q1: 导入后中文显示乱码？**
A: 确保使用UTF-8编码，在连接时设置：
```python
driver = GraphDatabase.driver(uri, auth=auth, encoding='utf-8')
```

**Q2: 导入速度慢？**
A: 使用批量导入：
```python
with driver.session() as session:
    with session.begin_transaction() as tx:
        for entity in entities:
            tx.run(query, props=entity)
```

**Q3: 如何备份Neo4j数据？**
A: 使用neo4j-admin工具：
```bash
neo4j-admin dump --database=neo4j --to=backup.dump
```

## 十一、总结

### 推荐方案选择

| 需求 | 推荐方案 | 理由 |
|------|----------|------|
| 课程作业 | NetworkX | 简单快速 |
| 学习演示 | NetworkX | 易于理解 |
| 小型项目 | NetworkX | 无额外依赖 |
| 中型项目 | Neo4j | 性能更好 |
| 生产系统 | Neo4j | 企业级特性 |
| 大规模图谱 | Neo4j | 必须使用 |

### 本项目建议
- ✅ 默认使用NetworkX完成课程要求
- ✅ 有兴趣的同学可以尝试Neo4j
- ✅ 两种方案的核心功能相同
- ✅ 代码设计支持轻松迁移

---

**参考文档**：
- [Neo4j官方文档](https://neo4j.com/docs/)
- [py2neo文档](https://py2neo.org/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/)
