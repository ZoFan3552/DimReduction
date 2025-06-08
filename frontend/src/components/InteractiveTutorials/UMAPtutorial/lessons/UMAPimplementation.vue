<template>
    <div class="section-container">
        <el-card class="section-card">
            <div slot="header" class="section-header">
                <h2>10. UMAP的实现与优化</h2>
                <el-tag v-if="isCompleted" type="success">已完成</el-tag>
            </div>

            <!-- Markdown展示部分 -->
            <div class="markdown-content" v-html="renderedContent"></div>

            <!-- 互动部分 - 代码示例和性能优化 -->
            <div class="interaction-container">
                <h3>UMAP实现与性能优化案例</h3>
                <p>下面展示了不同编程语言和库中UMAP的实现，以及常见的性能优化方法。查看代码示例并了解如何根据不同场景优化UMAP。</p>

                <el-tabs v-model="activeTab" type="border-card">
                    <el-tab-pane label="Python实现" name="python">
                        <div class="code-example-container">
                            <h4>Python中的UMAP实现</h4>
                            <p>Python是UMAP最常用的实现语言，主要通过<code>umap-learn</code>库。以下是基本用法示例：</p>

                            <div class="code-to-fix">
                                <pre><code class="language-python">import numpy as np
  import umap
  import matplotlib.pyplot as plt
  from sklearn.datasets import load_digits
  
  # 加载示例数据集
  digits = load_digits()
  data = digits.data
  labels = digits.target
  
  # 创建UMAP模型并进行降维
  reducer = umap.UMAP(
      n_neighbors=15,     # 邻居数量
      min_dist=0.1,       # 最小距离
      n_components=2,     # 目标维度
      metric='euclidean'  # 距离度量
  )
  embedding = reducer.fit_transform(data)
  
  # 可视化结果
  plt.figure(figsize=(12, 10))
  plt.scatter(
      embedding[:, 0],
      embedding[:, 1],
      c=labels,
      cmap='Spectral',
      s=5
  )
  plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
  plt.title('UMAP projection of the Digits dataset')
  plt.show()</code></pre>
                            </div>

                            <h4>Python性能优化技巧</h4>
                            <ul>
                                <li><strong>使用Rapids UMAP</strong>：对于大型数据集，可以使用支持GPU加速的Rapids UMAP实现：</li>
                            </ul>

                            <div class="code-to-fix">
                                <pre><code class="language-python"># 使用Rapids UMAP进行GPU加速
  import cudf
  import cuml
  from cuml.manifold import UMAP
  
  # 将数据转换为GPU格式
  gdf = cudf.DataFrame.from_pandas(pd.DataFrame(data))
  
  # 使用GPU加速的UMAP
  g_reducer = cuml.manifold.UMAP(n_neighbors=15, min_dist=0.1)
  embedding = g_reducer.fit_transform(gdf)</code></pre>
                            </div>

                            <ul>
                                <li><strong>稀疏矩阵</strong>：对于高维稀疏数据，使用稀疏矩阵格式可以提高效率：</li>
                            </ul>

                            <div class="code-to-fix">
                                <pre><code class="language-python">from scipy import sparse
  
  # 将数据转换为稀疏格式
  sparse_data = sparse.csr_matrix(data)
  
  # UMAP可以直接处理稀疏矩阵
  sparse_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1)
  sparse_embedding = sparse_reducer.fit_transform(sparse_data)</code></pre>
                            </div>
                        </div>
                    </el-tab-pane>

                    <el-tab-pane label="R实现" name="r">
                        <div class="code-example-container">
                            <h4>R中的UMAP实现</h4>
                            <p>R语言中可以通过<code>uwot</code>包实现UMAP算法：</p>

                            <div class="code-to-fix">
                                <pre><code class="language-r"># 安装并加载必要的包
  install.packages("uwot")
  library(uwot)
  library(ggplot2)
  
  # 加载示例数据集
  data(iris)
  iris_data &lt;- iris[, 1:4]
  iris_labels &lt;- iris[, 5]
  
  # 使用UMAP进行降维
  iris_umap &lt;- umap(
    iris_data,
    n_neighbors = 15,
    min_dist = 0.1,
    n_components = 2,
    metric = "euclidean"
  )
  
  # 将结果组合成数据框
  umap_df &lt;- data.frame(
    x = iris_umap[, 1],
    y = iris_umap[, 2],
    species = iris_labels
  )
  
  # 可视化结果
  ggplot(umap_df, aes(x, y, color = species)) +
    geom_point(size = 3, alpha = 0.7) +
    theme_minimal() +
    labs(title = "UMAP projection of the Iris dataset")</code></pre>
                            </div>

                            <h4>R性能优化技巧</h4>
                            <ul>
                                <li><strong>并行计算</strong>：利用<code>uwot</code>包的并行计算功能：</li>
                            </ul>

                            <div class="code-to-fix">
                                <pre><code class="language-r"># 使用并行计算加速UMAP计算
  iris_umap_parallel &lt;- umap(
    iris_data,
    n_neighbors = 15,
    min_dist = 0.1,
    n_components = 2,
    n_threads = 4,  # 使用4个线程进行并行计算
    metric = "euclidean"
  )</code></pre>
                            </div>
                        </div>
                    </el-tab-pane>

                    <el-tab-pane label="性能优化" name="optimization">
                        <div class="code-example-container">
                            <h4>UMAP性能优化策略</h4>
                            <p>针对大型数据集，有多种方法可以提高UMAP的性能：</p>

                            <div class="optimization-card">
                                <div class="opt-header">
                                    <i class="el-icon-data-analysis"></i>
                                    <h5>降低数据维度</h5>
                                </div>
                                <p>在应用UMAP之前，先使用PCA等线性方法降低数据维度可以显著提高性能：</p>
                                <div class="code-to-fix">
                                    <pre><code class="language-python">from sklearn.decomposition import PCA
  
  # 首先使用PCA将维度降至50
  pca = PCA(n_components=50)
  data_pca = pca.fit_transform(data)
  
  # 然后应用UMAP
  reducer = umap.UMAP(n_neighbors=15, min_dist=0.1)
  embedding = reducer.fit_transform(data_pca)</code></pre>
                                </div>
                            </div>

                            <div class="optimization-card">
                                <div class="opt-header">
                                    <i class="el-icon-cpu"></i>
                                    <h5>参数调整</h5>
                                </div>
                                <p>调整关键参数可以在性能和结果质量之间取得平衡：</p>
                                <ul>
                                    <li><strong>n_neighbors</strong>：较小的值计算更快，但可能丢失全局结构</li>
                                    <li><strong>metric</strong>：某些距离度量计算更高效，如欧几里得距离</li>
                                    <li><strong>n_epochs</strong>：减少迭代次数可以加快计算，但可能影响结果质量</li>
                                </ul>
                                <div class="code-to-fix">
                                    <pre><code class="language-python"># 调整参数以优化性能
  fast_reducer = umap.UMAP(
      n_neighbors=10,     # 减少邻居数量
      metric='euclidean', # 使用高效的距离度量
      n_epochs=200,       # 减少迭代次数
      low_memory=True     # 减少内存使用
  )</code></pre>
                                </div>
                            </div>

                            <div class="optimization-card">
                                <div class="opt-header">
                                    <i class="el-icon-connection"></i>
                                    <h5>分块处理与增量学习</h5>
                                </div>
                                <p>对于特别大的数据集，可以考虑分块处理或增量方法：</p>
                                <div class="code-to-fix">
                                    <pre><code class="language-python"># 首先在数据子集上训练UMAP模型
  subset_size = 10000
  subset_indices = np.random.choice(data.shape[0], subset_size, replace=False)
  subset_data = data[subset_indices]
  
  reducer = umap.UMAP(n_neighbors=15, min_dist=0.1)
  _ = reducer.fit(subset_data)
  
  # 然后将剩余数据转换到同一嵌入空间
  remaining_indices = np.setdiff1d(np.arange(data.shape[0]), subset_indices)
  remaining_data = data[remaining_indices]
  remaining_embedding = reducer.transform(remaining_data)
  
  # 合并结果
  subset_embedding = reducer.embedding_
  full_embedding = np.zeros((data.shape[0], 2))
  full_embedding[subset_indices] = subset_embedding
  full_embedding[remaining_indices] = remaining_embedding</code></pre>
                                </div>
                            </div>

                            <div class="performance-comparison">
                                <h4>性能比较</h4>
                                <p>不同优化策略的性能比较（基于100,000个样本，1,000个特征的数据集）：</p>

                                <el-table :data="performanceData" style="width: 100%" border>
                                    <el-table-column prop="method" label="方法" width="250"></el-table-column>
                                    <el-table-column prop="time" label="运行时间"></el-table-column>
                                    <el-table-column prop="memory" label="内存使用"></el-table-column>
                                    <el-table-column prop="quality" label="结果质量">
                                        <template slot-scope="scope">
                                            <el-rate v-model="scope.row.quality" disabled show-score></el-rate>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>
                        </div>
                    </el-tab-pane>
                </el-tabs>

                <!-- 互动测验：代码修复挑战 -->
                <div class="quiz-container" v-if="!quizCompleted">
                    <h4>代码修复挑战</h4>
                    <p>以下UMAP代码片段中包含一些常见错误或性能问题。请找出并修复这些问题：</p>


                    <div class="code-to-fix">
                        <pre><code class="language-python">import umap
                import numpy as np
                from sklearn.datasets import load_digits

                # 加载数据
                digits = load_digits()
                data = digits.data

                # 创建UMAP模型
                reducer = umap.UMAP(
                n_neighbors=5, # [问题 1]
                min_dist=0, # [问题 2]
                n_components=2,
                metric='manhattan' # [问题 3]
                )

                # 应用UMAP
                embedding = reducer.transform(data) # [问题 4]

                # 可视化结果
                import matplotlib.pyplot as plt
                plt.figure(figsize=(10, 8))
                plt.scatter(embedding[:, 0], embedding[:, 1])
                plt.show()
            </code></pre>

                        <!-- <div class="code-to-fix">
                            <pre><code class="language-python">import umap
                    import numpy as np
                    from sklearn.datasets import load_digits

                    # 加载数据
                    digits = load_digits()
                    data = digits.data

                    # 创建UMAP模型
                    reducer = umap.UMAP(
                    n_neighbors=5, # [问题 1]
                    min_dist=0, # [问题 2]
                    n_components=2,
                    metric='manhattan' # [问题 3]
                    )

                    # 应用UMAP
                    embedding = reducer.transform(data) # [问题 4]

                    # 可视化结果
                    import matplotlib.pyplot as plt
                    plt.figure(figsize=(10, 8))
                    plt.scatter(embedding[:, 0], embedding[:, 1])
                    plt.show()</code></pre>
                        </div> -->

                        <div class="problem-list">
                            <p>请选择每个标记问题的正确修复方法：</p>

                            <div v-for="(problem, index) in problems" :key="index" class="problem-item">
                                <p><strong>问题 {{ index + 1 }}:</strong> {{ problem.description }}</p>
                                <el-radio-group v-model="userFixes[index]">
                                    <el-radio v-for="(option, optIndex) in problem.options" :key="optIndex"
                                        :label="optIndex" class="fix-option">
                                        {{ option }}
                                    </el-radio>
                                </el-radio-group>
                            </div>

                            <el-button type="primary" @click="checkCodeFixes" :disabled="!isAllFixed"
                                class="submit-btn">
                                提交修复
                            </el-button>
                        </div>
                    </div>
                </div>

                <!-- 回应部分 -->
                <div v-if="quizCompleted" class="response-container">
                    <el-alert :title="quizFeedbackTitle" :type="allCorrect ? 'success' : 'warning'"
                        :description="quizFeedbackDescription" show-icon>
                    </el-alert>

                    <div v-if="!allCorrect" class="fix-results">
                        <h4>修复结果:</h4>
                        <div v-for="(problem, index) in problems" :key="index" class="fix-result-item">
                            <p>
                                <strong>问题 {{ index + 1 }}: {{ problem.description }}</strong>
                                <el-tag size="small" :type="fixResults[index] ? 'success' : 'danger'">
                                    {{ fixResults[index] ? '正确' : '错误' }}
                                </el-tag>
                            </p>
                            <p v-if="!fixResults[index]" class="explanation">
                                您的选择: {{ problem.options[userFixes[index]] }}<br>
                                正确答案: {{ problem.options[problem.answer] }}<br>
                                解释: {{ problem.explanation }}
                            </p>
                        </div>

                        <el-button type="info" @click="resetQuiz" class="retry-btn">
                            重新尝试
                        </el-button>
                    </div>

                    <div v-if="allCorrect || retries >= 1" class="next-section">
                        <p>🎉 您已完成UMAP实现与优化部分！可以继续学习最后的案例分析部分。</p>
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
    name: 'Section10Implementation',
    data() {
        return {
            markdownContent: `
## UMAP的实现与优化

UMAP (Uniform Manifold Approximation and Projection) 作为一种强大的降维算法，已经在多种编程语言和环境中得到实现。本节将介绍UMAP的主要实现方式、性能优化策略，以及在实际项目中的最佳实践。

### 主要实现库

#### 1. Python: umap-learn

官方的Python实现是最完整、最广泛使用的UMAP库：

- **GitHub**: [umap-learn](https://github.com/lmcinnes/umap)
- **安装**: \`pip install umap-learn\`
- **特点**:
  - 提供完整的UMAP算法实现
  - 支持监督、半监督和无监督模式
  - 集成了scikit-learn接口风格（fit/transform方法）
  - 提供了高级功能，如参数自动调优、标签传播等

Python的UMAP实现使用Numba进行即时编译加速，这使得它在CPU上的性能相当好，即使处理较大的数据集。

#### 2. R: uwot

R语言的UMAP实现主要通过uwot包提供：

- **CRAN**: [uwot](https://cran.r-project.org/web/packages/uwot/index.html)
- **安装**: \`install.packages("uwot")\`
- **特点**:
  - 提供与umap-learn相似的功能
  - 集成了R语言生态系统
  - 支持多线程计算

#### 3. 基于GPU的实现

对于大规模数据集，GPU加速版本提供了显著的性能提升：

- **RAPIDS cuML**: 提供CUDA加速的UMAP实现
- **适用场景**:
  - 超大型数据集（百万级样本）
  - 计算资源有GPU可用
  - 对计算速度有较高要求

### 实现细节与优化

#### 1. K近邻图构建

最耗时的步骤通常是构建K近邻图，优化策略包括：

- **使用近似最近邻算法**:
  - Annoy (Approximate Nearest Neighbors Oh Yeah)
  - HNSW (Hierarchical Navigable Small World)
  - 这些方法以牺牲少量精度为代价，显著提高大型数据集上的性能

- **空间索引结构**:
  - 使用KD树、Ball树等数据结构加速邻居搜索
  - 对于低维到中等维度的数据特别有效

#### 2. 内存优化

处理大型数据集时，内存管理变得关键：

- **稀疏表示**:
  - 对于高度稀疏的数据（如文本向量），使用稀疏矩阵格式
  - 可以通过scipy.sparse在Python中实现

- **数据类型优化**:
  - 使用单精度浮点数(float32)而非双精度(float64)
  - 对于整数特征，选择适当的整数类型(int8/int16/int32)

- **增量处理**:
  - 对特别大的数据集，使用批处理或增量学习策略
  - 先在数据子集上训练，然后使用transform方法处理剩余数据

#### 3. 计算加速策略

除了近似最近邻和GPU计算外，还有其他加速策略：

- **降维预处理**:
  - 先使用PCA等线性方法降至中等维度(如50-100维)
  - 然后再应用UMAP，这样可显著提高性能且几乎不影响结果

- **参数调优**:
  - \`n_neighbors\` 参数较小时计算更快，但可能影响全局结构保留
  - \`n_epochs\` 参数控制优化迭代次数，减少可加快计算，但可能影响结果质量
  - 某些距离度量比其他的计算更高效

### 实际应用中的最佳实践

#### 1. 数据预处理

- **标准化/归一化**:
  - 确保数据的不同特征在相似的尺度上
  - 对于欧几里得距离特别重要

- **异常值处理**:
  - 检测并处理异常值，避免它们过度影响结果
  - 考虑使用稳健的缩放方法，如MinMaxScaler或RobustScaler

- **降噪**:
  - 对于噪声较大的数据，考虑使用主成分分析(PCA)等方法进行降噪
  - 或调整UMAP的\`min_dist\`参数以控制局部噪声敏感性

#### 2. 可视化增强

- **交互式可视化**:
  - 使用工具如Plotly或Bokeh创建交互式UMAP可视化
  - 允许缩放、悬停信息和颜色编码

- **多视图集成**:
  - 将UMAP结果与其他可视化（如平行坐标、热图）结合
  - 提供数据的多角度视图

#### 3. 模型持久化

- **保存和加载模型**:
  - 使用Python的pickle或joblib保存训练好的UMAP模型
  - 允许在新数据上重用相同的变换

- **嵌入管道**:
  - 将UMAP集成到scikit-learn管道中
  - 确保一致的数据预处理和转换

### 常见问题与解决方案

- **维度诅咒**:
  - 对于非常高维的数据(>1000维)，先使用PCA等降至中等维度

- **内存错误**:
  - 使用\`low_memory=True\`参数减少内存占用
  - 考虑使用稀疏矩阵或分块处理

- **结果不稳定**:
  - 设置固定的\`random_state\`参数确保结果可复现
  - 考虑增加\`n_epochs\`参数提高优化质量

- **计算瓶颈**:
  - 识别性能瓶颈（通常是KNN计算）
  - 考虑使用GPU加速或近似KNN算法

在下面的交互部分，您将看到不同语言中UMAP的具体实现示例，以及针对性能优化的最佳实践和技巧。
      `,
            activeTab: 'python',
            performanceData: [
                {
                    method: '标准UMAP',
                    time: '15分钟',
                    memory: '4.2 GB',
                    quality: 5
                },
                {
                    method: 'PCA预处理 + UMAP',
                    time: '3分钟',
                    memory: '2.8 GB',
                    quality: 4.5
                },
                {
                    method: '近似最近邻 (Annoy)',
                    time: '5分钟',
                    memory: '3.5 GB',
                    quality: 4
                },
                {
                    method: 'GPU加速 (RAPIDS)',
                    time: '45秒',
                    memory: '5.8 GB',
                    quality: 5
                },
                {
                    method: '分块处理',
                    time: '7分钟',
                    memory: '1.2 GB',
                    quality: 3.5
                }
            ],
            problems: [
                {
                    description: "n_neighbors值设置过小 (n_neighbors=5)",
                    options: [
                        "保持n_neighbors=5不变，对于小数据集这是合适的",
                        "将n_neighbors增加到15-30，以更好地捕捉全局结构",
                        "将n_neighbors设置为更小值如2，提高算法速度"
                    ],
                    answer: 1,
                    explanation: "n_neighbors值过小会导致UMAP过度关注局部结构，难以捕捉数据的全局模式。对于大多数数据集，推荐使用15-30的值。"
                },
                {
                    description: "min_dist设置为0",
                    options: [
                        "保持min_dist=0不变，这是最优设置",
                        "将min_dist设置为负值，如-0.1，增强聚类效果",
                        "将min_dist调整到0.1-0.5范围内，避免点过度重叠"
                    ],
                    answer: 2,
                    explanation: "min_dist=0会导致点过度重叠，难以区分。虽然技术上允许为0，但通常建议设置为0.1-0.5之间的值，以获得更好的可视化效果。"
                },
                {
                    description: "使用manhattan距离度量",
                    options: [
                        "更改为euclidean距离，这是UMAP的默认和最常用度量",
                        "保持manhattan不变，这对于UMAP是合适的",
                        "更改为cosine距离，这对所有数据类型都更好"
                    ],
                    answer: 0,
                    explanation: "虽然UMAP支持多种距离度量，但euclidean（欧几里得距离）是默认和最常用的。对于一般用途，euclidean通常是最佳起点，而manhattan可能不适合捕捉某些类型的数据结构。"
                },
                {
                    description: "直接使用reducer.transform(data)而不先fit",
                    options: [
                        "这是正确的用法，不需要更改",
                        "应改为reducer.fit_transform(data)，combine好处理",
                        "应先使用reducer.fit(data)，再使用reducer.transform(data)"
                    ],
                    answer: 1,
                    explanation: "UMAP遵循scikit-learn的API，需要先拟合模型再进行转换。对于首次处理数据，应使用fit_transform()方法，它等同于先调用fit()再调用transform()。直接调用transform()而不先fit会导致错误。"
                }
            ],
            userFixes: [],
            fixResults: [],
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
        isAllFixed() {
            return this.userFixes.length === this.problems.length &&
                !this.userFixes.includes(undefined);
        },
        quizFeedbackTitle() {
            return this.allCorrect ? '恭喜！代码修复正确！' : '代码修复结果';
        },
        quizFeedbackDescription() {
            if (this.allCorrect) {
                return '您已经成功找出并修复了所有代码中的问题。这些是在实际应用UMAP时常见的错误，识别并修复它们是有效实现的关键。';
            } else {
                const correctCount = this.fixResults.filter(result => result).length;
                return `您正确修复了${correctCount}个问题（共${this.problems.length}个）。请查看下方的详细解释，了解每个问题的最佳修复方案。`;
            }
        }
    },
    mounted() {
        // 检查该部分是否已完成
        const storedCompleted = localStorage.getItem('umap-completed-sections');
        if (storedCompleted) {
            const completedSections = JSON.parse(storedCompleted);
            this.isCompleted = completedSections.includes(10);
        }

        // 为代码添加样式
        this.highlightCode();
    },
    updated() {
        // 更新时重新应用代码高亮
        this.highlightCode();
    },
    methods: {
        highlightCode() {
            // 简单的代码高亮函数，或者集成现有的代码高亮库
            document.querySelectorAll('pre code').forEach(block => {
                // 简单添加基本样式
                block.style.fontFamily = 'Consolas, Monaco, "Andale Mono", monospace';
                block.style.backgroundColor = '#f5f7fa';
                block.style.padding = '15px';
                block.style.borderRadius = '4px';
                block.style.overflowX = 'auto';
            });
        },

        checkCodeFixes() {
            this.quizCompleted = true;
            this.fixResults = this.problems.map(
                (problem, i) => this.userFixes[i] === problem.answer
            );
            this.allCorrect = this.fixResults.every(result => result);

            if (this.allCorrect || ++this.retries >= 1) {
                this.isCompleted = true;
                this.$emit('complete');
            }
        },

        resetQuiz() {
            this.quizCompleted = false;
            this.userFixes = [];
            this.fixResults = [];
        },

        goToNextSection() {
            this.$emit('complete');
            this.$emit('scrollToSection')
        }
    }
}
</script>

<style scoped>
.code-to-fix pre {
    all: initial;
    /* 重置所有继承样式 */
    display: block;
    white-space: pre;
    /* 必须用pre（不是pre-wrap） */
    font-family: monospace;
    /* 等宽字体 */
    margin: 0;
    padding: 1em;
    overflow: auto;
    background: #f5f5f5;
    border-radius: 4px;
}

.code-to-fix code {
    display: block;
    line-height: 1.5;
    /* 行高 */
    tab-size: 2;
    /* 缩进宽度 */
}

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

.code-example-container {
    padding: 15px 0;
}

.code-example-container h4 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #409EFF;
}

.code-block {
    margin: 15px 0;
    border-radius: 4px;
    overflow: hidden;
}

.code-block pre {
    margin: 0;
    overflow-x: auto;
}

.code-block code {
    font-family: Consolas, Monaco, "Andale Mono", monospace;
    font-size: 0.9rem;
    line-height: 1.5;
}

.optimization-card {
    margin: 20px 0;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.opt-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.opt-header i {
    font-size: 24px;
    color: #409EFF;
    margin-right: 10px;
}

.opt-header h5 {
    margin: 0;
    color: #303133;
}

.performance-comparison {
    margin-top: 30px;
}

.quiz-container {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px dashed #dcdfe6;
}

.code-fix-challenge {
    margin-top: 20px;
    padding: 15px;
    background-color: white;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.code-to-fix {
    margin-bottom: 20px;
}

.problem-list {
    margin-top: 20px;
}

.problem-item {
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f5f7fa;
    border-radius: 4px;
}

.fix-option {
    display: block;
    margin: 10px 0;
}

.submit-btn {
    margin-top: 20px;
}

.response-container {
    margin-top: 20px;
}

.fix-results {
    margin-top: 20px;
    padding: 15px;
    background-color: #f2f6fc;
    border-radius: 4px;
}

.fix-result-item {
    margin-bottom: 15px;
}

.explanation {
    margin-top: 5px;
    margin-left: 20px;
    color: #606266;
    font-size: 0.9rem;
    line-height: 1.5;
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

:deep(code) {
    background-color: #f5f7fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: Consolas, Monaco, "Andale Mono", monospace;
    color: #476582;
}
</style>