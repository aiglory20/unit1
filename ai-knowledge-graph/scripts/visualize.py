#!/usr/bin/env python3
"""
知识图谱可视化脚本
生成知识图谱的可视化图像
"""

from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from kg_core import KnowledgeGraph
import matplotlib
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# 设置matplotlib使用非交互式后端
matplotlib.use('Agg')


# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans',
                                          'SimHei', 'WenQuanYi Micro Hei']
matplotlib.rcParams['axes.unicode_minus'] = False


def visualize_subgraph(kg, center_entity_id, depth=2, output_file='viz_subgraph.png'):
    """可视化以某实体为中心的子图"""
    center_entity = kg.get_entity_by_id(center_entity_id)
    print(f"正在生成以 '{center_entity['name']}' 为中心的子图...")

    # 获取邻居节点
    neighbors = kg.get_neighbors(center_entity_id, depth=depth)
    node_ids = [center_entity_id] + list(neighbors.keys())

    # 创建子图
    subgraph = kg.graph.subgraph(node_ids)

    # 设置布局
    pos = nx.spring_layout(subgraph, k=2, iterations=50)

    # 设置节点颜色（按类型）
    type_colors = {
        'AI_Field': '#FF6B6B',
        'Algorithm': '#4ECDC4',
        'Model': '#45B7D1',
        'Technique': '#FFA07A',
        'Application': '#98D8C8',
        'Person': '#F7DC6F',
        'Organization': '#BB8FCE',
        'Tool': '#85C1E2',
        'Concept': '#F8B500'
    }

    node_colors = []
    for node_id in subgraph.nodes():
        entity = kg.get_entity_by_id(node_id)
        node_colors.append(type_colors.get(entity['type'], '#CCCCCC'))

    # 绘制图形
    plt.figure(figsize=(20, 15))

    # 绘制节点
    nx.draw_networkx_nodes(subgraph, pos,
                           node_color=node_colors,
                           node_size=1000,
                           alpha=0.9)

    # 绘制边
    nx.draw_networkx_edges(subgraph, pos,
                           edge_color='gray',
                           alpha=0.5,
                           arrows=True,
                           arrowsize=20,
                           arrowstyle='->',
                           connectionstyle='arc3,rad=0.1')

    # 绘制标签
    labels = {}
    for node_id in subgraph.nodes():
        entity = kg.get_entity_by_id(node_id)
        labels[node_id] = entity['name']

    nx.draw_networkx_labels(subgraph, pos, labels,
                            font_size=8,
                            font_weight='bold')

    # 绘制边标签
    edge_labels = {}
    for u, v, data in subgraph.edges(data=True):
        edge_labels[(u, v)] = data['relation']

    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels,
                                 font_size=6,
                                 alpha=0.7)

    plt.title(f"AI知识图谱子图：以'{center_entity['name']}'为中心（深度={depth}）",
              fontsize=16, fontweight='bold', pad=20)

    # 添加图例
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=color, markersize=10, label=type_name)
                       for type_name, color in type_colors.items()]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 子图已保存：{output_file}")
    plt.close()


def visualize_entity_type_distribution(kg, output_file='viz_entity_types.png'):
    """可视化实体类型分布"""
    print("正在生成实体类型分布图...")

    stats = kg.get_statistics()

    # 准备数据
    types = list(stats['entity_types'].keys())
    counts = list(stats['entity_types'].values())

    # 创建柱状图
    plt.figure(figsize=(12, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
              '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B500']

    bars = plt.bar(types, counts, color=colors[:len(
        types)], alpha=0.8, edgecolor='black')

    # 在柱子上显示数值
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xlabel('实体类型', fontsize=12, fontweight='bold')
    plt.ylabel('数量', fontsize=12, fontweight='bold')
    plt.title('AI知识图谱 - 实体类型分布', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 实体类型分布图已保存：{output_file}")
    plt.close()


def visualize_relation_type_distribution(kg, output_file='viz_relation_types.png'):
    """可视化关系类型分布"""
    print("正在生成关系类型分布图...")

    stats = kg.get_statistics()

    # 准备数据
    relations = list(stats['relation_types'].keys())
    counts = list(stats['relation_types'].values())

    # 按数量排序
    sorted_data = sorted(zip(relations, counts),
                         key=lambda x: x[1], reverse=True)
    relations, counts = zip(*sorted_data)

    # 创建水平柱状图
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(range(len(relations)))

    bars = plt.barh(relations, counts, color=colors,
                    alpha=0.8, edgecolor='black')

    # 在柱子上显示数值
    for i, (bar, count) in enumerate(zip(bars, counts)):
        plt.text(count + 1, i, f'{count}',
                 va='center', fontsize=10, fontweight='bold')

    plt.xlabel('数量', fontsize=12, fontweight='bold')
    plt.ylabel('关系类型', fontsize=12, fontweight='bold')
    plt.title('AI知识图谱 - 关系类型分布', fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 关系类型分布图已保存：{output_file}")
    plt.close()


def visualize_timeline(kg, output_file='viz_timeline.png'):
    """可视化AI发展时间线"""
    print("正在生成AI发展时间线...")

    # 收集有年份信息的实体
    timeline_data = defaultdict(list)

    for entity_id, entity in kg.entities.items():
        if 'year' in entity and entity['year']:
            try:
                year = int(entity['year'])
                if 1900 <= year <= 2025:
                    timeline_data[year].append(entity)
            except:
                pass

    if not timeline_data:
        print("没有足够的时间线数据")
        return

    # 创建时间线图
    plt.figure(figsize=(16, 10))

    years = sorted(timeline_data.keys())
    y_pos = 0
    year_positions = {}

    for year in years:
        entities = timeline_data[year]
        year_positions[year] = y_pos

        for i, entity in enumerate(entities[:3]):  # 每年最多显示3个
            plt.scatter(year, y_pos + i*0.3, s=100, alpha=0.7)
            plt.text(year + 0.5, y_pos + i*0.3, entity['name'],
                     fontsize=7, va='center')

        y_pos += 1

    plt.xlabel('年份', fontsize=12, fontweight='bold')
    plt.title('AI技术发展时间线', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 时间线图已保存：{output_file}")
    plt.close()


def main():
    """主函数"""
    print("="*70)
    print("知识图谱可视化系统")
    print("="*70)

    # 加载知识图谱
    print("\n加载知识图谱...")
    kg = KnowledgeGraph()
    kg.load('database/knowledge_graph.pkl')

    # 生成各种可视化
    print("\n开始生成可视化...")

    # 1. 实体类型分布
    visualize_entity_type_distribution(kg, 'viz_entity_types.png')

    # 2. 关系类型分布
    visualize_relation_type_distribution(kg, 'viz_relation_types.png')

    # 3. 时间线
    visualize_timeline(kg, 'viz_timeline.png')

    # 4. 子图可视化 - 以深度学习为中心
    dl = kg.get_entity_by_name('深度学习')
    if dl:
        visualize_subgraph(kg, dl['id'], depth=1,
                           output_file='viz_deeplearning_subgraph.png')

    # 5. 子图可视化 - 以GPT为中心
    gpt = kg.get_entity_by_name('GPT')
    if gpt:
        visualize_subgraph(kg, gpt['id'], depth=1,
                           output_file='viz_gpt_subgraph.png')

    print("\n" + "="*70)
    print("✓ 所有可视化已生成")
    print("="*70)
    print("\n生成的文件：")
    print("  • viz_entity_types.png - 实体类型分布")
    print("  • viz_relation_types.png - 关系类型分布")
    print("  • viz_timeline.png - AI发展时间线")
    print("  • viz_deeplearning_subgraph.png - 深度学习领域子图")
    print("  • viz_gpt_subgraph.png - GPT相关子图")
    print("="*70)


if __name__ == '__main__':
    main()
