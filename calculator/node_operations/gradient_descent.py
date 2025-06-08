from flask import Flask, request, jsonify, Blueprint
from sklearn.metrics import pairwise_distances
import numpy as np
import uuid
import copy
from scipy.spatial.distance import pdist, squareform
from umap.umap_ import find_ab_params
gradient_api = Blueprint('gradient_api', __name__)


def compute_low_dimensional_similarity_tsne(Y):
    """
    计算t-SNE低维相似度矩阵
    """
    n = Y.shape[0]

    # 计算成对欧氏距离
    sum_Y = np.sum(np.square(Y), axis=1)
    D = np.add(np.add(-2 * np.dot(Y, Y.T), sum_Y).T, sum_Y)

    # 确保距离非负
    D = np.maximum(D, 0.0)

    # Student-t分布（自由度为1）
    num = 1 / (1 + D)
    np.fill_diagonal(num, 0)

    # 归一化，防止除以零
    q_sum = np.sum(num)
    if q_sum < 1e-12:
        # 如果和太小，添加一个小常数防止除零
        q = num + 1e-12
        q = q / np.sum(q)
    else:
        q = num / q_sum

    # 确保最小值
    q = np.maximum(q, 1e-12)

    return q


def compute_low_dimensional_similarity_sne(Y):
    """
    计算SNE低维相似度矩阵（使用高斯分布）
    """
    n = Y.shape[0]

    # 计算成对欧氏距离
    sum_Y = np.sum(np.square(Y), axis=1)
    D = np.add(np.add(-2 * np.dot(Y, Y.T), sum_Y).T, sum_Y)

    # 确保距离非负
    D = np.maximum(D, 0.0)

    # 高斯核
    q = np.exp(-D)
    np.fill_diagonal(q, 0)

    # 归一化，防止除以零
    q_sum = np.sum(q)
    if q_sum < 1e-12:
        # 如果和太小，添加一个小常数防止除零
        q = q + 1e-12
        q = q / np.sum(q)
    else:
        q = q / q_sum

    # 确保最小值
    q = np.maximum(q, 1e-12)

    return q



def compute_gradient_tsne(P, Q, Y):
    """
    计算t-SNE梯度
    """
    n = Y.shape[0]

    # 计算成对欧氏距离
    sum_Y = np.sum(np.square(Y), axis=1)
    D = np.add(np.add(-2 * np.dot(Y, Y.T), sum_Y).T, sum_Y)

    # 确保距离非负
    D = np.maximum(D, 0.0)

    # t-SNE梯度计算
    inv_D = np.power(1 + D, -1)

    # 确保没有无效值
    inv_D = np.nan_to_num(inv_D, nan=0.0, posinf=0.0, neginf=0.0)

    # t-SNE梯度中的PQ差异
    PQ_diff = P - Q

    # 避免无效值
    PQ_diff = np.nan_to_num(PQ_diff, nan=0.0, posinf=0.0, neginf=0.0)

    grad = np.zeros_like(Y)

    for i in range(n):
        # 使用向量化操作计算梯度，确保数值稳定
        grad_i = 4 * np.sum(np.expand_dims(PQ_diff[i] * inv_D[i], 1) * (Y[i] - Y), axis=0)

        # 避免梯度爆炸
        if np.linalg.norm(grad_i) > 10.0:
            grad_i = grad_i / np.linalg.norm(grad_i) * 10.0

        grad[i] = grad_i

    return grad


def compute_gradient_sne(P, Q, Y):
    """
    计算SNE梯度
    """
    n = Y.shape[0]

    # 计算成对欧氏距离
    sum_Y = np.sum(np.square(Y), axis=1)
    D = np.add(np.add(-2 * np.dot(Y, Y.T), sum_Y).T, sum_Y)

    # 确保距离非负
    D = np.maximum(D, 0.0)

    # SNE梯度计算中的PQ差异
    PQ_diff = P - Q

    # 避免无效值
    PQ_diff = np.nan_to_num(PQ_diff, nan=0.0, posinf=0.0, neginf=0.0)

    grad = np.zeros_like(Y)

    for i in range(n):
        # 使用向量化操作计算梯度，确保数值稳定
        grad_i = 2 * np.sum(np.expand_dims(PQ_diff[i], 1) * (Y[i] - Y), axis=0)

        # 避免梯度爆炸
        if np.linalg.norm(grad_i) > 10.0:
            grad_i = grad_i / np.linalg.norm(grad_i) * 10.0

        grad[i] = grad_i

    return grad





def calculate_cost_tsne(P, Q):
    """
    计算t-SNE成本函数值 (KL散度)
    """
    # 确保P和Q中没有无效值，并且是有效的概率分布
    P = np.maximum(P, 1e-12)
    Q = np.maximum(Q, 1e-12)

    # 避免log(0)
    ratio = np.maximum(P / Q, 1e-12)

    # 处理可能的NaN或Inf
    log_ratio = np.log(ratio)
    log_ratio = np.nan_to_num(log_ratio, nan=0.0, posinf=0.0, neginf=0.0)

    # 计算KL散度
    kl = P * log_ratio

    # 处理可能的NaN或Inf
    kl = np.nan_to_num(kl, nan=0.0, posinf=0.0, neginf=0.0)

    return np.sum(kl)


def calculate_cost_sne(P, Q):
    """
    计算SNE成本函数值 (KL散度)
    """
    # 确保P和Q中没有无效值，并且是有效的概率分布
    P = np.maximum(P, 1e-12)
    Q = np.maximum(Q, 1e-12)

    # 避免log(0)
    ratio = np.maximum(P / Q, 1e-12)

    # 处理可能的NaN或Inf
    log_ratio = np.log(ratio)
    log_ratio = np.nan_to_num(log_ratio, nan=0.0, posinf=0.0, neginf=0.0)

    # 计算KL散度
    kl = P * log_ratio

    # 处理可能的NaN或Inf
    kl = np.nan_to_num(kl, nan=0.0, posinf=0.0, neginf=0.0)

    return np.sum(kl)




def calculate_gradient_norm(grad):
    """
    计算梯度的Frobenius范数
    """
    return np.sqrt(np.sum(np.square(grad)))



def umap_gradient_descent(high_dim_sim, Y_init, learning_rate=1.0, iterations=1000,
                          min_dist=0.1, recording_interval=100):
    """
    UMAP梯度下降优化，接收高维相似度矩阵和初始低维嵌入

    参数:
    high_dim_sim: 高维相似度矩阵，形状为 (n_samples, n_samples)，将被转换为numpy数组
    Y_init: 初始低维嵌入，形状为 (n_samples, n_components)
    learning_rate: 梯度下降的学习率
    iterations: 梯度下降的迭代次数
    min_dist: 控制嵌入中点的最小距离
    recording_interval: 记录数据的间隔

    返回:
    Y: 优化后的低维嵌入
    low_dim_sim: 最终的低维相似度矩阵
    iterations_data: 迭代过程中记录的数据
    """
    # 确保输入是numpy数组
    high_dim_sim = np.array(high_dim_sim)
    Y = np.array(Y_init.copy()) if not isinstance(Y_init, np.ndarray) else Y_init.copy()

    n_samples = Y.shape[0]

    # 创建存储迭代数据的列表
    iterations_data = []

    # UMAP中的a和b参数，用于控制嵌入的分布
    a = 1.0
    b = 1.0
    if min_dist > 0:
        # 根据min_dist设置a和b
        a = 1.929
        b = 0.7915

    # 梯度下降优化
    for iteration in range(iterations):
        # 计算低维空间中的距离
        Y_distances = pairwise_distances(Y)
        np.fill_diagonal(Y_distances, 1.0)  # 避免除以零

        # 计算梯度
        gradient = np.zeros_like(Y)

        for i in range(n_samples):
            for j in range(n_samples):
                if i != j:
                    # 高维相似度
                    v = high_dim_sim[i, j]

                    # 低维距离
                    dist = Y_distances[i, j]

                    # 方向向量
                    direction = (Y[i] - Y[j]) / (dist + 1e-10)

                    # UMAP的低维相似度函数
                    w = 1.0 / (1.0 + a * (dist ** (2 * b)))

                    # 梯度计算
                    # 吸引力：高维相似度 * 低维不相似度
                    # 排斥力：低维相似度 * (1 - 高维相似度)
                    if v > 0:
                        attractive_force = v * (1.0 - w) * direction
                        gradient[i] -= learning_rate * attractive_force

                    # 所有点之间都有排斥力
                    repulsive_force = (1.0 - v) * w * direction
                    gradient[i] += learning_rate * repulsive_force

        # 更新低维嵌入
        Y += gradient

        # 计算当前成本
        cost = 0.0
        for i in range(n_samples):
            for j in range(i + 1, n_samples):  # 只计算上三角矩阵，避免重复
                v = high_dim_sim[i, j]
                dist = Y_distances[i, j]
                w = 1.0 / (1.0 + a * (dist ** (2 * b)))

                if v > 0:
                    # 正样本对的损失
                    cost += -v * np.log(w + 1e-10) - (1 - v) * np.log(1 - w + 1e-10)

        # 计算梯度范数
        grad_norm = np.linalg.norm(gradient)

        # 记录迭代数据
        if iteration % recording_interval == 0 or iteration == iterations - 1:
            print("迭代次数", iteration)
            iterations_data.append({
                'iteration': iteration,
                'embedding': Y.tolist(),
                'cost': float(cost),
                'gradient_norm': float(grad_norm)
            })

    # 计算最终的低维相似度矩阵
    final_Y_distances = pairwise_distances(Y)
    np.fill_diagonal(final_Y_distances, 0.0)  # 对角线设为0，表示自己与自己的相似度最高

    # 将距离转换为相似度
    low_dim_sim = np.zeros_like(final_Y_distances)
    for i in range(n_samples):
        for j in range(n_samples):
            if i != j:
                dist = final_Y_distances[i, j]
                # 使用UMAP的低维相似度函数计算相似度
                low_dim_sim[i, j] = 1.0 / (1.0 + a * (dist ** (2 * b)))

    # 返回最终的低维嵌入、低维相似度矩阵和迭代记录
    return Y, low_dim_sim, iterations_data

def run_gradient_descent(algorithm, parameters, node_data):
    """
    执行梯度下降算法
    """
    # 将输入数据视为低维表示
    dataset = np.array(node_data.get('dataset', []), dtype=np.float64)

    # 确保数据的第二列是可操作的
    if dataset.size == 0 or dataset.ndim != 2:
        return {"success": False, "message": "数据集格式不正确"}

    # 获取初始的高维相似度矩阵（如果存在）
    computed = node_data.get('computed', {})

    # 如果没有高维相似度矩阵，则计算一个
    high_similarity_matrix = computed.get('high_similarity_matrix')
    if high_similarity_matrix is None:
        if 'feature_names' not in node_data or not node_data['feature_names']:
            return {"success": False, "message": "需要特征数据来计算高维相似度矩阵"}

        # 假设dataset是低维表示，我们需要另一个高维数据来计算高维相似度
        # 通常在此之前应该有其他节点提供了高维数据
        return {"success": False, "message": "缺少高维相似度矩阵"}
    else:
        # 确保是numpy数组
        P = np.array(high_similarity_matrix, dtype=np.float64)

        # 确保P中没有无效值
        P = np.nan_to_num(P, nan=1e-12, posinf=1e-12, neginf=1e-12)

        # 确保P是有效概率分布
        P = np.maximum(P, 1e-12)
        P_sum = np.sum(P)
        if P_sum > 0:
            P = P / P_sum
        else:
            return {"success": False, "message": "高维相似度矩阵无效，请重新计算"}

    # 初始化低维表示
    # 如果数据集已经有2列，就直接使用
    if dataset.shape[1] == 2:
        Y = dataset.copy()
    else:
        # 否则从数据集前两列或随机初始化
        if dataset.shape[1] >= 2:
            Y = dataset[:, :2].copy()
        else:
            n_samples = dataset.shape[0]
            Y = np.random.randn(n_samples, 2) * 0.0001

    # 检查Y中是否有无效值
    if np.isnan(Y).any() or np.isinf(Y).any():
        # 如果有无效值，则重新初始化
        n_samples = Y.shape[0]
        Y = np.random.randn(n_samples, 2) * 0.0001

    # 算法参数
    iterations = parameters.get('iterations', 1000)
    learning_rate = parameters.get('learning_rate', 200)
    momentum = parameters.get('momentum', 0.8)
    perplexity = parameters.get('perplexity', 30)
    n_neighbors = parameters.get('n_neighbors', 15)
    min_dist = parameters.get('min_dist', 0.1)
    recording_interval = parameters.get('recording_interval', 10)

    # 初始化动量项
    Y_prev = Y.copy()
    Y_incs = np.zeros_like(Y)

    # 记录迭代过程
    iterations_data = []

    # 根据算法选择不同的相似度计算方法
    if algorithm == 'tsne':
        compute_low_similarity = compute_low_dimensional_similarity_tsne
        compute_gradient = compute_gradient_tsne
        calculate_cost = calculate_cost_tsne
        algorithm_params = {}
    elif algorithm == 'sne':
        compute_low_similarity = compute_low_dimensional_similarity_sne
        compute_gradient = compute_gradient_sne
        calculate_cost = calculate_cost_sne
        algorithm_params = {}
    elif algorithm == 'umap':
        a, b = find_ab_params(1.0, min_dist)
        try:
            print("high_similarity_matrix",type(high_similarity_matrix))
            print("Y",type(Y))
            # print("high_similarity_matrix的尺寸", high_similarity_matrix.shape)
            print("Y的尺寸", Y.shape)
            Y, final_Q,iterations_data = umap_gradient_descent(high_similarity_matrix,Y,learning_rate,iterations,min_dist, recording_interval)
        except Exception as e:
            return {"success": False, "message": f"UMAP梯度下降过程中出错: {str(e)}"}

    else:
        return {"success": False, "message": f"不支持的算法: {algorithm}"}

    # 梯度下降主循环
    if algorithm !='umap':
        for iteration in range(iterations):
            try:
                # 计算当前低维相似度
                Q = compute_low_similarity(Y)

                # 检查Q是否有效
                if np.isnan(Q).any() or np.isinf(Q).any():
                    # 如果Q无效，则尝试重置Y并减小学习率
                    Y = Y_prev.copy()
                    learning_rate *= 0.5
                    if learning_rate < 1e-5:
                        return {"success": False,
                                "message": "梯度下降过程中出现数值不稳定，请尝试降低学习率或重新初始化"}
                    continue

                # 计算梯度
                grad = compute_gradient(P, Q, Y, **algorithm_params)

                # 检查梯度是否有效
                if np.isnan(grad).any() or np.isinf(grad).any():
                    # 如果梯度无效，尝试使用小梯度代替
                    grad = np.nan_to_num(grad, nan=0.0, posinf=1.0, neginf=-1.0)
                    # 限制梯度幅度
                    grad_norm = np.sqrt(np.sum(np.square(grad)))
                    if grad_norm > 1.0:
                        grad = grad / grad_norm

                # 计算当前成本和梯度范数
                cost = calculate_cost(P, Q)
                grad_norm = calculate_gradient_norm(grad)

                # 应用动量和学习率
                Y_incs = momentum * Y_incs - learning_rate * grad
                Y_next = Y + Y_incs

                # 检查新位置是否有效
                if np.isnan(Y_next).any() or np.isinf(Y_next).any():
                    # 如果无效，则减小学习率并重试
                    learning_rate *= 0.5
                    if learning_rate < 1e-5:
                        return {"success": False,
                                "message": "梯度下降过程中出现数值不稳定，请尝试降低学习率或重新初始化"}
                    continue

                # 更新位置
                Y_prev = Y.copy()
                Y = Y_next

                # 为了可视化清晰度，去除嵌入的平均值
                Y = Y - np.mean(Y, axis=0)

                # 记录迭代数据
                if iteration % recording_interval == 0 or iteration == iterations - 1:
                    print("迭代次数", iteration)
                    iterations_data.append({
                        'iteration': iteration,
                        'embedding': Y.tolist(),
                        'cost': float(cost),
                        'gradient_norm': float(grad_norm)
                    })

            except Exception as e:
                return {"success": False, "message": f"梯度下降过程中出错: {str(e)}"}

    # 创建新节点
    new_node = copy.deepcopy(node_data)
    new_node['id'] = str(uuid.uuid4())
    new_node['operation'] = f"{algorithm.upper()} 梯度下降"
    new_node['parameters'] = parameters
    new_node['dataset'] = Y.tolist()
    new_node['children'] = []
    new_node['selected'] = False

    # 更新计算结果
    if 'computed' not in new_node:
        new_node['computed'] = {}

    # 计算最终的低维相似度
    try:
        if algorithm != 'umap':
            final_Q = compute_low_similarity(Y)

    except Exception as e:
        return {"success": False, "message": f"梯度下降出错点1: {str(e)}"}
    try:
        new_node['computed']['high_similarity_matrix'] = high_similarity_matrix
        new_node['computed']['low_similarity_matrix'] = final_Q.tolist()
        new_node['computed']['final_cost'] = float(iterations_data[len(iterations_data) - 1]['cost'])
        new_node['computed']['iterations_recorded'] = len(iterations_data)
    except Exception as e:
        return {"success": False, "message": f"梯度下降出错点2: {str(e)}"}

    return {
        "success": True,
        "message": "梯度下降计算成功",
        "node": new_node,
        "iterations": iterations_data
    }


@gradient_api.route('/api/gradient_descent', methods=['POST'])
def gradient_descent_endpoint():
    """
    梯度下降API端点
    """
    try:
        data = request.get_json()

        algorithm = data.get('algorithm')
        parameters = data.get('parameters', {})
        node_data = data.get('node')

        if not algorithm:
            return jsonify({"success": False, "message": "缺少算法参数"}), 400

        if not node_data:
            return jsonify({"success": False, "message": "缺少节点数据"}), 400

        # 运行梯度下降
        result = run_gradient_descent(algorithm, parameters, node_data)

        return jsonify(result)

    except Exception as e:
        # app.logger.error(f"梯度下降计算错误: {str(e)}")
        return jsonify({"success": False, "message": f"处理请求时出错: {str(e)}"}), 500

