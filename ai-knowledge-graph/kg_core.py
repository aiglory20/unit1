#!/usr/bin/env python3
"""
知识图谱核心模块
包含KnowledgeGraph类的定义
"""

import json
import networkx as nx
import pickle
from typing import List, Dict, Any


class KnowledgeGraph:
    """知识图谱类"""

    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.entities = {}

    def load_from_json(self, json_file: str):
        """从JSON文件加载知识图谱"""
        print(f"正在加载知识图谱：{json_file}")

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 加载实体
        print(f"  加载 {len(data['entities'])} 个实体...")
        for entity in data['entities']:
            entity_id = entity['id']
            self.entities[entity_id] = entity
            self.graph.add_node(entity_id, **entity)

        # 加载关系
        print(f"  加载 {len(data['relations'])} 个关系...")
        for relation in data['relations']:
            self.graph.add_edge(
                relation['subject'],
                relation['object'],
                relation=relation['predicate']
            )

        print(f"✓ 知识图谱加载完成")
        print(f"  节点数：{self.graph.number_of_nodes()}")
        print(f"  边数：{self.graph.number_of_edges()}")

    def save(self, file_path: str):
        """保存知识图谱"""
        data = {
            'graph': self.graph,
            'entities': self.entities
        }
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"✓ 知识图谱已保存到：{file_path}")

    def load(self, file_path: str):
        """加载知识图谱"""
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        self.graph = data['graph']
        self.entities = data['entities']
        print(f"✓ 知识图谱已加载")

    def search_entity(self, keyword: str) -> List[Dict]:
        """搜索实体"""
        results = []
        keyword_lower = keyword.lower()

        for entity_id, entity_data in self.entities.items():
            if (keyword_lower in entity_data['name'].lower() or
                    keyword_lower in entity_data.get('description', '').lower()):
                results.append(entity_data)

        return results

    def get_entity_by_id(self, entity_id: str) -> Dict:
        """根据ID获取实体"""
        return self.entities.get(entity_id)

    def get_entity_by_name(self, name: str) -> Dict:
        """根据名称精确查找实体"""
        for entity_id, entity_data in self.entities.items():
            if entity_data['name'] == name:
                return entity_data
        return None

    def get_relations(self, entity_id: str) -> Dict[str, List]:
        """获取实体的所有关系"""
        relations = {
            'outgoing': [],  # 出边（主语）
            'incoming': []   # 入边（宾语）
        }

        # 获取出边（该实体作为主语）
        if entity_id in self.graph:
            for target in self.graph.successors(entity_id):
                edge_data = self.graph.get_edge_data(entity_id, target)
                for key, data in edge_data.items():
                    relations['outgoing'].append({
                        'predicate': data['relation'],
                        'object': target,
                        'object_name': self.entities[target]['name']
                    })

        # 获取入边（该实体作为宾语）
        if entity_id in self.graph:
            for source in self.graph.predecessors(entity_id):
                edge_data = self.graph.get_edge_data(source, entity_id)
                for key, data in edge_data.items():
                    relations['incoming'].append({
                        'predicate': data['relation'],
                        'subject': source,
                        'subject_name': self.entities[source]['name']
                    })

        return relations

    def query_by_relation(self, predicate: str, subject: str = None, obj: str = None) -> List[Dict]:
        """按关系查询三元组"""
        results = []

        for u, v, data in self.graph.edges(data=True):
            if data['relation'] == predicate:
                if subject and u != subject:
                    continue
                if obj and v != obj:
                    continue

                results.append({
                    'subject': u,
                    'subject_name': self.entities[u]['name'],
                    'predicate': predicate,
                    'object': v,
                    'object_name': self.entities[v]['name']
                })

        return results

    def get_entities_by_type(self, entity_type: str) -> List[Dict]:
        """获取指定类型的所有实体"""
        results = []
        for entity_id, entity_data in self.entities.items():
            if entity_data['type'] == entity_type:
                results.append(entity_data)
        return results

    def get_shortest_path(self, start_id: str, end_id: str) -> List:
        """计算两个实体间的最短路径"""
        try:
            path = nx.shortest_path(self.graph, start_id, end_id)
            return path
        except nx.NetworkXNoPath:
            return None

    def get_neighbors(self, entity_id: str, depth: int = 1) -> Dict:
        """获取实体的邻居（指定深度）"""
        if entity_id not in self.graph:
            return {}

        neighbors = {}
        visited = {entity_id}
        current_level = {entity_id}

        for d in range(depth):
            next_level = set()
            for node in current_level:
                # 出边邻居
                for neighbor in self.graph.successors(node):
                    if neighbor not in visited:
                        next_level.add(neighbor)
                        visited.add(neighbor)
                        if neighbor not in neighbors:
                            neighbors[neighbor] = {
                                'entity': self.entities[neighbor],
                                'depth': d + 1
                            }

                # 入边邻居
                for neighbor in self.graph.predecessors(node):
                    if neighbor not in visited:
                        next_level.add(neighbor)
                        visited.add(neighbor)
                        if neighbor not in neighbors:
                            neighbors[neighbor] = {
                                'entity': self.entities[neighbor],
                                'depth': d + 1
                            }

            current_level = next_level

        return neighbors

    def get_statistics(self) -> Dict:
        """获取图谱统计信息"""
        stats = {
            'total_entities': len(self.entities),
            'total_relations': self.graph.number_of_edges(),
            'entity_types': {},
            'relation_types': {}
        }

        # 统计实体类型
        for entity_data in self.entities.values():
            entity_type = entity_data['type']
            stats['entity_types'][entity_type] = stats['entity_types'].get(
                entity_type, 0) + 1

        # 统计关系类型
        for u, v, data in self.graph.edges(data=True):
            relation = data['relation']
            stats['relation_types'][relation] = stats['relation_types'].get(
                relation, 0) + 1

        return stats
