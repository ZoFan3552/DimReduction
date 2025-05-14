# 主成分分析(PCA)降维算法详解

## 1. 基本概念
**主成分分析** (Principal Component Analysis, PCA) 是一种**无监督**的线性降维方法，通过正交变换将高维数据投影到低维空间，同时保留最大方差。

### 核心特点：
- 🎯 **数据压缩**：减少特征维度
- 📊 **方差最大化**：保留最重要的数据变异
- ✂️ **去相关性**：生成的主成分互不相关
- 🔍 **特征提取**：发现数据潜在结构

## 2. 数学原理

### 2.1 输入数据
给定数据集 $X \in \mathbb{R}^{n \times p}$，其中：
- $n$：样本数量
- $p$：原始特征维度

### 2.2 标准化处理
对每个特征进行标准化：
$$
X_{ij} = \frac{X_{ij} - \mu_j}{\sigma_j}
$$
其中$\mu_j$为均值，$\sigma_j$为标准差

### 2.3 协方差矩阵计算
$$
\Sigma = \frac{1}{n}X^TX \in \mathbb{R}^{p \times p}
$$

### 2.4 特征分解
求解特征方程：
$$
\Sigma v = \lambda v
$$
- $\lambda$：特征值（表示主成分的重要性）
- $v$：特征向量（主成分方向）

### 2.5 选择主成分
按特征值从大到小排序，选择前$k$个特征向量组成投影矩阵：
$$
W = [v_1, v_2, ..., v_k] \in \mathbb{R}^{p \times k}
$$

### 2.6 降维投影
$$
Z = XW \in \mathbb{R}^{n \times k}
$$

## 3. 算法步骤（Python伪代码）

```python
# 1. 数据标准化
X_std = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

# 2. 计算协方差矩阵
cov_mat = np.cov(X_std.T)

# 3. 特征分解
eigen_vals, eigen_vecs = np.linalg.eig(cov_mat)

# 4. 排序特征值
idx = eigen_vals.argsort()[::-1]
eigen_vecs = eigen_vecs[:,idx]

# 5. 选择前k个主成分
W = eigen_vecs[:,:k]

# 6. 投影降维
X_pca = X_std.dot(W)
```

## 4. 关键参数

|     参数     |       说明       |             典型值              |
| :----------: | :--------------: | :-----------------------------: |
| n_components | 保留的主成分数量 | 1-3 (可视化) 0.95 (保留95%方差) |
|    whiten    |   是否白化数据   |              False              |
|  svd_solver  |    求解器类型    |             'auto'              |

## 5. 优缺点分析

### ✅ 优点：

- 计算效率高（*O*(*p*3)）
- 线性变换可解释性强
- 有效去除特征相关性
- 适用于高斯分布数据

### ❌ 局限：

- 线性方法，无法处理非线性关系
- 对异常值敏感
- 方差小的特征可能包含重要信息
- 需要数据标准化

## 6. 应用场景

### 典型应用：

- 🖼️ **图像压缩** (人脸识别Eigenfaces)
- 🧬 **基因数据分析**
- 📈 **金融风险因子分析**
- 🔬 **化学光谱处理**

## 7. 可视化示例

**Scree Plot**（碎石图）：

python

复制

```python
plt.plot(np.cumsum(eigen_vals)/sum(eigen_vals))
plt.xlabel('Number of components')
plt.ylabel('Explained variance ratio')
```

**Biplot**（双标图）：

python

复制

```python
# 同时显示样本和变量在PC空间的投影
```

## 8. 扩展方法

### 非线性扩展：

- Kernel PCA
- t-SNE
- UMAP

### 稀疏版本：

- Sparse PCA