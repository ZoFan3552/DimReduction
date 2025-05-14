from flask import Flask, request, jsonify, Blueprint
import numpy as np
import uuid
import math
from scipy.spatial.distance import pdist, squareform
from umap.umap_ import fuzzy_simplicial_set, nearest_neighbors

calculate_similarity_api = Blueprint('calculate_similarity_api', __name__)


@calculate_similarity_api.route('/calculate-similarity', methods=['POST'])
def calculate_similarity():
    try:
        # 获取请求数据
        data = request.json
        source_node = data.get('source_node')
        formula = data.get('formula')
        parameters = data.get('parameters', {})
        similarity_type = data.get('similarityType', 'high')

        # 验证输入数据
        if not source_node or not formula:
            return jsonify({'success': False, 'message': '缺少必要的参数'})

        # 获取数据集
        dataset = source_node.get('dataset', [])
        if not dataset or len(dataset) == 0:
            return jsonify({'success': False, 'message': '数据集为空'})

        # 确保源节点有computed和parameters字段
        if 'computed' not in source_node:
            source_node['computed'] = {}
        if 'parameters' not in source_node:
            source_node['parameters'] = {}

        # 将数据集转换为numpy数组
        data_array = np.array(dataset)

        # 创建新节点
        new_node = source_node.copy()
        new_node["id"] = str(uuid.uuid4())
        new_node["selected"] = False
        new_node["operation"] = "相似度矩阵计算"
        new_node["parameters"]["similarity_formula"] = formula
        new_node["children"] = []

        # 根据选择的公式计算相似度矩阵
        if similarity_type == 'high':
            # 高维相似度计算
            similarity_matrix = compute_high_dimensional_similarity(data_array, formula, parameters)
            new_node["computed"]["high_similarity_matrix"] = similarity_matrix.tolist()
            # new_node["computed"]["similarity_matrix"] = similarity_matrix.tolist()  # 向后兼容
        else:
            # 低维相似度计算
            similarity_matrix = compute_low_dimensional_similarity(data_array, formula, parameters)
            new_node["computed"]["low_similarity_matrix"] = similarity_matrix.tolist()
            # new_node["computed"]["similarity_matrix"] = similarity_matrix.tolist()  # 向后兼容

        return jsonify({
            'success': True,
            'message': '相似度矩阵计算成功',
            'node': new_node
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'计算过程中出错: {str(e)}'
        })


def compute_high_dimensional_similarity(data, formula, parameters):
    """
    计算高维空间中的相似度矩阵

    参数:
    - data: numpy数组形式的数据集
    - formula: 计算公式名称
    - parameters: 计算参数

    返回:
    - similarity_matrix: 相似度矩阵
    """
    n_samples = data.shape[0]

    if formula == 'euclidean':
        # 欧几里得距离相似度
        sigma = parameters.get('sigma', 1.0)

        # 使用scipy计算欧氏距离矩阵
        distances = squareform(pdist(data, 'euclidean'))

        # 转换为相似度
        similarity_matrix = np.exp(-(distances ** 2) / (2 * (sigma ** 2)))
        np.fill_diagonal(similarity_matrix, 1.0)  # 设置对角线为1

    elif formula == 'cosine':
        # 余弦相似度
        # 数据归一化
        norms = np.linalg.norm(data, axis=1, keepdims=True)
        normalized_data = data / norms

        # 计算余弦相似度
        similarity_matrix = np.dot(normalized_data, normalized_data.T)
        np.fill_diagonal(similarity_matrix, 1.0)  # 确保对角线为1

    elif formula == 'gaussian':
        # 高斯相似度 (条件概率 p_j|i)
        perplexity = parameters.get('perplexity', 30)

        # 使用scipy计算欧氏距离矩阵
        distances = squareform(pdist(data, 'euclidean'))

        # 初始化相似度矩阵
        similarity_matrix = np.zeros((n_samples, n_samples))

        # 为每个点找到合适的sigma_i，使得perplexity达到目标值
        for i in range(n_samples):
            similarity_matrix[i, :] = compute_gaussian_kernel_row(distances[i, :], i, perplexity)

    elif formula == 'symmetric_sne':
        # 对称SNE相似度
        perplexity = parameters.get('perplexity', 30)

        # 首先计算条件概率 p_j|i
        distances = squareform(pdist(data, 'euclidean'))
        conditional_probs = np.zeros((n_samples, n_samples))

        for i in range(n_samples):
            conditional_probs[i, :] = compute_gaussian_kernel_row(distances[i, :], i, perplexity)

        # 对称化: p_ij = (p_j|i + p_i|j) / (2n)
        similarity_matrix = (conditional_probs + conditional_probs.T) / (2 * n_samples)


    elif formula == 'umap_high_similarity':

        # UMAP高维相似度
        n_neighbors = int(parameters.get('n_neighbors', 15))
        min_dist = parameters.get('min_dist', 0.1)
        #
        # # 使用scipy计算欧氏距离矩阵
        # distances = squareform(pdist(data, 'euclidean'))
        #
        # # 初始化相似度矩阵
        # similarity_matrix = np.zeros((n_samples, n_samples))
        #
        # # 定义寻找sigma的函数
        # def find_sigma_umap(distances_i, indices, target_entropy=None):
        #     """
        #     二分查找寻找sigma，使得近邻概率分布的熵约等于log(k)
        #     """
        #     if target_entropy is None:
        #         target_entropy = np.log(len(indices))
        #
        #     def calc_entropy(sigma):
        #         d = distances_i[indices]
        #         p = np.exp(-d / sigma)
        #         p = p / np.sum(p)
        #         return -np.sum(p * np.log(p + 1e-8))
        #
        #     # 二分查找合适的sigma
        #     lo, hi = 0.01, 100.0
        #
        #     for i in range(30):  # 通常30次迭代足够
        #         mid = (lo + hi) / 2
        #         entropy = calc_entropy(mid)
        #         if entropy < target_entropy:
        #             lo = mid
        #         else:
        #             hi = mid
        #
        #     return mid
        #
        # # 对每个点计算相似度
        # for i in range(n_samples):
        #     # 找到k近邻
        #     indices = np.argsort(distances[i, :])[1:n_neighbors + 1]
        #     # 找到适合的sigma_i值，使得概率分布的熵等于log(k)
        #     sigma_i = find_sigma_umap(distances[i, :], indices)
        #     # 计算条件概率 p_j|i
        #     sim_row = np.zeros(n_samples)
        #
        #     for j in range(n_samples):
        #         if i != j:
        #             # 标准UMAP公式: exp(-d_ij / sigma_i)
        #             sim_row[j] = np.exp(-distances[i, j] / sigma_i)
        #
        #     # 归一化，使得概率和为1
        #     sum_p = np.sum(sim_row)
        #
        #     if sum_p > 0:
        #         sim_row = sim_row / sum_p
        #
        #     similarity_matrix[i, :] = sim_row
        #
        # # 计算UMAP特有的相似度矩阵 P_ij = p_j|i + p_i|j - p_j|i * p_i|j
        # P_ij = similarity_matrix + similarity_matrix.T - similarity_matrix * similarity_matrix.T
        # similarity_matrix = P_ij
        similarity_matrix = get_umap_similarity_matrix(data,n_neighbors)

    else:
        raise ValueError(f"未知的高维相似度计算公式: {formula}")

    return similarity_matrix



def get_umap_similarity_matrix(data, n_neighbors=15, metric='euclidean', random_state=42):
    """
    计算UMAP高维相似度矩阵

    参数:
    data: 输入数据，形状为 (n_samples, n_features)
    n_neighbors: 近邻数
    metric: 距离度量方式

    返回:
    similarity_matrix: UMAP高维相似度矩阵
    """
    # 计算近邻图 - 添加缺少的参数
    knn_indices, knn_dists, _ = nearest_neighbors(
        data,
        n_neighbors=n_neighbors,
        metric=metric,
        metric_kwds={},  # 空字典作为默认值
        angular=False,  # 默认为False
        random_state=random_state
    )

    # 计算模糊简单复合集（包含高维相似度信息）
    fuzzy_simp_set, _, _ = fuzzy_simplicial_set(
        X=data,
        n_neighbors=n_neighbors,
        random_state=random_state,
        metric=metric,
        knn_indices=knn_indices,
        knn_dists=knn_dists,
        set_op_mix_ratio=1.0,
        local_connectivity=1.0
    )

    # 转换为密集矩阵
    similarity_matrix = fuzzy_simp_set.toarray()

    return similarity_matrix

from scipy.spatial.distance import pdist, squareform
from umap.umap_ import find_ab_params


def umap_low_dim_similarity_with_umap_params(embedding, min_dist=0.1, spread=1.0):
    """
    使用UMAP内部函数计算参数a和b，然后计算低维相似度矩阵

    参数:
    embedding: 降维后的数据
    min_dist: 最小距离参数
    spread: 分布扩散参数

    返回:
    similarity_matrix: 低维相似度矩阵
    """
    # 使用UMAP的函数计算参数a和b
    a, b = find_ab_params(spread, min_dist)

    # 计算距离矩阵
    distances = squareform(pdist(embedding, 'euclidean'))
    n_samples = embedding.shape[0]

    # 应用UMAP核函数计算相似度
    similarity_matrix = 1.0 / (1.0 + a * np.maximum(0, distances - min_dist) ** (2 * b))

    # 确保对角线为1
    np.fill_diagonal(similarity_matrix, 1.0)

    return similarity_matrix

def compute_low_dimensional_similarity(data, formula, parameters):
    """
    计算低维空间中的相似度矩阵

    参数:
    - data: numpy数组形式的数据集（低维嵌入）
    - formula: 计算公式名称
    - parameters: 计算参数

    返回:
    - similarity_matrix: 相似度矩阵
    """
    n_samples = data.shape[0]

    if formula == 'tsne_low_similarity':
        # t-SNE低维相似度（q_ij）
        degrees_of_freedom = parameters.get('degrees_of_freedom', 1.0)

        # 计算欧氏距离矩阵
        distances = squareform(pdist(data, 'euclidean'))

        # 计算 t-分布的核
        inv_distances = 1 / (1 + (distances ** 2) / degrees_of_freedom)
        np.fill_diagonal(inv_distances, 0.0)  # q_ii = 0

        # 归一化
        similarity_matrix = inv_distances / np.sum(inv_distances)

    elif formula == 'umap_low_similarity':
        # UMAP低维相似度
        a = parameters.get('a', 1.0)
        b = parameters.get('b', 1.0)

        similarity_matrix = umap_low_dim_similarity_with_umap_params(data,parameters.get('min_dist',0.1))

        # 计算欧氏距离矩阵
        # distances = squareform(pdist(data, 'euclidean'))
        #
        # # 计算UMAP低维相似度: q_ij = (1 + a * ||y_i - y_j||^2b)^-1
        # similarity_matrix = 1.0 / (1.0 + a * (distances ** (2 * b)))
        # np.fill_diagonal(similarity_matrix, 0.0)  # q_ii = 0

        # 归一化 (可选)
        # similarity_matrix = similarity_matrix / np.sum(similarity_matrix)

    else:
        raise ValueError(f"未知的低维相似度计算公式: {formula}")

    return similarity_matrix


def compute_gaussian_kernel_row(dist_row, i, perplexity):
    """
    为单个点计算高斯核（条件概率p_j|i）
    使用二分搜索找到合适的sigma，使得概率分布的困惑度接近目标值

    参数:
    - dist_row: 点i到所有其他点的距离
    - i: 当前点的索引
    - perplexity: 目标困惑度

    返回:
    - prob_row: 条件概率p_j|i
    """
    n = len(dist_row)
    tolerance = 1e-5
    log_perp = np.log(perplexity)

    # 初始化结果向量
    prob_row = np.zeros(n)

    # 排除自身
    indices = np.arange(n) != i

    # 设置搜索范围
    beta_min = -np.inf
    beta_max = np.inf
    beta = 1.0  # 初始值，beta = 1/(2*sigma^2)

    # 使用二分搜索找到合适的beta
    max_iterations = 50
    for _ in range(max_iterations):
        # 计算高斯核
        dist_squared = dist_row[indices] ** 2
        exp_values = np.exp(-beta * dist_squared)
        sum_exp = np.sum(exp_values)

        if sum_exp == 0:
            # 避免除以零
            beta = beta / 2.0
            continue

        # 计算概率
        probs = exp_values / sum_exp

        # 计算熵
        entropy = np.sum(-probs * np.log2(probs + 1e-10))

        # 计算困惑度差
        entropy_diff = entropy - log_perp

        if np.abs(entropy_diff) < tolerance:
            break

        # 更新beta
        if entropy_diff > 0:
            # 当前熵太高，增大beta以减小困惑度
            beta_min = beta
            if beta_max == np.inf:
                beta = beta * 2.0
            else:
                beta = (beta + beta_max) / 2.0
        else:
            # 当前熵太低，减小beta以增加困惑度
            beta_max = beta
            if beta_min == -np.inf:
                beta = beta / 2.0
            else:
                beta = (beta + beta_min) / 2.0

    # 计算最终概率
    dist_squared = dist_row ** 2
    exp_values = np.exp(-beta * dist_squared)
    exp_values[i] = 0  # 确保自身概率为0
    prob_row = exp_values / np.sum(exp_values)

    return prob_row


def find_sigma_umap(distances, indices, rho):
    """
    为UMAP相似度计算寻找合适的sigma

    参数:
    - distances: 点i到所有其他点的距离
    - indices: k近邻的索引
    - rho: 距离到第k近邻的距离

    返回:
    - sigma: 缩放参数
    """
    target = np.log(indices.shape[0])
    lo = 0.0
    hi = np.inf
    mid = 1.0

    # 二分搜索
    for _ in range(20):
        spread = np.zeros(indices.shape[0])

        for i, idx in enumerate(indices):
            d = max(0, distances[idx] - rho)
            spread[i] = np.exp(-d / mid)

        # 计算熵
        sum_spread = np.sum(spread)
        if sum_spread == 0:
            break

        entropy = -np.sum((spread / sum_spread) * np.log(spread / sum_spread + 1e-10))

        # 检查是否接近目标熵
        if np.abs(entropy - target) < 1e-3:
            break

        # 更新搜索范围
        if entropy < target:
            hi = mid
            mid = (lo + hi) / 2.0
        else:
            lo = mid
            if hi == np.inf:
                mid = mid * 2.0
            else:
                mid = (lo + hi) / 2.0

    return mid