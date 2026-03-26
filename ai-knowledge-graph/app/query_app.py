#!/usr/bin/env python3
"""
知识图谱查询应用
提供实体检索、关系查询等功能
"""

from kg_core import KnowledgeGraph
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class KGQueryApp:
    """知识图谱查询应用类"""

    def __init__(self, kg_file: str):
        self.kg = KnowledgeGraph()
        print("正在加载知识图谱...")
        self.kg.load(kg_file)
        print("✓ 知识图谱加载成功\n")

    def display_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("AI知识图谱查询系统")
        print("="*60)
        print("1. 实体搜索（关键词搜索）")
        print("2. 查看实体详情")
        print("3. 查询实体关系")
        print("4. 按关系类型查询")
        print("5. 按实体类型查询")
        print("6. 查找实体间路径")
        print("7. 查看图谱统计")
        print("0. 退出")
        print("="*60)

    def search_entities(self):
        """实体搜索"""
        keyword = input("请输入搜索关键词：").strip()
        results = self.kg.search_entity(keyword)

        if results:
            print(f"\n找到 {len(results)} 个匹配的实体：")
            print("-"*60)
            for i, entity in enumerate(results[:20], 1):  # 限制显示前20个
                print(
                    f"{i}. [{entity['id']}] {entity['name']} ({entity['type']})")
                if 'description' in entity:
                    print(f"   描述：{entity['description'][:80]}...")
                if 'year' in entity:
                    print(f"   年份：{entity['year']}")
                print()
        else:
            print("未找到匹配的实体")

    def view_entity_details(self):
        """查看实体详情"""
        entity_input = input("请输入实体ID或名称：").strip()

        # 尝试按ID查找
        entity = self.kg.get_entity_by_id(entity_input)
        if not entity:
            # 尝试按名称查找
            entity = self.kg.get_entity_by_name(entity_input)

        if entity:
            print("\n" + "="*60)
            print(f"实体详情：{entity['name']}")
            print("="*60)
            print(f"ID：{entity['id']}")
            print(f"类型：{entity['type']}")
            if 'description' in entity:
                print(f"描述：{entity['description']}")
            if 'year' in entity:
                print(f"年份：{entity['year']}")
            for key, value in entity.items():
                if key not in ['id', 'name', 'type', 'description', 'year']:
                    print(f"{key}：{value}")

            # 显示关系
            relations = self.kg.get_relations(entity['id'])
            if relations['outgoing']:
                print(f"\n【出边关系】（{entity['name']} 作为主语）：")
                for rel in relations['outgoing'][:10]:
                    print(
                        f"  → {rel['predicate']} → {rel['object_name']} ({rel['object']})")

            if relations['incoming']:
                print(f"\n【入边关系】（{entity['name']} 作为宾语）：")
                for rel in relations['incoming'][:10]:
                    print(
                        f"  ← {rel['predicate']} ← {rel['subject_name']} ({rel['subject']})")

        else:
            print("未找到该实体")

    def query_entity_relations(self):
        """查询实体关系"""
        entity_input = input("请输入实体ID或名称：").strip()

        # 尝试按ID查找
        entity = self.kg.get_entity_by_id(entity_input)
        if not entity:
            # 尝试按名称查找
            entity = self.kg.get_entity_by_name(entity_input)

        if entity:
            relations = self.kg.get_relations(entity['id'])

            print(f"\n实体：{entity['name']} ({entity['id']})")
            print("-"*60)

            if relations['outgoing']:
                print(f"\n作为主语的关系（共{len(relations['outgoing'])}个）：")
                for rel in relations['outgoing']:
                    print(
                        f"  {entity['name']} --[{rel['predicate']}]--> {rel['object_name']}")

            if relations['incoming']:
                print(f"\n作为宾语的关系（共{len(relations['incoming'])}个）：")
                for rel in relations['incoming']:
                    print(
                        f"  {rel['subject_name']} --[{rel['predicate']}]--> {entity['name']}")

            if not relations['outgoing'] and not relations['incoming']:
                print("该实体没有关系")

        else:
            print("未找到该实体")

    def query_by_relation_type(self):
        """按关系类型查询"""
        print("可用的关系类型：")
        relation_types = ['belongsTo', 'usesAlgorithm', 'basedon', 'developedBy',
                          'appliedIn', 'usesTool', 'relatedTo', 'isPartOf',
                          'worksAt', 'proposes']
        for i, rel_type in enumerate(relation_types, 1):
            print(f"{i}. {rel_type}")

        relation = input("\n请输入关系类型：").strip()
        results = self.kg.query_by_relation(relation)

        if results:
            print(f"\n找到 {len(results)} 个 [{relation}] 关系：")
            print("-"*60)
            for i, triple in enumerate(results[:30], 1):  # 限制显示前30个
                print(
                    f"{i}. {triple['subject_name']} --[{triple['predicate']}]--> {triple['object_name']}")
        else:
            print(f"未找到 [{relation}] 关系")

    def query_by_entity_type(self):
        """按实体类型查询"""
        print("可用的实体类型：")
        entity_types = ['AI_Field', 'Algorithm', 'Model', 'Technique',
                        'Application', 'Person', 'Organization', 'Tool', 'Concept']
        for i, ent_type in enumerate(entity_types, 1):
            print(f"{i}. {ent_type}")

        entity_type = input("\n请输入实体类型：").strip()
        results = self.kg.get_entities_by_type(entity_type)

        if results:
            print(f"\n找到 {len(results)} 个 [{entity_type}] 类型的实体：")
            print("-"*60)
            for i, entity in enumerate(results, 1):
                print(f"{i}. {entity['name']} ({entity['id']})")
                if 'year' in entity:
                    print(f"   年份：{entity['year']}")
        else:
            print(f"未找到 [{entity_type}] 类型的实体")

    def find_path(self):
        """查找两个实体间的路径"""
        start_input = input("请输入起始实体ID或名称：").strip()
        end_input = input("请输入目标实体ID或名称：").strip()

        # 查找实体
        start_entity = self.kg.get_entity_by_id(start_input)
        if not start_entity:
            start_entity = self.kg.get_entity_by_name(start_input)

        end_entity = self.kg.get_entity_by_id(end_input)
        if not end_entity:
            end_entity = self.kg.get_entity_by_name(end_input)

        if not start_entity:
            print(f"未找到起始实体：{start_input}")
            return
        if not end_entity:
            print(f"未找到目标实体：{end_input}")
            return

        path = self.kg.get_shortest_path(start_entity['id'], end_entity['id'])

        if path:
            print(f"\n找到从 {start_entity['name']} 到 {end_entity['name']} 的路径：")
            print("-"*60)
            for i, entity_id in enumerate(path):
                entity = self.kg.get_entity_by_id(entity_id)
                print(f"{i+1}. {entity['name']} ({entity['type']})")
                if i < len(path) - 1:
                    # 显示连接关系
                    next_id = path[i+1]
                    edge_data = self.kg.graph.get_edge_data(entity_id, next_id)
                    if edge_data:
                        relation = list(edge_data.values())[0]['relation']
                        print(f"    ↓ [{relation}]")
        else:
            print(f"未找到从 {start_entity['name']} 到 {end_entity['name']} 的路径")

    def show_statistics(self):
        """显示图谱统计"""
        stats = self.kg.get_statistics()

        print("\n" + "="*60)
        print("知识图谱统计信息")
        print("="*60)
        print(f"实体总数：{stats['total_entities']}")
        print(f"关系总数：{stats['total_relations']}")

        print("\n实体类型分布：")
        for entity_type, count in sorted(stats['entity_types'].items()):
            print(f"  {entity_type}: {count}")

        print("\n关系类型分布：")
        for relation_type, count in sorted(stats['relation_types'].items()):
            print(f"  {relation_type}: {count}")
        print("="*60)

    def run(self):
        """运行应用"""
        while True:
            self.display_menu()
            choice = input("\n请选择操作（0-7）：").strip()

            try:
                if choice == '0':
                    print("\n感谢使用！再见！")
                    break
                elif choice == '1':
                    self.search_entities()
                elif choice == '2':
                    self.view_entity_details()
                elif choice == '3':
                    self.query_entity_relations()
                elif choice == '4':
                    self.query_by_relation_type()
                elif choice == '5':
                    self.query_by_entity_type()
                elif choice == '6':
                    self.find_path()
                elif choice == '7':
                    self.show_statistics()
                else:
                    print("无效选择，请重新输入")
            except KeyboardInterrupt:
                print("\n\n操作已取消")
            except Exception as e:
                print(f"\n错误：{e}")

            input("\n按回车键继续...")


if __name__ == '__main__':
    # 检查知识图谱文件是否存在
    kg_file = 'database/knowledge_graph.pkl'
    if not os.path.exists(kg_file):
        print("知识图谱文件不存在，请先运行：python3 scripts/load_knowledge_graph.py")
        sys.exit(1)

    app = KGQueryApp(kg_file)
    app.run()
