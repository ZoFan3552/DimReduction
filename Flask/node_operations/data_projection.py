from flask import Flask, request, jsonify, Blueprint
import numpy as np
import uuid

from matplotlib import pyplot as plt
from scipy.stats import zscore

projection_api = Blueprint('projection_api', __name__)


@projection_api.route('/api/projection', methods=['POST'])
def perform_projection():
    try:
        data = request.json

        # 获取请求参数
        matrix_type = data.get('matrix_type')
        matrix_label = data.get('matrix_label')
        eigenvectors = np.array(data.get('eigenvectors', []))
        eigenvalues = np.array(data.get('eigenvalues', []))
        standardize = data.get('standardize', True)
        output_dimension = data.get('outputDimension', 2)
        node_data = data.get('nodeData', {})

        # 验证输入数据
        if not matrix_type or len(eigenvectors) == 0:
            return jsonify({
                'success': False,
                'message': '缺少必要的投影参数'
            })

        # 获取原始数据集
        dataset = np.array(node_data.get('dataset', []))
        feature_names = node_data.get('feature_names', [])
        target = node_data.get('target', [])
        target_names = node_data.get('target_names', [])

        if dataset.size == 0:
            return jsonify({
                'success': False,
                'message': '数据集为空'
            })

        # 数据预处理
        X = dataset.copy()

        # 标准化处理
        if standardize:
            X = zscore(X, axis=0)

        # 选择指定的特征向量
        selected_eigenvectors = eigenvectors[:output_dimension].T
        print("特征向量矩阵",selected_eigenvectors)
        # 执行投影
        projected_data = np.dot(X, selected_eigenvectors)
        # print("投影后的数据集",projected_data)

        # x1 = projected_data[:, 0]
        # x2 = projected_data[:, 1]
        #
        # # 绘制散点图
        # plt.figure(figsize=(6, 5))
        # plt.scatter(x1, x2, c='blue', alpha=0.6, edgecolors='k')
        # plt.xlabel('Feature 1')
        # plt.ylabel('Feature 2')
        # plt.title('2D Scatter Plot of Dataset X')
        # plt.grid(True)
        # plt.show()

        # 构建新的特征名称
        new_feature_names = [f'{matrix_label}_投影_{i + 1}' for i in range(output_dimension)]

        # 创建新节点
        new_node = {
            'id': str(uuid.uuid4()),
            'selected': False,
            'operation': f'{matrix_label}投影 ({output_dimension}维)',
            'parameters': {
                'matrix_type': matrix_type,
                'matrix_label': matrix_label,
                'standardize': standardize,
                'output_dimension': output_dimension,
                'selected_eigenvector_indices': list(range(len(eigenvectors)))
            },
            'target_names': target_names,
            'target': target,
            'feature_names': new_feature_names,
            'dataset': projected_data.tolist(),
            'computed': {
                'projection_info': {
                    'original_features': feature_names,
                    'original_dimension': len(feature_names),
                    'reduced_dimension': output_dimension,
                    'matrix_type': matrix_type,
                    'matrix_label': matrix_label,
                    'eigenvalues_used': eigenvalues.tolist(),
                    # 'variance_explained': calculate_variance_explained(eigenvalues),
                    'projection_matrix': selected_eigenvectors.tolist()
                }
            },
            'children': []
        }

        # 保留原始的computed信息（供后续分析使用）
        if 'computed' in node_data:
            # 只保留未被使用的矩阵信息
            original_computed = {}
            for key, value in node_data['computed'].items():
                if not key.startswith(matrix_type):
                    original_computed[key] = value

            if original_computed:
                new_node['computed']['original_matrices'] = original_computed

        return jsonify({
            'success': True,
            'node': new_node,
            'message': f'使用{matrix_label}成功完成{output_dimension}维投影'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'投影失败: {str(e)}'
        })


# def calculate_variance_explained(eigenvalues):
#     """计算方差解释率"""
#     total_variance = np.sum(np.abs(eigenvalues))
#     variance_explained = []
#     cumulative = 0
#
#     for i, eigenvalue in enumerate(eigenvalues):
#         percentage = (np.abs(eigenvalue) / total_variance) * 100 if total_variance > 0 else 0
#         cumulative += percentage
#         variance_explained.append({
#             'component': i + 1,
#             'eigenvalue': float(eigenvalue),
#             'variance_ratio': float(percentage),
#             'cumulative_variance_ratio': float(cumulative)
#         })
#
#     return variance_explained


# 额外的API端点，用于获取矩阵信息
# @projection_api.route('/api/matrix-info', methods=['POST'])
# def get_matrix_info():
#     """获取指定节点的矩阵信息摘要"""
#     try:
#         data = request.json
#         node_data = data.get('nodeData', {})
#
#         if not node_data or 'computed' not in node_data:
#             return jsonify({
#                 'success': False,
#                 'message': '节点数据不完整'
#             })
#
#         computed = node_data['computed']
#         matrix_info = {
#             'available_matrices': [],
#             'summary': {}
#         }
#
#         # 检查各种矩阵的存在性
#         matrix_types = [
#             ('covariance', '协方差矩阵'),
#             ('within_class_scatter', '类内散度矩阵'),
#             ('between_class_scatter', '类间散度矩阵'),
#             ('lda', 'LDA广义特征向量')
#         ]
#
#         for matrix_type, matrix_label in matrix_types:
#             eigenvectors_key = f'{matrix_type}_eigenvectors'
#             eigenvalues_key = f'{matrix_type}_eigenvalues'
#
#             if eigenvectors_key in computed and eigenvalues_key in computed:
#                 eigenvalues = np.array(computed[eigenvalues_key])
#                 eigenvectors = np.array(computed[eigenvectors_key])
#
#                 matrix_info['available_matrices'].append({
#                     'type': matrix_type,
#                     'label': matrix_label,
#                     'dimensions': len(eigenvalues),
#                     'rank': np.linalg.matrix_rank(eigenvectors),
#                     'condition_number': np.linalg.cond(eigenvectors) if len(eigenvectors) > 0 else float('inf')
#                 })
#
#                 # 计算该矩阵的摘要信息
#                 matrix_info['summary'][matrix_type] = {
#                     'total_variance': float(np.sum(np.abs(eigenvalues))),
#                     'max_eigenvalue': float(np.max(np.abs(eigenvalues))),
#                     'min_eigenvalue': float(np.min(np.abs(eigenvalues))),
#                     'variance_explained': calculate_variance_explained(eigenvalues)
#                 }
#
#         return jsonify({
#             'success': True,
#             'matrix_info': matrix_info
#         })
#
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'获取矩阵信息失败: {str(e)}'
#         })

