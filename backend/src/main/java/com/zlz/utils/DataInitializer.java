package com.zlz.utils;


import com.zlz.dao.AlgorithmCodeRepository;
import com.zlz.pojo.AlgorithmCode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * 应用启动时初始化标准算法代码
 */
@Component
public class DataInitializer implements CommandLineRunner {

    private final AlgorithmCodeRepository algorithmCodeRepository;

    public DataInitializer(AlgorithmCodeRepository algorithmCodeRepository) {
        this.algorithmCodeRepository = algorithmCodeRepository;
    }

    @Override
    public void run(String... args) throws Exception {
        // 只有当数据库中没有算法代码时才初始化
        if (algorithmCodeRepository.count() == 0) {
            AlgorithmCode standardCode = new AlgorithmCode();

            standardCode.setPcaCode(getPCAStandardCode());
            standardCode.setTsneCode(getTSNEStandardCode());
            standardCode.setUmapCode(getUMAPStandardCode());

            algorithmCodeRepository.save(standardCode);

            System.out.println("标准算法代码初始化完成");
        }
    }

    private String getPCAStandardCode() {
        return "# PCA（主成分分析）标准实现\n" +
                "import numpy as np\n" +
                "import matplotlib.pyplot as plt\n" +
                "from sklearn.datasets import load_iris\n" +
                "from sklearn.preprocessing import StandardScaler\n" +
                "\n" +
                "# 设置中文字体（使用系统支持的字体）\n" +
                "plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows\n" +
                "  \n" +
                "# 加载数据\n" +
                "iris = load_iris()\n" +
                "X = iris.data\n" +
                "y = iris.target\n" +
                "  \n" +
                "# 标准化数据\n" +
                "scaler = StandardScaler()\n" +
                "X_scaled = scaler.fit_transform(X)\n" +
                "  \n" +
                "# PCA实现\n" +
                "class PCA:\n" +
                "    def __init__(self, n_components):\n" +
                "        self.n_components = n_components\n" +
                "        self.components = None\n" +
                "        self.mean = None\n" +
                "        self.explained_variance_ratio = None\n" +
                "      \n" +
                "    def fit(self, X):\n" +
                "        # 中心化\n" +
                "        self.mean = np.mean(X, axis=0)\n" +
                "        X_centered = X - self.mean\n" +
                "          \n" +
                "        # 计算协方差矩阵\n" +
                "        cov_matrix = np.cov(X_centered.T)\n" +
                "          \n" +
                "        # 特征值分解\n" +
                "        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)\n" +
                "          \n" +
                "        # 排序\n" +
                "        idx = eigenvalues.argsort()[::-1]\n" +
                "        eigenvalues = eigenvalues[idx]\n" +
                "        eigenvectors = eigenvectors[:, idx]\n" +
                "          \n" +
                "        # 存储主成分\n" +
                "        self.components = eigenvectors[:, :self.n_components]\n" +
                "          \n" +
                "        # 计算解释方差比例\n" +
                "        self.explained_variance_ratio = eigenvalues[:self.n_components] / np.sum(eigenvalues)\n" +
                "          \n" +
                "        return self\n" +
                "      \n" +
                "    def transform(self, X):\n" +
                "        X_centered = X - self.mean\n" +
                "        return np.dot(X_centered, self.components)\n" +
                "  \n" +
                "# 应用PCA\n" +
                "pca = PCA(n_components=2)\n" +
                "pca.fit(X_scaled)\n" +
                "X_pca = pca.transform(X_scaled)\n" +
                "  \n" +
                "# 可视化\n" +
                "plt.figure(figsize=(10, 8))\n" +
                "colors = ['navy', 'turquoise', 'darkorange']\n" +
                "target_names = ['鸢尾-setosa', '鸢尾-versicolor', '鸢尾-virginica']\n" +
                "\n" +
                "for color, i, target_name in zip(colors, [0, 1, 2], target_names):\n" +
                "    plt.scatter(X_pca[y == i, 0], X_pca[y == i, 1], \n" +
                "               color=color, alpha=0.8, lw=2, label=target_name)\n" +
                "\n" +
                "plt.xlabel(f'第一主成分 ({pca.explained_variance_ratio[0]:.2%})')\n" +
                "plt.ylabel(f'第二主成分 ({pca.explained_variance_ratio[1]:.2%})')\n" +
                "plt.title('PCA降维后的鸢尾花数据集')\n" +
                "plt.legend(loc='best', shadow=False, scatterpoints=1)\n" +
                "plt.grid(True, alpha=0.3)\n" +
                "plt.show()\n" +
                "  \n" +
                "print(f\"解释方差比例: {pca.explained_variance_ratio}\")\n" +
                "print(f\"累计解释方差: {np.sum(pca.explained_variance_ratio):.2%}\")\n" +
                "\n" +
                "# 验证与sklearn实现的一致性\n" +
                "from sklearn.decomposition import PCA as SklearnPCA\n" +
                "\n" +
                "sklearn_pca = SklearnPCA(n_components=2)\n" +
                "X_sklearn_pca = sklearn_pca.fit_transform(X_scaled)\n" +
                "\n" +
                "print(\"\\n与sklearn实现的比较:\")\n" +
                "print(f\"sklearn解释方差比例: {sklearn_pca.explained_variance_ratio_}\")";
    }

    private String getTSNEStandardCode() {
        return "# t-SNE（t-分布随机近邻嵌入）标准实现\n" +
                "import numpy as np\n" +
                "import matplotlib.pyplot as plt\n" +
                "from sklearn.datasets import load_digits\n" +
                "from sklearn.manifold import TSNE\n" +
                "from sklearn.preprocessing import StandardScaler\n" +
                "\n" +
                "# 设置中文字体（使用系统支持的字体）\n" +
                "plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows\n" +
                "\n" +
                "# 加载数据\n" +
                "digits = load_digits()\n" +
                "X = digits.data[:400]  # 使用部分数据加快计算\n" +
                "y = digits.target[:400]\n" +
                "\n" +
                "# 数据预处理\n" +
                "scaler = StandardScaler()\n" +
                "X_scaled = scaler.fit_transform(X)\n" +
                "\n" +
                "# 应用t-SNE降维\n" +
                "tsne = TSNE(n_components=2, perplexity=30, n_iter=1000, random_state=42)\n" +
                "X_tsne = tsne.fit_transform(X_scaled)\n" +
                "\n" +
                "# 可视化\n" +
                "plt.figure(figsize=(12, 10))\n" +
                "\n" +
                "# 创建颜色映射\n" +
                "colors = plt.cm.get_cmap('tab10', 10)\n" +
                "\n" +
                "# 散点图\n" +
                "for i in range(10):  # 数字0-9\n" +
                "    plt.scatter(\n" +
                "        X_tsne[y == i, 0], \n" +
                "        X_tsne[y == i, 1],\n" +
                "        c=[colors(i)],\n" +
                "        label=f'数字 {i}',\n" +
                "        alpha=0.8,\n" +
                "        s=60\n" +
                "    )\n" +
                "\n" +
                "plt.title('t-SNE降维可视化手写数字数据', fontsize=16)\n" +
                "plt.xlabel('t-SNE维度1', fontsize=12)\n" +
                "plt.ylabel('t-SNE维度2', fontsize=12)\n" +
                "plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')\n" +
                "plt.grid(alpha=0.3)\n" +
                "plt.tight_layout()\n" +
                "plt.show()\n" +
                "\n" +
                "# 输出降维结果信息\n" +
                "print(f\"原始数据维度: {X.shape}\")\n" +
                "print(f\"降维后数据维度: {X_tsne.shape}\")\n" +
                "print(\"\\nt-SNE降维完成！\")\n" +
                "\n" +
                "# t-SNE的一些特性说明\n" +
                "print(\"\\nt-SNE算法特性:\")\n" +
                "print(\"1. 保持数据的局部结构，适合可视化高维数据\")\n" +
                "print(\"2. 非线性降维，可以发现复杂的流形结构\")\n" +
                "print(\"3. perplexity参数控制局部近邻数量，通常在5-50之间调整\")\n" +
                "print(\"4. 迭代次数n_iter可以影响结果质量，通常需要至少1000次迭代获得稳定结果\")";
    }

    private String getUMAPStandardCode() {
        return "# UMAP（统一流形逼近和投影）标准实现\n" +
                "import numpy as np\n" +
                "import matplotlib.pyplot as plt\n" +
                "from sklearn.datasets import load_digits\n" +
                "from sklearn.preprocessing import StandardScaler\n" +
                "\n" +
                "# 需要安装umap-learn库\n" +
                "# pip install umap-learn\n" +
                "import umap\n" +
                "\n" +
                "# 设置中文字体（使用系统支持的字体）\n" +
                "plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑，适用于Windows\n" +
                "\n" +
                "# 加载数据\n" +
                "digits = load_digits()\n" +
                "X = digits.data\n" +
                "y = digits.target\n" +
                "\n" +
                "# 数据标准化\n" +
                "scaler = StandardScaler()\n" +
                "X_scaled = scaler.fit_transform(X)\n" +
                "\n" +
                "# UMAP参数设置\n" +
                "n_neighbors = 15      # 局部近邻点数量\n" +
                "min_dist = 0.1        # 嵌入空间中点的最小距离\n" +
                "n_components = 2      # 降维后的维度\n" +
                "\n" +
                "# 应用UMAP降维\n" +
                "reducer = umap.UMAP(\n" +
                "    n_neighbors=n_neighbors,\n" +
                "    min_dist=min_dist,\n" +
                "    n_components=n_components,\n" +
                "    random_state=42\n" +
                ")\n" +
                "\n" +
                "X_umap = reducer.fit_transform(X_scaled)\n" +
                "\n" +
                "# 可视化结果\n" +
                "plt.figure(figsize=(12, 10))\n" +
                "\n" +
                "# 创建颜色映射\n" +
                "colors = plt.cm.get_cmap('tab10', 10)\n" +
                "\n" +
                "# 绘制散点图\n" +
                "for i in range(10):  # 数字0-9\n" +
                "    plt.scatter(\n" +
                "        X_umap[y == i, 0], \n" +
                "        X_umap[y == i, 1],\n" +
                "        c=[colors(i)],\n" +
                "        label=f'数字 {i}',\n" +
                "        alpha=0.8,\n" +
                "        s=60\n" +
                "    )\n" +
                "\n" +
                "plt.title('UMAP降维可视化手写数字数据', fontsize=16)\n" +
                "plt.xlabel('UMAP维度1', fontsize=12)\n" +
                "plt.ylabel('UMAP维度2', fontsize=12)\n" +
                "plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')\n" +
                "plt.grid(alpha=0.3)\n" +
                "plt.tight_layout()\n" +
                "plt.show()\n" +
                "\n" +
                "# 输出降维结果信息\n" +
                "print(f\"原始数据维度: {X.shape}\")\n" +
                "print(f\"降维后数据维度: {X_umap.shape}\")\n" +
                "print(\"\\nUMAP降维完成！\")\n" +
                "\n" +
                "# UMAP的特性说明\n" +
                "print(\"\\nUMAP算法特性:\")\n" +
                "print(\"1. 比t-SNE更快的计算速度，尤其对于大型数据集\")\n" +
                "print(\"2. 可以保持数据的全局结构同时也保留局部信息\")\n" +
                "print(\"3. n_neighbors参数控制关注的局部结构范围(小值关注局部结构，大值关注全局结构)\")\n" +
                "print(\"4. min_dist参数控制嵌入空间中点的紧密程度\")\n" +
                "print(\"5. UMAP支持监督、半监督和无监督学习\")";
    }
}