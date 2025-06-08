<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>9. UMAP的应用场景</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 应用场景案例展示 -->
            <div class="interaction-container">
                <h3>应用场景案例展示</h3>
                <p>探索UMAP在不同领域的实际应用。点击下面的应用场景卡片，了解详细信息并查看相关可视化。</p>

                <div class="application-cards">
                    <el-row :gutter="20">
                        <el-col :span="8" v-for="(app, index) in applications" :key="index">
                            <el-card class="application-card" :class="{ active: selectedApplication === index }"
                                @click.native="selectApplication(index)">
                                <div class="card-content">
                                    <i :class="app.icon" class="app-icon"></i>
                                    <h4>{{ app.title }}</h4>
                                    <p>{{ app.shortDescription }}</p>
                                </div>
                            </el-card>
                        </el-col>
                    </el-row>
                </div>

                <div v-if="selectedApplication !== null" class="application-detail">
                    <el-divider>
                        <i class="el-icon-info"></i>
                        应用详情
                    </el-divider>

                    <div class="detail-content">
                        <h3>{{ applications[selectedApplication].title }}</h3>
                        <div class="application-viz" ref="applicationViz"></div>
                        <div class="detail-text" v-html="applications[selectedApplication].detailDescription"></div>

                        <div class="application-highlights">
                            <h4>关键优势</h4>
                            <el-row :gutter="20">
                                <el-col :span="8" v-for="(highlight, i) in applications[selectedApplication].highlights"
                                    :key="i">
                                    <div class="highlight-item">
                                        <i :class="highlight.icon"></i>
                                        <div class="highlight-text">
                                            <h5>{{ highlight.title }}</h5>
                                            <p>{{ highlight.description }}</p>
                                        </div>
                                    </div>
                                </el-col>
                            </el-row>
                        </div>

                        <div class="application-implementation">
                            <h4>实现提示</h4>
                            <el-alert type="info" :closable="false" show-icon>
                                <pre
                                    class="code-snippet"><code>{{ applications[selectedApplication].codeSnippet }}</code></pre>
                            </el-alert>
                        </div>
                    </div>
                </div>

                <!-- 应用场景匹配测验 -->
                <div class="quiz-container" v-if="!quizCompleted">
                    <h4>应用场景匹配练习</h4>
                    <p>根据您对UMAP应用场景的理解，将以下任务与最合适的降维方法匹配：</p>

                    <div class="match-quiz">
                        <div v-for="(scenario, index) in scenarios" :key="index" class="scenario-item">
                            <div class="scenario-desc">
                                <span class="scenario-number">{{ index + 1 }}</span>
                                <p>{{ scenario.description }}</p>
                            </div>

                            <el-select v-model="userMatches[index]" placeholder="选择最合适的方法">
                                <el-option v-for="option in matchOptions" :key="option.value" :label="option.label"
                                    :value="option.value">
                                </el-option>
                            </el-select>
                        </div>
                    </div>

                    <el-button type="primary" @click="checkMatches" :disabled="!isAllMatched" class="submit-btn">
                        提交答案
                    </el-button>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="quizFeedbackTitle" :type="allCorrect ? 'success' : 'info'"
                        :description="quizFeedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="!allCorrect" class="match-results">
                        <h4>匹配结果:</h4>
                        <div v-for="(scenario, index) in scenarios" :key="index" class="match-result-item">
                            <p>
                                <strong>{{ index + 1 }}. {{ scenario.description }}</strong>
                                <el-tag size="small" :type="matchResults[index] ? 'success' : 'danger'">
                                    {{ matchResults[index] ? '正确' : '错误' }}
                                </el-tag>
                            </p>
                            <p v-if="!matchResults[index]" class="explanation">
                                您的选择: {{ getOptionLabel(userMatches[index]) }}<br>
                                正确答案: {{ getOptionLabel(scenario.answer) }}<br>
                                解释: {{ scenario.explanation }}
                            </p>
                        </div>

                        <el-button type="info" @click="resetQuiz" class="retry-btn">
                            重新匹配
                        </el-button>
                    </div>

                    <div v-if="allCorrect || retries >= 1" class="next-section">
                        <p>🎉 您已完成UMAP应用场景部分！可以继续学习下一部分。</p>
                        <el-button type="success" @click="goToNextSection">
                            继续学习 <i class="el-icon-arrow-right"></i>
                        </el-button>
                    </div>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { marked } from 'marked';
import * as d3 from 'd3';

// 设置渲染器以支持数学公式
import 'katex/dist/katex.min.css';
// import katex from 'katex';
import katex from 'katex';
// 处理数学公式（简单例子）
function renderMath(markdown) {
    return markdown
        .replace(/\$\$([^$]+)\$\$/g, (_, expr) => katex.renderToString(expr, { displayMode: true }))
        .replace(/\$([^$]+)\$/g, (_, expr) => katex.renderToString(expr, { displayMode: false }))
}


export default {
    name: 'Section9Applications',
    data() {
        return {
            markdownContent: `
  ## UMAP的应用场景
  
  UMAP (Uniform Manifold Approximation and Projection) 凭借其优秀的性能和灵活性，已经在多个领域得到广泛应用。这些应用充分利用了UMAP在保留数据局部和全局结构方面的优势，以及它处理大规模数据集的能力。
  
  ### 1. 单细胞基因组学
  
单细胞技术的发展使得研究人员能够测量单个细胞的基因表达水平，但这会产生高维数据（通常有10,000-20,000个基因）。UMAP已成为这一领域的标准工具：

- **细胞类型鉴定**：通过可视化细胞群体，识别未知细胞类型
- **发育轨迹分析**：揭示细胞分化和发育的连续过程
- **空间转录组学**：将基因表达与细胞在组织中的空间位置结合

UMAP能够保留细胞群体之间的全局关系，同时分离不同的细胞类型，使其成为单细胞分析的理想选择。

### 2. 图像和计算机视觉

在计算机视觉领域，UMAP可用于：

- **图像嵌入可视化**：探索由深度学习模型（如CNN、自编码器）提取的图像特征
- **图像检索系统**：提高相似图像搜索的效率
- **图像集聚类和组织**：自动组织大型图像集合

UMAP能够捕捉图像之间的语义相似性，使得视觉上相似的图像在低维空间中彼此接近。

### 3. 自然语言处理

在NLP领域，UMAP可用于：

- **词嵌入可视化**：探索Word2Vec、GloVe或BERT等模型生成的词向量
- **文档聚类**：基于语义相似性组织文档集合
- **主题建模辅助**：可视化文档-主题分布

UMAP能够保留词语或文档之间的语义关系，有助于理解语言数据中的模式和结构。

### 4. 药物发现和生物信息学

在药物研发过程中，UMAP可用于：

- **化合物库可视化**：探索大型化合物库的化学空间
- **蛋白质结构比较**：分析蛋白质结构相似性
- **药物-靶点相互作用预测**：识别潜在的药物靶点

UMAP帮助研究人员在复杂的生物和化学数据中发现模式，加速药物发现过程。

### 5. 异常检测和欺诈分析

UMAP可用于金融和网络安全中的异常检测：

- **信用卡欺诈检测**：识别异常交易模式
- **网络入侵检测**：发现异常网络流量
- **用户行为分析**：识别异常用户活动

通过将高维特征投影到低维空间，UMAP可以使异常点与正常数据明显分离，便于可视化和检测。

### 6. 多组学数据整合

现代生物学研究通常涉及多种数据类型的整合：

- **多模态数据融合**：将基因组、蛋白组、代谢组等数据整合
- **跨平台数据比较**：比较不同技术平台生成的数据
- **患者亚型鉴定**：通过整合多种生物标志物识别疾病亚型

UMAP能够有效处理来自不同来源的高维数据，并在保留各数据集特性的同时找到共同结构。

### 7. 推荐系统

在推荐系统中，UMAP可用于：

- **用户偏好建模**：理解用户行为和偏好
- **内容相似性计算**：计算商品、电影、音乐等的相似性
- **冷启动问题缓解**：为新用户或新商品提供初始推荐

通过降低用户-商品交互矩阵的维度，UMAP可以揭示隐藏的偏好模式，提高推荐质量。

### 8. 音频和音乐分析

在音频处理领域，UMAP可用于：

- **音乐分类和组织**：基于声学特征组织音乐库
- **声音事件检测**：识别特定环境中的声音事件
- **音乐可视化**：创建音乐集合的可视化地图

UMAP能够捕捉声音特征之间的相似性，帮助研究人员和音乐爱好者探索声音数据。

### 9. 社交网络分析

在社交网络研究中，UMAP可用于：

- **社区检测**：发现社交网络中的社区结构
- **影响力分析**：识别网络中的关键节点
- **网络演化可视化**：跟踪社交网络随时间的变化

UMAP通过保留节点之间的关系结构，提供社交网络的直观可视化，帮助理解复杂的社会动态。

### 10. 时间序列分析

对于时间序列数据，UMAP可用于：

- **时间序列聚类**：分组相似的时间序列模式
- **异常时间段检测**：识别异常的时间序列段
- **趋势可视化**：简化复杂时间序列的表示

UMAP能够捕捉时间序列中的时序模式和结构，有助于识别隐藏在时间数据中的规律。

在实践应用中，UMAP往往结合其他技术使用，如聚类算法、分类器或更专业的领域特定工具。它的灵活性和在不同数据类型上的良好表现使其成为各领域数据科学家的重要工具。

在下面的互动演示中，您可以探索UMAP在几个具体应用场景中的实际使用效果。
      `,
            selectedApplication: null,
            applications: [
                {
                    title: "单细胞RNA测序分析",
                    icon: "el-icon-s-cooperation",
                    shortDescription: "使用UMAP分析和可视化单细胞基因表达数据",
                    detailDescription: `
            <p>单细胞RNA测序(scRNA-seq)技术允许研究人员测量数千个单个细胞的基因表达。这会产生极高维度的数据集（通常10,000-30,000个基因），需要降维以便进行可视化和分析。</p>
            <p>UMAP在这一领域表现优异，因为它能够：</p>
            <ul>
              <li>保留不同细胞类型之间的全局关系</li>
              <li>清晰分离不同的细胞类型，形成可识别的簇</li>
              <li>保留细胞分化的连续轨迹</li>
              <li>高效处理大型单细胞数据集（数十万甚至数百万个细胞）</li>
            </ul>
            <p>上图展示了一个小鼠大脑单细胞数据集的UMAP可视化。不同颜色代表不同的细胞类型，如神经元、少突胶质细胞、星形胶质细胞等。可以看到，UMAP能够清晰地分离不同细胞类型，同时保留它们之间的发育关系。</p>
          `,
                    highlights: [
                        {
                            icon: "el-icon-s-data",
                            title: "高分辨率",
                            description: "能够区分非常相似的细胞亚型，发现新的细胞类型"
                        },
                        {
                            icon: "el-icon-coordinate",
                            title: "保留轨迹",
                            description: "捕捉细胞分化和发育的连续过程，如从干细胞到成熟细胞的转变"
                        },
                        {
                            icon: "el-icon-refresh",
                            title: "批次整合",
                            description: "帮助整合和校正来自不同实验批次或技术平台的数据"
                        }
                    ],
                    codeSnippet: `
# 使用Python的scanpy包处理单细胞数据
import scanpy as sc
import numpy as np

# 读取数据
adata = sc.read_h5ad('mouse_brain.h5ad')

# 预处理
sc.pp.normalize_per_cell(adata)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var.highly_variable]

# 运行UMAP
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# 可视化结果
sc.pl.umap(adata, color='cell_type', legend_loc='on data')
          `
                },
                {
                    title: "图像特征可视化",
                    icon: "el-icon-picture",
                    shortDescription: "使用UMAP探索和组织图像集合",
                    detailDescription: `
            <p>现代计算机视觉系统通常使用深度学习模型（如CNN）提取图像的高维特征表示。UMAP可以将这些高维特征投影到2D空间，实现图像集合的直观可视化和组织。</p>
            <p>这种应用特别有用于：</p>
            <ul>
              <li>探索大型图像数据集的结构</li>
              <li>识别相似图像和异常图像</li>
              <li>评估图像分类模型的特征表示质量</li>
              <li>创建基于内容的图像检索系统</li>
            </ul>
            <p>上图展示了MNIST手写数字数据集的UMAP可视化。每个点代表一张图像，颜色表示不同的数字类别（0-9）。注意UMAP如何将相同数字的图像聚集在一起，同时保留数字之间的关系（例如，1和7在视觉上更相似，因此它们的簇也更接近）。</p>
          `,
                    highlights: [
                        {
                            icon: "el-icon-s-grid",
                            title: "语义组织",
                            description: "根据视觉内容而非仅像素相似性组织图像"
                        },
                        {
                            icon: "el-icon-search",
                            title: "内容检索",
                            description: "通过在低维空间中查找近邻实现高效的图像搜索"
                        },
                        {
                            icon: "el-icon-monitor",
                            title: "模型监控",
                            description: "可视化模型如何感知不同类别，帮助诊断分类错误"
                        }
                    ],
                    codeSnippet: `
# 使用keras和UMAP可视化MNIST数据集
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
import umap
import matplotlib.pyplot as plt

# 加载数据
(x_train, y_train), _ = mnist.load_data()

# 预处理图像 (调整大小并扩展为RGB)
x_rgb = np.stack([np.repeat(x_train[:1000, :, :, np.newaxis], 3, axis=3)], axis=0)[0]
x_rgb = np.float32(x_rgb).reshape(-1, 28, 28, 3)
x_resized = np.zeros((1000, 224, 224, 3))
for i in range(1000):
    x_resized[i] = cv2.resize(x_rgb[i], (224, 224))
x_resized = preprocess_input(x_resized)

# 使用预训练的VGG16提取特征
model = VGG16(weights='imagenet', include_top=False, pooling='avg')
features = model.predict(x_resized)

# 应用UMAP
umap_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2)
embedding = umap_reducer.fit_transform(features)

# 可视化结果
plt.figure(figsize=(12, 10))
plt.scatter(embedding[:, 0], embedding[:, 1], c=y_train[:1000], 
            cmap='Spectral', s=5)
plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
plt.title('UMAP visualization of MNIST digits')
plt.show()
          `
                },
                {
                    title: "药物发现",
                    icon: "el-icon-first-aid-kit",
                    shortDescription: "应用UMAP于药物筛选和化合物分析",
                    detailDescription: `
            <p>药物发现过程涉及筛选和分析大量化合物，寻找具有所需生物活性的候选药物。化合物通常用分子描述符或指纹表示，这些是高维特征向量。</p>
            <p>UMAP在药物发现中的应用包括：</p>
            <ul>
              <li>可视化化合物库的化学空间</li>
              <li>识别具有相似化学结构但不同生物活性的分子（活性悬崖）</li>
              <li>基于结构-活性关系指导新化合物的设计</li>
              <li>比较不同来源的化合物库</li>
              <li>选择多样化的化合物子集进行实验测试</li>
            </ul>
            <p>上图展示了一个化合物库的UMAP可视化，其中颜色表示化合物与特定靶点的亲和力。聚集的颜色区域表明化学结构和生物活性之间的关系，这有助于药物化学家识别有前景的化学骨架和优化方向。</p>
          `,
                    highlights: [
                        {
                            icon: "el-icon-collection",
                            title: "化学空间导航",
                            description: "探索大型化合物库，发现结构新颖性和多样性"
                        },
                        {
                            icon: "el-icon-connection",
                            title: "结构-活性关系",
                            description: "识别化学结构与生物活性之间的关系模式"
                        },
                        {
                            icon: "el-icon-discover",
                            title: "虚拟筛选",
                            description: "加速药物候选物的识别，减少实验测试的化合物数量"
                        }
                    ],
                    codeSnippet: `
# 使用RDKit和UMAP分析化合物库
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import pandas as pd
import umap
import matplotlib.pyplot as plt

# 读取化合物数据 (SMILES格式)
df = pd.read_csv('compounds.csv')
smiles_list = df['SMILES'].tolist()
activity = df['Activity'].values

# 计算分子指纹 (Morgan/ECFP指纹)
mols = [Chem.MolFromSmiles(s) for s in smiles_list]
fps = [AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=1024) for m in mols]
fingerprints = np.array([np.array(fp) for fp in fps])

# 应用UMAP降维
reducer = umap.UMAP(n_neighbors=30, min_dist=0.1, metric='jaccard')
embedding = reducer.fit_transform(fingerprints)

# 可视化结果，颜色表示活性
plt.figure(figsize=(12, 10))
scatter = plt.scatter(embedding[:, 0], embedding[:, 1], 
                      c=activity, cmap='viridis', s=5, alpha=0.7)
plt.colorbar(scatter, label='Binding Affinity (pIC50)')
plt.title('Chemical Space of Compound Library')
plt.show()
          `
                }
            ],
            scenarios: [
                {
                    description: "你有一个包含100万个细胞和20,000个基因的单细胞RNA测序数据集，需要可视化不同细胞类型",
                    answer: "umap",
                    explanation: "UMAP非常适合处理大型单细胞数据集，它能够有效地保留细胞类型之间的关系，同时具有处理大数据集的计算效率。"
                },
                {
                    description: "你需要对一个包含1,000个样本和50个特征的表格数据进行初步探索，快速了解数据结构",
                    answer: "pca",
                    explanation: "对于初步数据探索，尤其是样本量不大的情况，PCA是一个简单、快速、可解释的选择，它不需要参数调整，可以立即提供数据结构的概览。"
                },
                {
                    description: "你有一个神经网络生成的词嵌入矩阵，包含10,000个词和300个维度，你希望可视化词之间的语义关系",
                    answer: "umap",
                    explanation: "UMAP能够很好地保留词嵌入空间中的局部和全局语义结构，使得相似含义的词在可视化中聚集在一起，是词嵌入可视化的优秀选择。"
                },
                {
                    description: "你正在分析金融交易数据，希望检测异常交易，数据集包含100万条交易记录和100个特征",
                    answer: "isolation_forest",
                    explanation: "虽然UMAP可用于异常检测的可视化，但Isolation Forest是专门为异常检测设计的算法，特别适合处理大型高维数据，是这种场景的更直接选择。"
                },
                {
                    description: "你需要将图像特征压缩到较低维度，以便在移动设备上进行实时图像检索，要求算法执行速度快",
                    answer: "pca",
                    explanation: "对于需要速度和确定性的实时应用，特别是在资源受限的环境中，PCA是更好的选择。它计算简单，结果确定，且在降维后可以快速计算欧氏距离。"
                }
            ],
            matchOptions: [
                { value: "pca", label: "PCA (主成分分析)" },
                { value: "tsne", label: "t-SNE" },
                { value: "umap", label: "UMAP" },
                { value: "isolation_forest", label: "Isolation Forest" },
                { value: "kmeans", label: "K-means聚类" }
            ],
            userMatches: [],
            matchResults: [],
            quizCompleted: false,
            allCorrect: false,
            retries: 0,
            isCompleted: false
        }
    },
    computed: {
        renderedContent() {
            const withMath = renderMath(this.markdownContent)
            return marked(withMath)
        },
        isAllMatched() {
            return this.userMatches.length === this.scenarios.length &&
                !this.userMatches.includes(undefined);
        },
        quizFeedbackTitle() {
            return this.allCorrect ? '恭喜！所有匹配正确！' : '匹配完成';
        },
        quizFeedbackDescription() {
            if (this.allCorrect) {
                return '您已经很好地理解了UMAP和其他方法的适用场景。这种理解对于在实际项目中选择合适的技术非常重要。';
            } else {
                const correctCount = this.matchResults.filter(result => result).length;
                return `您正确匹配了${correctCount}个场景（共${this.scenarios.length}个）。请查看下方的详细解释，了解每种方法的最佳应用场景。`;
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(9);
        }
    },
    methods: {
        selectApplication(index) {
            if (this.selectedApplication === index) {
                // 如果点击当前选中项，则取消选择
                this.selectedApplication = null;
            } else {
                this.selectedApplication = index;

                // 延迟创建可视化，确保DOM已更新
                this.$nextTick(() => {
                    this.createApplicationVisualization();
                });
            }
        },
        createApplicationVisualization() {
            if (!this.$refs.applicationViz) return;

            const width = this.$refs.applicationViz.clientWidth;
            const height = 300;

            // 清除现有SVG
            d3.select(this.$refs.applicationViz).selectAll("*").remove();

            const svg = d3.select(this.$refs.applicationViz)
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // 根据选定的应用场景生成不同的可视化
            switch (this.selectedApplication) {
                case 0:
                    this.createSingleCellVisualization(svg, width, height);
                    break;
                case 1:
                    this.createImageVisualization(svg, width, height);
                    break;
                case 2:
                    this.createDrugDiscoveryVisualization(svg, width, height);
                    break;
                default:
                    // 默认空可视化
                    svg.append("text")
                        .attr("x", width / 2)
                        .attr("y", height / 2)
                        .attr("text-anchor", "middle")
                        .attr("font-size", "14px")
                        .text("请选择一个应用场景查看可视化");
            }
        },

        createSingleCellVisualization(svg, width, height) {
            // 模拟单细胞RNA-seq数据的UMAP可视化
            const numCellTypes = 8;
            const cellsPerType = 100;
            const points = [];

            // 生成不同的细胞类型簇
            const cellTypeColors = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
                "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
            ];

            // 细胞类型位置 - 模拟一些混合的分化谱系
            const typePositions = [
                { x: width * 0.3, y: height * 0.3, spread: 30 },   // 类型1
                { x: width * 0.3, y: height * 0.5, spread: 25 },   // 类型2
                { x: width * 0.3, y: height * 0.7, spread: 25 },   // 类型3
                { x: width * 0.5, y: height * 0.3, spread: 30 },   // 类型4
                { x: width * 0.5, y: height * 0.7, spread: 25 },   // 类型5
                { x: width * 0.7, y: height * 0.3, spread: 20 },   // 类型6
                { x: width * 0.7, y: height * 0.5, spread: 25 },   // 类型7
                { x: width * 0.7, y: height * 0.7, spread: 30 }    // 类型8
            ];

            // 生成每种细胞类型的点
            for (let type = 0; type < numCellTypes; type++) {
                const position = typePositions[type];

                for (let i = 0; i < cellsPerType; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const r = Math.random() * position.spread;

                    points.push({
                        x: position.x + Math.cos(angle) * r,
                        y: position.y + Math.sin(angle) * r,
                        cellType: type,
                        color: cellTypeColors[type]
                    });
                }
            }

            // 添加一些连接线，表示发育轨迹
            const trajectories = [
                { source: 0, target: 1 },
                { source: 1, target: 2 },
                { source: 0, target: 3 },
                { source: 3, target: 4 },
                { source: 3, target: 5 },
                { source: 5, target: 6 },
                { source: 6, target: 7 }
            ];

            // 绘制轨迹连接线
            trajectories.forEach(t => {
                const source = typePositions[t.source];
                const target = typePositions[t.target];

                svg.append("line")
                    .attr("x1", source.x)
                    .attr("y1", source.y)
                    .attr("x2", target.x)
                    .attr("y2", target.y)
                    .attr("stroke", "#ddd")
                    .attr("stroke-width", 5)
                    .attr("stroke-opacity", 0.5)
                    .attr("stroke-dasharray", "5,5");
            });

            // 绘制细胞点
            svg.selectAll("circle")
                .data(points)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 3)
                .attr("fill", d => d.color)
                .attr("opacity", 0.7)
                .attr("stroke", "#fff")
                .attr("stroke-width", 0.5);

            // 添加细胞类型标签
            for (let type = 0; type < numCellTypes; type++) {
                const position = typePositions[type];

                svg.append("text")
                    .attr("x", position.x)
                    .attr("y", position.y - position.spread - 5)
                    .attr("text-anchor", "middle")
                    .attr("font-size", "12px")
                    .attr("font-weight", "bold")
                    .attr("fill", cellTypeColors[type])
                    .text(`细胞类型 ${type + 1}`);
            }

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .text("小鼠大脑单细胞RNA-seq数据UMAP可视化");
        },

        createImageVisualization(svg, width, height) {
            // 模拟MNIST数字图像的UMAP投影
            const numDigits = 10;
            const samplesPerDigit = 50;
            const points = [];

            // 数字类别的颜色
            const digitColors = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
            ];

            // 创建数字类别的布局 - 一些数字类别的簇更接近（如1和7）
            const digitPositions = [
                { x: width * 0.5, y: height * 0.25 },  // 0
                { x: width * 0.25, y: height * 0.4 },  // 1
                { x: width * 0.65, y: height * 0.5 },  // 2
                { x: width * 0.75, y: height * 0.65 }, // 3
                { x: width * 0.4, y: height * 0.7 },   // 4
                { x: width * 0.6, y: height * 0.4 },   // 5
                { x: width * 0.3, y: height * 0.6 },   // 6
                { x: width * 0.35, y: height * 0.3 },  // 7
                { x: width * 0.7, y: height * 0.3 },   // 8
                { x: width * 0.5, y: height * 0.7 }    // 9
            ];

            // 生成每个数字类别的点
            for (let digit = 0; digit < numDigits; digit++) {
                const position = digitPositions[digit];

                for (let i = 0; i < samplesPerDigit; i++) {
                    // 添加一些随机性，形成簇
                    const angle = Math.random() * Math.PI * 2;
                    const r = Math.random() * 20;

                    points.push({
                        x: position.x + Math.cos(angle) * r,
                        y: position.y + Math.sin(angle) * r,
                        digit: digit,
                        color: digitColors[digit]
                    });
                }
            }

            // 绘制点
            svg.selectAll("circle")
                .data(points)
                .enter()
                .append("circle")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 3.5)
                .attr("fill", d => d.color)
                .attr("opacity", 0.7)
                .attr("stroke", "#fff")
                .attr("stroke-width", 0.5);

            // 添加数字标签
            for (let digit = 0; digit < numDigits; digit++) {
                const position = digitPositions[digit];

                svg.append("text")
                    .attr("x", position.x)
                    .attr("y", position.y)
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "middle")
                    .attr("font-size", "16px")
                    .attr("font-weight", "bold")
                    .attr("fill", digitColors[digit])
                    .text(digit);
            }

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .text("MNIST手写数字UMAP可视化");

            // 添加说明
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", height - 10)
                .attr("text-anchor", "middle")
                .attr("font-size", "12px")
                .text("注意数字1和7的簇较为接近，反映它们的视觉相似性");
        },

        createDrugDiscoveryVisualization(svg, width, height) {
            // 模拟化合物库的UMAP可视化
            const numCompounds = 300;
            const points = [];

            // 生成化学空间中的几个区域，代表不同化学骨架
            const scaffolds = [
                { x: width * 0.3, y: height * 0.3, radius: 60, activityRange: [0.7, 0.9] },
                { x: width * 0.7, y: height * 0.3, radius: 50, activityRange: [0.3, 0.5] },
                { x: width * 0.3, y: height * 0.7, radius: 50, activityRange: [0.1, 0.3] },
                { x: width * 0.7, y: height * 0.7, radius: 60, activityRange: [0.5, 0.7] },
                { x: width * 0.5, y: height * 0.5, radius: 40, activityRange: [0.8, 1.0] }
            ];

            // 为每个区域生成化合物点
            scaffolds.forEach((scaffold, index) => {
                const compoundsInScaffold = Math.floor(numCompounds / scaffolds.length) +
                    (index < numCompounds % scaffolds.length ? 1 : 0);

                for (let i = 0; i < compoundsInScaffold; i++) {
                    // 化合物在骨架区域内的分布
                    const angle = Math.random() * Math.PI * 2;
                    const r = Math.random() * scaffold.radius;

                    // 活性值在范围内随机
                    const minActivity = scaffold.activityRange[0];
                    const maxActivity = scaffold.activityRange[1];
                    const activity = minActivity + Math.random() * (maxActivity - minActivity);

                    points.push({
                        x: scaffold.x + Math.cos(angle) * r,
                        y: scaffold.y + Math.sin(angle) * r,
                        scaffold: index,
                        activity: activity
                    });
                }
            });

            // 创建活性颜色比例尺
            const colorScale = d3.scaleSequential(d3.interpolateViridis)
                .domain([0, 1]);

            // 绘制骨架区域
            svg.selectAll("circle.scaffold")
                .data(scaffolds)
                .enter()
                .append("circle")
                .attr("class", "scaffold")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", d => d.radius)
                .attr("fill", "none")
                .attr("stroke", "#999")
                .attr("stroke-width", 1)
                .attr("stroke-dasharray", "3,3");

            // 绘制化合物点
            svg.selectAll("circle.compound")
                .data(points)
                .enter()
                .append("circle")
                .attr("class", "compound")
                .attr("cx", d => d.x)
                .attr("cy", d => d.y)
                .attr("r", 4)
                .attr("fill", d => colorScale(d.activity))
                .attr("opacity", 0.8)
                .attr("stroke", "#fff")
                .attr("stroke-width", 0.5);

            // 添加骨架标签
            scaffolds.forEach((scaffold, index) => {
                svg.append("text")
                    .attr("x", scaffold.x)
                    .attr("y", scaffold.y - scaffold.radius - 5)
                    .attr("text-anchor", "middle")
                    .attr("font-size", "12px")
                    .attr("font-weight", "bold")
                    .text(`化学骨架 ${index + 1}`);
            });

            // 添加标题
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", 20)
                .attr("text-anchor", "middle")
                .attr("font-size", "14px")
                .attr("font-weight", "bold")
                .text("化合物库UMAP可视化 - 颜色表示靶点亲和力");

            // 添加颜色图例
            const legendWidth = 150;
            const legendHeight = 15;
            const legendX = width - legendWidth - 20;
            const legendY = height - 40;

            // 创建线性渐变
            const defs = svg.append("defs");
            const linearGradient = defs.append("linearGradient")
                .attr("id", "activity-gradient")
                .attr("x1", "0%")
                .attr("y1", "0%")
                .attr("x2", "100%")
                .attr("y2", "0%");

            // 添加渐变颜色停止点
            const stops = [0, 0.2, 0.4, 0.6, 0.8, 1];
            stops.forEach(stop => {
                linearGradient.append("stop")
                    .attr("offset", `${stop * 100}%`)
                    .attr("stop-color", colorScale(stop));
            });

            // 绘制图例矩形
            svg.append("rect")
                .attr("x", legendX)
                .attr("y", legendY)
                .attr("width", legendWidth)
                .attr("height", legendHeight)
                .style("fill", "url(#activity-gradient)");

            // 添加图例标题
            svg.append("text")
                .attr("x", legendX + legendWidth / 2)
                .attr("y", legendY - 5)
                .attr("text-anchor", "middle")
                .attr("font-size", "10px")
                .text("靶点亲和力");

            // 添加图例刻度
            const legendScale = d3.scaleLinear()
                .domain([0, 1])
                .range([legendX, legendX + legendWidth]);

            stops.forEach(stop => {
                svg.append("text")
                    .attr("x", legendScale(stop))
                    .attr("y", legendY + legendHeight + 12)
                    .attr("text-anchor", "middle")
                    .attr("font-size", "9px")
                    .text(stop.toFixed(1));
            });
        },

        checkMatches() {
            this.quizCompleted = true;
            this.matchResults = this.scenarios.map(
                (scenario, i) => this.userMatches[i] === scenario.answer
            );
            this.allCorrect = this.matchResults.every(result => result);

            if (this.allCorrect || ++this.retries >= 1) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetQuiz() {
            this.quizCompleted = false;
            this.userMatches = [];
            this.matchResults = [];
        },

        getOptionLabel(value) {
            const option = this.matchOptions.find(opt => opt.value === value);
            return option ? option.label : '未选择';
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    }
}
</script>

<style scoped>
.section-container {
    margin-bottom: 40px;
}

.section-card {
    margin-bottom: 20px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.markdown-content {
    margin-bottom: 30px;
}

.interaction-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 4px;
    margin-top: 20px;
}

.application-cards {
    margin: 20px 0;
}

.application-card {
    height: 180px;
    cursor: pointer;
    transition: all 0.3s;
    margin-bottom: 20px;
}

.application-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.application-card.active {
    border-color: #409EFF;
    box-shadow: 0 5px 15px rgba(64, 158, 255, 0.2);
}

.card-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
}

.app-icon {
    font-size: 36px;
    color: #409EFF;
    margin-bottom: 15px;
    margin-top: 10px;
}

.card-content h4 {
    margin: 0 0 10px;
    text-align: center;
    color: #303133;
}

.card-content p {
    text-align: center;
    color: #606266;
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.4;
}

.application-detail {
    margin-top: 30px;
}

.detail-content {
    padding: 20px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-content h3 {
    margin-top: 0;
    margin-bottom: 20px;
    color: #409EFF;
    text-align: center;
}

.application-viz {
    width: 100%;
    height: 300px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 20px;
}

.detail-text {
    margin-bottom: 20px;
    line-height: 1.6;
}

.application-highlights {
    margin: 20px 0;
}

.application-highlights h4 {
    margin-bottom: 15px;
    color: #303133;
}

.highlight-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
    height: 100%;
}

.highlight-item i {
    font-size: 24px;
    color: #409EFF;
    margin-right: 15px;
    margin-top: 5px;
}

.highlight-text {
    flex: 1;
}

.highlight-text h5 {
    margin: 0 0 5px;
    color: #303133;
}

.highlight-text p {
    margin: 0;
    color: #606266;
    font-size: 0.9rem;
    line-height: 1.4;
}

.application-implementation {
    margin: 20px 0;
}

.application-implementation h4 {
    margin-bottom: 15px;
    color: #303133;
}

.code-snippet {
    margin: 0;
    white-space: pre-wrap;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.9rem;
    line-height: 1.4;
}

.quiz-container {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px dashed #dcdfe6;
}

.match-quiz {
    margin-top: 20px;
}

.scenario-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.scenario-desc {
    flex: 1;
    display: flex;
    align-items: flex-start;
    margin-right: 20px;
}

.scenario-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background-color: #409EFF;
    color: white;
    border-radius: 50%;
    margin-right: 10px;
    font-size: 0.9rem;
    font-weight: bold;
}

.scenario-desc p {
    margin: 0;
    line-height: 1.4;
}

.submit-btn {
    margin-top: 20px;
}

.response-container {
    margin-top: 20px;
}

.match-results {
    margin-top: 20px;
    padding: 15px;
    background-color: #f2f6fc;
    border-radius: 4px;
}

.match-result-item {
    margin-bottom: 15px;
}

.explanation {
    margin-top: 5px;
    margin-left: 20px;
    color: #606266;
    font-size: 0.9rem;
}

.retry-btn {
    margin-top: 15px;
}

.next-section {
    margin-top: 20px;
    text-align: center;
}

/* 全局样式适配 */
:deep(h2) {
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    margin-top: 20px;
}

:deep(blockquote) {
    border-left: 4px solid #409EFF;
    padding-left: 15px;
    color: #606266;
    margin: 20px 0;
}

:deep(p) {
    line-height: 1.6;
}

:deep(strong) {
    color: #409EFF;
}

:deep(ul),
:deep(ol) {
    padding-left: 20px;
    line-height: 1.6;
}
</style>