#!/usr/bin/env python3
"""
知识图谱功能演示脚本
展示核心功能和典型应用场景
"""

import sys
import os

# 首先修改 sys.path，然后才能导入 kg_core
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from kg_core import KnowledgeGraph


def demo_intro():
    """演示介绍"""
    print("="*70)
    print(" "*20 + "AI知识图谱系统演示")
    print("="*70)
    print("\n本系统构建了一个人工智能核心概念知识图谱")
    print("包含272个实体和358个关系三元组")
    print("\n涵盖的内容：")
    print("  • AI领域：机器学习、深度学习、NLP、计算机视觉等")
    print("  • 算法与模型：神经网络、Transformer、GPT、BERT等")
    print("  • 技术方法：迁移学习、强化学习、注意力机制等")
    print("  • 应用场景：语音识别、图像分类、机器翻译等")
    print("  • 人物与组织：Hinton、LeCun、OpenAI、DeepMind等")
    print("  • 工具框架：TensorFlow、PyTorch、Keras等")
    print("="*70)


def demo_entity_search(kg):
    """演示1：实体搜索"""
    print("\n" + "="*70)
    print("【演示1：实体搜索 - 关键词检索】")
    print("="*70)

    examples = [
        ("GPT", "搜索大语言模型"),
        ("深度学习", "搜索AI领域"),
        ("Hinton", "搜索AI先驱")
    ]

    for keyword, desc in examples:
        print(f"\n{desc}（关键词：{keyword}）")
        print("-"*70)
        results = kg.search_entity(keyword)
        print(f"找到 {len(results)} 个匹配结果：\n")

        for i, entity in enumerate(results[:5], 1):
            print(f"{i}. {entity['name']} ({entity['type']})")
            if 'description' in entity:
                print(f"   描述：{entity['description'][:60]}...")
            if 'year' in entity:
                print(f"   年份：{entity['year']}")
            print()


def demo_relation_exploration(kg):
    """演示2：关系探索"""
    print("\n" + "="*70)
    print("【演示2：关系探索 - 查看实体的关系网络】")
    print("="*70)

    # 示例：探索GPT模型
    entity = kg.get_entity_by_name('GPT')
    print(f"\n探索实体：{entity['name']}")
    print(f"类型：{entity['type']}")
    print(f"描述：{entity['description']}")
    print(f"提出年份：{entity['year']}")

    relations = kg.get_relations(entity['id'])

    print(f"\n【出边关系】（{entity['name']} 作为主语）：")
    print("-"*70)
    for rel in relations['outgoing']:
        print(
            f"  {entity['name']} --[{rel['predicate']}]--> {rel['object_name']}")

    print(f"\n【入边关系】（{entity['name']} 作为宾语）：")
    print("-"*70)
    for rel in relations['incoming']:
        print(
            f"  {rel['subject_name']} --[{rel['predicate']}]--> {entity['name']}")


def demo_relation_query(kg):
    """演示3：关系查询"""
    print("\n" + "="*70)
    print("【演示3：按关系类型查询 - 发现特定模式】")
    print("="*70)

    # 场景1：查找所有基于Transformer的模型
    print("\n场景1：查找所有基于Transformer的模型")
    print("-"*70)
    transformer = kg.get_entity_by_name('Transformer')
    results = kg.query_by_relation('basedon', obj=transformer['id'])
    print(f"找到 {len(results)} 个基于Transformer的技术：\n")
    for i, triple in enumerate(results[:10], 1):
        subject = kg.get_entity_by_id(triple['subject'])
        print(
            f"{i}. {triple['subject_name']} ({subject['type']}) - {subject.get('year', 'N/A')}")

    # 场景2：查找OpenAI开发的所有产品
    print("\n\n场景2：查找OpenAI开发的所有产品")
    print("-"*70)
    openai = kg.get_entity_by_name('OpenAI')
    results = kg.query_by_relation('developedBy', obj=openai['id'])
    print(f"找到 {len(results)} 个OpenAI开发的产品：\n")
    for i, triple in enumerate(results, 1):
        subject = kg.get_entity_by_id(triple['subject'])
        print(
            f"{i}. {triple['subject_name']} ({subject['type']}) - {subject.get('year', 'N/A')}")


def demo_type_query(kg):
    """演示4：类型查询"""
    print("\n" + "="*70)
    print("【演示4：按类型查询 - 分类浏览】")
    print("="*70)

    # 查看所有AI领域
    print("\n所有AI研究领域：")
    print("-"*70)
    fields = kg.get_entities_by_type('AI_Field')
    for i, field in enumerate(fields, 1):
        print(f"{i}. {field['name']} ({field.get('year', 'N/A')})")
        print(f"   {field['description'][:70]}...")

    # 查看重要人物
    print("\n\nAI领域重要人物（TOP 10）：")
    print("-"*70)
    persons = kg.get_entities_by_type('Person')
    for i, person in enumerate(persons[:10], 1):
        print(f"{i}. {person['name']} ({person.get('nationality', 'N/A')})")
        print(f"   领域：{person.get('field', 'N/A')}")
        print(f"   {person['description']}")
        print()


def demo_application_analysis(kg):
    """演示5：应用场景分析"""
    print("\n" + "="*70)
    print("【演示5：应用场景分析 - 技术到应用的映射】")
    print("="*70)

    # 分析计算机视觉相关的应用
    print("\n计算机视觉相关的应用场景：")
    print("-"*70)
    cv_field = kg.get_entity_by_name('计算机视觉')
    applications = kg.get_entities_by_type('Application')

    cv_apps = []
    for app in applications:
        relations = kg.get_relations(app['id'])
        for rel in relations['outgoing']:
            if rel['object'] == cv_field['id'] and rel['predicate'] == 'appliedIn':
                cv_apps.append(app)
                break

        # 反向查找：哪些模型应用于此
        for rel in relations['incoming']:
            if rel['predicate'] == 'appliedIn':
                subject = kg.get_entity_by_id(rel['subject'])
                if subject and 'belongsTo' in [r['predicate'] for r in kg.get_relations(subject['id'])['outgoing']]:
                    # 检查是否属于计算机视觉
                    for r in kg.get_relations(subject['id'])['outgoing']:
                        if r['predicate'] == 'belongsTo' and r['object'] == cv_field['id']:
                            if app not in cv_apps:
                                cv_apps.append(app)

    # 获取所有应用于计算机视觉领域的应用
    cv_relations = kg.query_by_relation('appliedIn')
    cv_app_ids = set()
    for rel in cv_relations:
        obj_entity = kg.get_entity_by_id(rel['object'])
        if obj_entity and obj_entity['type'] == 'Application':
            # 检查这个应用是否与计算机视觉相关
            app_rels = kg.get_relations(rel['object'])
            for app_rel in app_rels['incoming']:
                subj = kg.get_entity_by_id(app_rel['subject'])
                if subj:
                    subj_rels = kg.get_relations(subj['id'])
                    for sr in subj_rels['outgoing']:
                        if sr['object'] == cv_field['id']:
                            cv_app_ids.add(rel['object'])

    # 显示与计算机视觉相关的应用
    for app_id in list(cv_app_ids)[:10]:
        app = kg.get_entity_by_id(app_id)
        if app:
            print(f"\n• {app['name']}")
            print(f"  {app['description']}")

            # 显示使用的技术
            app_rels = kg.get_relations(app_id)
            techniques = [rel['subject_name'] for rel in app_rels['incoming']
                          if rel['predicate'] in ['appliedIn', 'usesAlgorithm']]
            if techniques:
                print(f"  使用的技术：{', '.join(techniques[:5])}")


def demo_knowledge_reasoning(kg):
    """演示6：知识推理"""
    print("\n" + "="*70)
    print("【演示6：知识推理 - 基于关系的推理】")
    print("="*70)

    # 推理1：找出深度学习的技术栈
    print("\n推理1：深度学习的完整技术栈")
    print("-"*70)
    dl = kg.get_entity_by_name('深度学习')

    print(f"深度学习体系：\n")

    # 查找属于深度学习的算法
    dl_algorithms = kg.query_by_relation('belongsTo', obj=dl['id'])
    print(f"核心算法（{len(dl_algorithms)}个）：")
    for i, triple in enumerate(dl_algorithms[:8], 1):
        algo = kg.get_entity_by_id(triple['subject'])
        print(f"  {i}. {triple['subject_name']} ({algo.get('year', 'N/A')})")

    # 查找基于深度学习的模型
    dl_models = []
    models = kg.get_entities_by_type('Model')
    for model in models:
        rels = kg.get_relations(model['id'])
        for rel in rels['outgoing']:
            if rel['object'] == dl['id'] and rel['predicate'] == 'belongsTo':
                dl_models.append(model)
                break

    # 推理2：技术演进路径
    print("\n\n推理2：神经网络的技术演进")
    print("-"*70)
    nn = kg.get_entity_by_name('神经网络')

    # 查找基于神经网络的技术
    evolution = kg.query_by_relation('basedon', obj=nn['id'])
    print(f"基于神经网络发展的技术（{len(evolution)}个）：\n")
    for i, triple in enumerate(evolution[:10], 1):
        tech = kg.get_entity_by_id(triple['subject'])
        print(f"{i}. {triple['subject_name']} ({tech.get('year', 'N/A')})")


def demo_domain_experts(kg):
    """演示7：领域专家识别"""
    print("\n" + "="*70)
    print("【演示7：领域专家识别 - 人物与贡献】")
    print("="*70)

    persons = kg.get_entities_by_type('Person')

    print(f"\n发现 {len(persons)} 位AI领域专家：\n")

    for person in persons:
        print(f"• {person['name']} ({person.get('nationality', 'N/A')})")
        print(f"  研究领域：{person.get('field', 'N/A')}")
        print(f"  简介：{person['description']}")

        # 查找贡献
        rels = kg.get_relations(person['id'])
        contributions = [rel for rel in rels['outgoing']
                         if rel['predicate'] == 'proposes']
        if contributions:
            print(f"  主要贡献：", end='')
            print(', '.join([rel['object_name'] for rel in contributions]))

        # 查找开发的产品
        developed = [rel for rel in rels['incoming']
                     if rel['predicate'] == 'developedBy']
        if developed:
            print(f"  开发产品：", end='')
            print(', '.join([rel['subject_name'] for rel in developed[:3]]))

        # 查找工作单位
        work_places = [rel for rel in rels['outgoing']
                       if rel['predicate'] == 'worksAt']
        if work_places:
            print(f"  工作单位：", end='')
            print(', '.join([rel['object_name'] for rel in work_places]))

        print()


def demo_tool_ecosystem(kg):
    """演示8：工具生态分析"""
    print("\n" + "="*70)
    print("【演示8：工具生态分析 - AI开发工具链】")
    print("="*70)

    tools = kg.get_entities_by_type('Tool')

    print(f"\n发现 {len(tools)} 个AI开发工具：\n")

    # 按年份排序
    tools_sorted = sorted(tools, key=lambda x: x.get('year', '9999'))

    for tool in tools_sorted:
        print(f"• {tool['name']} ({tool.get('year', 'N/A')})")
        print(f"  {tool['description']}")

        # 查找开发者
        rels = kg.get_relations(tool['id'])
        developers = [rel for rel in rels['outgoing']
                      if rel['predicate'] == 'developedBy']
        if developers:
            print(
                f"  开发者：{', '.join([rel['object_name'] for rel in developers])}")

        print()


def demo_statistics_analysis(kg):
    """演示9：统计分析"""
    print("\n" + "="*70)
    print("【演示9：统计分析 - 知识图谱全局视图】")
    print("="*70)

    stats = kg.get_statistics()

    print("\n✓ 核心指标：")
    print(f"  • 实体总数：{stats['total_entities']} （要求≥200）")
    print(f"  • 关系总数：{stats['total_relations']} （要求≥300）")

    print("\n✓ 实体类型分布：")
    for entity_type, count in sorted(stats['entity_types'].items(),
                                     key=lambda x: x[1], reverse=True):
        bar = '█' * (count // 5)
        print(f"  {entity_type:15s}: {count:3d} {bar}")

    print("\n✓ 关系类型分布：")
    for relation_type, count in sorted(stats['relation_types'].items(),
                                       key=lambda x: x[1], reverse=True):
        bar = '█' * (count // 5)
        print(f"  {relation_type:15s}: {count:3d} {bar}")


def demo_use_cases(kg):
    """演示10：典型应用场景"""
    print("\n" + "="*70)
    print("【演示10：典型应用场景】")
    print("="*70)

    print("\n场景1：我想开发一个图像分类应用，应该使用什么技术？")
    print("-"*70)
    image_classification = kg.get_entity_by_name('图像分类')
    rels = kg.get_relations(image_classification['id'])

    print("\n推荐的模型和算法：")
    for rel in rels['incoming']:
        if rel['predicate'] == 'appliedIn':
            model = kg.get_entity_by_id(rel['subject'])
            print(f"  • {rel['subject_name']} ({model.get('year', 'N/A')})")

    print("\n\n场景2：学习自然语言处理，应该了解哪些核心概念？")
    print("-"*70)
    nlp = kg.get_entity_by_name('自然语言处理')

    # 查找属于NLP的技术
    nlp_tech = kg.query_by_relation('belongsTo', obj=nlp['id'])
    print(f"\n核心算法和模型（共{len(nlp_tech)}个）：")
    for i, triple in enumerate(nlp_tech[:10], 1):
        tech = kg.get_entity_by_id(triple['subject'])
        print(
            f"  {i}. {triple['subject_name']} ({tech['type']}, {tech.get('year', 'N/A')})")

    # 查找NLP的应用
    nlp_apps = kg.query_by_relation('appliedIn', obj=nlp['id'])
    print(f"\n应用场景（共{len(nlp_apps)}个）：")
    for i, triple in enumerate(nlp_apps[:10], 1):
        print(f"  {i}. {triple['subject_name']}")

    print("\n\n场景3：如果要入门深度学习，应该选择什么框架？")
    print("-"*70)
    tools = kg.get_entities_by_type('Tool')

    print("\n主流深度学习框架：")
    dl_tools = []
    for tool in tools:
        if any(keyword in tool['description'].lower() for keyword in
               ['深度学习', '神经网络', '机器学习框架']):
            dl_tools.append(tool)

    for i, tool in enumerate(dl_tools[:5], 1):
        print(f"  {i}. {tool['name']} ({tool.get('year', 'N/A')})")
        print(f"     {tool['description']}")

        # 查找开发者
        rels = kg.get_relations(tool['id'])
        devs = [rel for rel in rels['outgoing']
                if rel['predicate'] == 'developedBy']
        if devs:
            print(
                f"     开发者：{', '.join([rel['object_name'] for rel in devs])}")
        print()


def run_demo():
    """运行完整演示"""
    # 加载知识图谱
    kg = KnowledgeGraph()
    kg.load('database/knowledge_graph.pkl')

    # 介绍
    demo_intro()
    input("\n按回车键开始演示...")

    # 运行各个演示
    demos = [
        demo_entity_search,
        demo_relation_exploration,
        demo_relation_query,
        demo_type_query,
        demo_application_analysis,
        demo_domain_experts,
        demo_tool_ecosystem,
        demo_statistics_analysis,
        demo_use_cases
    ]

    for i, demo_func in enumerate(demos, 1):
        demo_func(kg)
        if i < len(demos):
            input("\n按回车键继续下一个演示...")

    # 总结
    print("\n" + "="*70)
    print(" "*25 + "演示完成")
    print("="*70)
    print("\n本知识图谱系统展示了：")
    print("  ✓ 完整的知识表示（RDF/OWL规范）")
    print("  ✓ 丰富的实体和关系（272实体，358关系）")
    print("  ✓ 多种查询功能（搜索、关系、类型查询等）")
    print("  ✓ 实际应用场景（技术选型、学习路径等）")
    print("\n您可以运行 'python3 app/query_app.py' 使用交互式查询系统")
    print("="*70)


if __name__ == '__main__':
    run_demo()
