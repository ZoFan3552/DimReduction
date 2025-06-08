from flask import Flask, request, jsonify, Blueprint
from scipy import linalg
import numpy as np
import uuid
import scipy.linalg as linalg
from copy import deepcopy

eigen_api = Blueprint('eigen_api', __name__)

# 矩阵名称中英文映射
MATRIX_NAME_MAPPING = {
    'covariance_matrix': '协方差矩阵',
    'between_class_scatter_matrix': '类间散度矩阵',
    'within_class_scatter_matrix': '类内散度矩阵',
    'correlation_matrix': '相关矩阵',
    'laplacian_matrix': '拉普拉斯矩阵'
}


def get_chinese_name(matrix_name):
    """获取矩阵的中文名称"""
    return MATRIX_NAME_MAPPING.get(matrix_name, matrix_name)


def calculate_and_sort_eigen(matrix_a, matrix_b=None):
    """
    计算并排序特征值和特征向量
    :param matrix_a: 矩阵A
    :param matrix_b: 矩阵B（可选，用于广义特征值问题）
    :return: 排序后的特征值和特征向量
    """
    if matrix_b is None:
        # 标准特征值问题
        if np.allclose(matrix_a, matrix_a.T):
            eigenvalues, eigenvectors = linalg.eigh(matrix_a)
        else:
            eigenvalues, eigenvectors = linalg.eig(matrix_a)
    else:
        # 广义特征值问题
        if np.allclose(matrix_a, matrix_a.T) and np.allclose(matrix_b, matrix_b.T):
            eigenvalues, eigenvectors = linalg.eigh(matrix_a, matrix_b)
        else:
            eigenvalues, eigenvectors = linalg.eig(matrix_a, matrix_b)

    # 按特征值降序排序
    idx = eigenvalues.argsort()[::-1]
    return eigenvalues[idx], eigenvectors[:, idx]


def create_new_node(node_data, operation_name, result_key, eigenvalues, eigenvectors):
    """
    创建新的结果节点
    :param node_data: 原始节点数据
    :param operation_name: 操作名称
    :param result_key: 结果键名
    :param eigenvalues: 特征值
    :param eigenvectors: 特征向量
    :return: 新节点
    """
    new_node = deepcopy(node_data)
    new_node["selected"] = False
    new_node['id'] = str(uuid.uuid4())
    new_node['children'] = []
    new_node['operation'] = operation_name
    new_node['computed'][f'{result_key}_eigenvalues'] = eigenvalues.tolist()
    new_node['computed'][f'{result_key}_eigenvectors'] = eigenvectors.tolist()
    return new_node


@eigen_api.route('/api/calculate-eigen', methods=['POST'])
def calculate_eigen():
    try:
        data = request.json
        node_data = data.get('node_data')
        calculation_type = data.get('calculation_type')

        # 检查节点数据是否有效
        if not node_data or 'computed' not in node_data:
            return jsonify({'error': '无效的节点数据'}), 400

        computed = node_data['computed']

        # 根据计算类型进行不同的处理
        if calculation_type == 'single':
            matrix_name = data.get('matrix_name')
            if matrix_name not in computed:
                return jsonify({'error': f'矩阵 {matrix_name} 在计算数据中未找到'}), 400

            matrix = np.array(computed[matrix_name])
            eigenvalues, eigenvectors = calculate_and_sort_eigen(matrix)

            # 创建新节点
            result_key = matrix_name.replace('_matrix', '')
            operation_name = f"{get_chinese_name(matrix_name)} 特征值分解"
            new_node = create_new_node(
                node_data, operation_name, result_key, eigenvalues, eigenvectors
            )

        elif calculation_type == 'generalized':
            matrix_a_name = data.get('matrix_a_name')
            matrix_b_name = data.get('matrix_b_name')

            if matrix_a_name not in computed or matrix_b_name not in computed:
                return jsonify({'error': '一个或多个矩阵在计算数据中未找到'}), 400

            matrix_a = np.array(computed[matrix_a_name])
            matrix_b = np.array(computed[matrix_b_name])

            try:
                eigenvalues, eigenvectors = calculate_and_sort_eigen(matrix_a, matrix_b)

                # 特殊处理LDA情况
                if matrix_a_name == 'between_class_scatter_matrix' and matrix_b_name == 'within_class_scatter_matrix':
                    operation_name = "LDA 广义特征值分解"
                    result_key = 'lda'
                else:
                    operation_name = f"{get_chinese_name(matrix_a_name)} 和 {get_chinese_name(matrix_b_name)} 广义特征值分解"
                    result_key = f"{matrix_a_name.split('_')[0]}_{matrix_b_name.split('_')[0]}_generalized"

                new_node = create_new_node(
                    node_data, operation_name, result_key, eigenvalues, eigenvectors
                )

            except Exception as e:
                return jsonify({'error': f'广义特征值计算失败: {str(e)}'}), 500

        else:
            return jsonify({'error': '无效的计算类型'}), 400

        # 返回结果
        return jsonify({
            'eigenvalues': eigenvalues.tolist(),
            'eigenvectors': eigenvectors.tolist(),
            'new_node': new_node
        })

    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500