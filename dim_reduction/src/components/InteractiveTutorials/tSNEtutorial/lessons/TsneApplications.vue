<template>
    <div class="lesson-container">
        <h2>Lesson 7: t-SNE的实际应用案例</h2>

        <div class="lesson-content">
            <p class="intro">
                在前面的课程中，我们学习了t-SNE的理论基础和参数调整。本节将探讨t-SNE在不同领域的实际应用案例，
                了解如何将t-SNE应用于各种实际问题。
            </p>

            <div class="case-study-section">
                <h3>案例一：图像数据探索与分析</h3>

                <div class="case-study-card">
                    <div class="case-info">
                        <h4>人脸图像聚类与探索</h4>
                        <p>
                            本案例演示如何使用t-SNE对人脸图像数据进行降维和聚类分析，以发现潜在的模式和结构。
                            这种应用在计算机视觉和人脸识别系统中非常有用。
                        </p>

                        <div class="application-info">
                            <div class="info-item">
                                <span class="info-label">数据集:</span>
                                <span>人脸图像数据集 (1000张图像)</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">特征:</span>
                                <span>像素值或深度学习特征</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">应用场景:</span>
                                <span>人脸聚类、异常检测、数据探索</span>
                            </div>
                        </div>
                    </div>

                    <div class="case-visualization">
                        <!-- <img src="@/assets/tsne/face_tsne.png" alt="人脸图像t-SNE可视化"> -->
                        <p class="caption">使用t-SNE对1000张人脸图像的可视化结果，颜色表示不同的表情或年龄组</p>
                    </div>

                    <div class="case-workflow">
                        <h5>工作流程</h5>
                        <div class="workflow-steps">
                            <div class="workflow-step">
                                <div class="step-number">1</div>
                                <div class="step-content">
                                    <h6>预处理</h6>
                                    <p>图像归一化、对齐和裁剪</p>
                                </div>
                            </div>
                            <div class="workflow-step">
                                <div class="step-number">2</div>
                                <div class="step-content">
                                    <h6>特征提取</h6>
                                    <p>使用CNN提取人脸特征向量(2048维)</p>
                                </div>
                            </div>
                            <div class="workflow-step">
                                <div class="step-number">3</div>
                                <div class="step-content">
                                    <h6>降维</h6>
                                    <p>应用t-SNE (perplexity=30)</p>
                                </div>
                            </div>
                            <div class="workflow-step">
                                <div class="step-number">4</div>
                                <div class="step-content">
                                    <h6>分析</h6>
                                    <p>聚类分析和模式识别</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="case-insights">
                        <h5>关键发现</h5>
                        <ul>
                            <li>t-SNE能够有效分离不同表情的人脸图像</li>
                            <li>类似年龄段的人脸在嵌入空间中倾向于聚集</li>
                            <li>通过交互式探索，发现一些难以用标准分类方法捕获的微妙模式</li>
                        </ul>
                    </div>

                    <div class="case-code">
                        <h5>实现代码</h5>
                        <pre><code class="language-python">
  import numpy as np
  from sklearn.manifold import TSNE
  import matplotlib.pyplot as plt
  from tensorflow.keras.applications import VGG16
  from tensorflow.keras.preprocessing import image
  
  # 加载预训练CNN模型
  base_model = VGG16(weights='imagenet', include_top=False, pooling='avg')
  
  # 特征提取函数
  def extract_features(img_path):
      img = image.load_img(img_path, target_size=(224, 224))
      x = image.img_to_array(img)
      x = np.expand_dims(x, axis=0)
      features = base_model.predict(x)
      return features.flatten()
  
  # 1. 提取所有图像特征
  image_paths = [f"faces/{i}.jpg" for i in range(1000)]
  features = np.array([extract_features(img_path) for img_path in image_paths])
  
  # 2. 应用t-SNE降维
  tsne = TSNE(n_components=2, perplexity=30, n_iter=1000, learning_rate=200)
  tsne_results = tsne.fit_transform(features)
  
  # 3. 可视化结果
  plt.figure(figsize=(12, 10))
  scatter = plt.scatter(tsne_results[:, 0], tsne_results[:, 1], 
                       c=labels, cmap='viridis', alpha=0.7)
  plt.colorbar(scatter, label='Expression Category')
  plt.title('t-SNE Visualization of Face Images')
  plt.show()
              </code></pre>
                    </div>
                </div>
            </div>

            <div class="case-study-section">
                <h3>案例二：单细胞RNA测序数据分析</h3>

                <div class="case-study-card">
                    <div class="case-info">
                        <h4>单细胞基因表达聚类</h4>
                        <p>
                            t-SNE在生物信息学领域的一个重要应用是单细胞RNA测序(scRNA-seq)数据的可视化和分析。
                            在这个案例中，我们展示如何使用t-SNE来识别不同的细胞类型和状态。
                        </p>

                        <div class="application-info">
                            <div class="info-item">
                                <span class="info-label">数据集:</span>
                                <span>5,000个细胞的基因表达矩阵</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">特征:</span>
                                <span>20,000个基因的表达水平</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">应用场景:</span>
                                <span>细胞类型鉴定、发育轨迹分析</span>
                            </div>
                        </div>
                    </div>

                    <div class="case-visualization">
                        <!-- <img src="@/assets/tsne/scRNA_tsne.png" alt="单细胞RNA-seq t-SNE可视化"> -->
                        <p class="caption">t-SNE展示的不同细胞类型，每种颜色代表一个已知或预测的细胞类型</p>
                    </div>

                    <div class="case-workflow">
                        <h5>工作流程</h5>
                        <div class="workflow-steps">
                            <div class="workflow-step">
                                <div class="step-number">1</div>
                                <div class="step-content">
                                    <h6>数据预处理</h6>
                                    <p>归一化、批次效应校正、高变异基因选择</p>
                                </div>
                            </div>
                            <div class="workflow-step">
                                <div class="step-number">2</div>
                                <div class="step-content">
                                    <h6>降维</h6>
                                    <p>PCA初步降维后应用t-SNE</p>
                                </div>
                            </div>
                            <div class="workflow-step">
                                <div class="step-number">3</div>
                                <div class="step-content">
                                    <h6>聚类</h6>
                                    <p>对t-SNE结果进行聚类分析</p>
                                </div>
                            </div>
                            <div class="workflow-step">
                                <div class="step-number">4</div>
                                <div class="step-content">
                                    <h6>细胞类型注释</h6>
                                    <p>基于标记基因表达识别细胞类型</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="case-insights">
                        <h5>关键发现</h5>
                        <ul>
                            <li>成功识别出12种不同的细胞类型，包括罕见细胞群体</li>
                            <li>发现了一些处于转换状态的细胞，表明细胞分化过程</li>
                            <li>t-SNE相比UMAP在保留局部结构方面表现更优，但UMAP更好地展示全局关系</li>
                        </ul>
                    </div>

                    <div class="case-code">
                        <h5>实现代码</h5>
                        <pre><code class="language-python">
  import scanpy as sc
  import numpy as np
  import matplotlib.pyplot as plt
  
  # 加载单细胞RNA-seq数据
  adata = sc.read_h5ad('scRNA_dataset.h5ad')
  
  # 数据预处理
  sc.pp.normalize_per_cell(adata)
  sc.pp.log1p(adata)
  sc.pp.highly_variable_genes(adata, n_top_genes=2000)
  adata = adata[:, adata.var.highly_variable]
  
  # PCA初步降维
  sc.pp.pca(adata, n_comps=50)
  
  # 应用t-SNE
  sc.tl.tsne(adata, perplexity=30, n_pcs=50)
  
  # 聚类分析
  sc.tl.leiden(adata, resolution=0.8)
  
  # 可视化结果
  sc.pl.tsne(adata, color=['leiden', 'CD4', 'CD8A', 'FOXP3'], 
            title=['Cell Clusters', 'CD4+ T cells', 'CD8+ T cells', 'Regulatory T cells'])
  
  # 细胞类型注释
  marker_genes = {
      'T-cells': ['CD3E', 'CD3D'],
      'B-cells': ['CD79A', 'CD79B'],
      'NK cells': ['NCAM1', 'NKG7'],
      'Monocytes': ['CD14', 'LYZ']
  }
  
  for cell_type, markers in marker_genes.items():
      sc.pl.tsne(adata, color=markers, title=f"{cell_type} markers")
              </code></pre>
                    </div>

                    <div class="interactive-demo">
                        <h5>交互式探索</h5>
                        <p>通过以下交互式示例，探索不同参数对单细胞RNA-seq聚类的影响：</p>

                        <div class="demo-controls">
                            <div class="control-group">
                                <label for="param-perplexity">Perplexity:</label>
                                <input type="range" id="param-perplexity" v-model.number="scrnaPerplexity" min="5"
                                    max="100" @change="updateScrnaDemo">
                                <span>{{ scrnaPerplexity }}</span>
                            </div>
                            <div class="control-group">
                                <label for="param-method">方法:</label>
                                <select id="param-method" v-model="scrnaMethod" @change="updateScrnaDemo">
                                    <option value="tsne">t-SNE</option>
                                    <option value="umap">UMAP</option>
                                    <option value="pca">PCA</option>
                                </select>
                            </div>
                            <div class="control-group">
                                <label for="param-genes">基因数量:</label>
                                <select id="param-genes" v-model="scrnaGenes" @change="updateScrnaDemo">
                                    <option value="500">Top 500</option>
                                    <option value="1000">Top 1,000</option>
                                    <option value="2000">Top 2,000</option>
                                </select>
                            </div>
                        </div>

                        <div class="demo-visualization">
                            <img :src="scrnaVisualizationImage" alt="scRNA-seq visualization">
                        </div>
                    </div>
                </div>
            </div>

            <div class="case-study-section">
                <h3>案例三：文本数据可视化与主题发现</h3>

                <div class="case-study-card">
                    <div class="case-info">
                        <h4>文档嵌入与主题聚类</h4>
                        <p>
                            本案例展示如何使用t-SNE对文本数据进行可视化，帮助发现语料库中的主题和模式。
                            通过降维和聚类，可以直观地理解大量文本数据的内在结构。
                        </p>

                        <div class="application-info">
                            <div class="info-item">
                                <span class="info-label">数据集:</span>
                                <span>新闻文章集合 (5,000篇)</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">特征:</span>
                                <span>TF-IDF或Word2Vec嵌入</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">应用场景:</span>
                                <span>主题发现、文档分类、内容推荐</span>
                            </div>
                        </div>
                    </div>

                    <div class="case-visualization">
                        <!-- <img src="@/assets/tsne/text_tsne.png" alt="文本数据t-SNE可视化"> -->
                        <p class="caption">新闻文章的t-SNE可视化，不同颜色表示不同的主题类别</p>
                    </div>

                    <div class="text-visualization-interactive">
                        <div class="visualization-container">
                            <div ref="textTsneChart" class="text-tsne-chart"></div>
                            <div class="hover-info" v-if="hoveredDocument">
                                <h6>{{ hoveredDocument.title }}</h6>
                                <p>{{ hoveredDocument.excerpt }}</p>
                                <p><strong>主题:</strong> {{ hoveredDocument.category }}</p>
                            </div>
                        </div>
                        <div class="controls">
                            <div class="control-group">
                                <label>嵌入方法:</label>
                                <div class="radio-group">
                                    <label><input type="radio" v-model="textEmbeddingMethod" value="tfidf"
                                            @change="updateTextDemo">TF-IDF</label>
                                    <label><input type="radio" v-model="textEmbeddingMethod" value="word2vec"
                                            @change="updateTextDemo">Word2Vec</label>
                                    <label><input type="radio" v-model="textEmbeddingMethod" value="bert"
                                            @change="updateTextDemo">BERT</label>
                                </div>
                            </div>
                            <div class="control-group">
                                <label>显示标签:</label>
                                <div class="checkbox-group">
                                    <label><input type="checkbox" v-model="showDocumentLabels"
                                            @change="updateTextDemo">文档标题</label>
                                    <label><input type="checkbox" v-model="showCategoryColors"
                                            @change="updateTextDemo">主题颜色</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="case-code">
                        <h5>实现代码</h5>
                        <pre><code class="language-python">
  import numpy as np
  import pandas as pd
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.manifold import TSNE
  import matplotlib.pyplot as plt
  import seaborn as sns
  import nltk
  from nltk.corpus import stopwords
  
  # 加载数据
  news_df = pd.read_csv('news_articles.csv')
  texts = news_df['content'].tolist()
  categories = news_df['category'].tolist()
  
  # 文本预处理
  nltk.download('stopwords')
  stop_words = set(stopwords.words('english'))
  
  def preprocess(text):
      tokens = [word.lower() for word in nltk.word_tokenize(text) 
                if word.isalpha() and word.lower() not in stop_words]
      return ' '.join(tokens)
  
  processed_texts = [preprocess(text) for text in texts]
  
  # TF-IDF特征提取
  vectorizer = TfidfVectorizer(max_features=5000)
  tfidf_matrix = vectorizer.fit_transform(processed_texts)
  
  # 应用t-SNE
  tsne = TSNE(n_components=2, perplexity=40, n_iter=1000, random_state=42)
  tsne_results = tsne.fit_transform(tfidf_matrix)
  
  # 可视化结果
  plt.figure(figsize=(14, 10))
  categories_unique = list(set(categories))
  color_map = dict(zip(categories_unique, sns.color_palette("hls", len(categories_unique))))
  colors = [color_map[cat] for cat in categories]
  
  scatter = plt.scatter(tsne_results[:, 0], tsne_results[:, 1], 
                       c=colors, alpha=0.7, s=40)
  
  # 添加标题和图例
  plt.title('t-SNE visualization of news articles')
  legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                               markerfacecolor=color_map[cat], label=cat, markersize=10) 
                    for cat in categories_unique]
  plt.legend(handles=legend_elements, title='News Categories')
  
  # 添加交互性 - 在Jupyter Notebook中使用mpld3
  import mpld3
  mpld3.enable_notebook()
  tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=news_df['title'].tolist())
  mpld3.plugins.connect(plt.gcf(), tooltip)
  
  plt.show()
              </code></pre>
                    </div>

                    <div class="case-insights">
                        <h5>关键发现</h5>
                        <ul>
                            <li>t-SNE能够有效地分离不同主题的新闻文章</li>
                            <li>使用BERT嵌入比传统TF-IDF和Word2Vec提供更清晰的主题分离</li>
                            <li>发现了一些跨主题的文章，这些文章往往位于簇的边界</li>
                            <li>某些相关主题(如科技和商业)在可视化中展现出邻近性</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="your-turn-section">
                <h3>轮到你了：实践项目</h3>
                <p>
                    现在您已经了解了t-SNE在多个领域的实际应用，是时候尝试将其应用到您自己的项目中了。
                    下面是一个实践项目，您可以按照指导步骤完成它。
                </p>

                <div class="project-card">
                    <h4>商品推荐系统中的用户行为聚类</h4>
                    <p>
                        在这个项目中，您将使用t-SNE对电子商务网站的用户行为数据进行聚类分析，
                        以发现不同的用户群体和行为模式，从而改进推荐系统。
                    </p>

                    <div class="project-steps">
                        <h5>项目步骤</h5>
                        <ol>
                            <li>
                                <strong>数据准备</strong>
                                <p>
                                    您将使用提供的用户-商品交互数据集，包含用户ID、商品ID、交互类型(点击、收藏、购买)和时间戳。
                                    <a href="#" @click.prevent="downloadDataset">下载数据集</a>
                                </p>
                            </li>
                            <li>
                                <strong>特征工程</strong>
                                <p>
                                    为每个用户构建特征向量，可以考虑以下特征：
                                <ul>
                                    <li>商品类别偏好(各类别的交互次数)</li>
                                    <li>交互行为分布(点击、收藏、购买的比例)</li>
                                    <li>时间模式(工作日vs周末、一天中的时间分布)</li>
                                    <li>价格敏感度(交互商品的价格分布)</li>
                                </ul>
                                </p>
                            </li>
                            <li>
                                <strong>应用t-SNE</strong>
                                <p>
                                    对用户特征向量应用t-SNE降维，尝试不同的参数设置。
                                </p>
                            </li>
                            <li>
                                <strong>聚类分析</strong>
                                <p>
                                    对t-SNE结果进行聚类(如K-means或DBSCAN)，确定最佳的聚类数量和每个聚类的特征。
                                </p>
                            </li>
                            <li>
                                <strong>用户群体画像</strong>
                                <p>
                                    分析每个聚类的用户行为特征，创建用户群体画像。
                                </p>
                            </li>
                            <li>
                                <strong>推荐策略优化</strong>
                                <p>
                                    基于不同用户群体的特征，提出针对性的推荐策略优化建议。
                                </p>
                            </li>
                        </ol>
                    </div>

                    <div class="project-resources">
                        <h5>参考代码框架</h5>
                        <pre><code class="language-python"></code></pre>
                    </div>

                    <div class="submission-instructions">
                        <h5>提交方式</h5>
                        <p>
                            完成项目后，请提交以下内容：
                        </p>
                        <ol>
                            <li>完整的代码和分析报告</li>
                            <li>t-SNE可视化结果和聚类分析图</li>
                            <li>用户群体画像和推荐策略建议</li>
                            <li>项目过程中遇到的挑战和解决方案</li>
                        </ol>
                        <button @click="submitProject" class="submit-button">提交项目</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="navigation-buttons">
            <button @click="previousLesson">上一课</button>
            <button @click="nextLesson">下一课</button>
        </div>
    </div>
</template>

<script>
// import * as d3 from 'd3';
import * as echarts from 'echarts';

export default {
    name: 'Lesson7TsneApplications',
    data() {
        return {
            // 单细胞RNA-seq演示相关
            scrnaPerplexity: 30,
            scrnaMethod: 'tsne',
            scrnaGenes: '2000',

            // 文本可视化相关
            textEmbeddingMethod: 'tfidf',
            showDocumentLabels: false,
            showCategoryColors: true,
            hoveredDocument: null,
            textChart: null,

            // 项目相关
            projectSubmitted: false
        };
    },
    computed: {
        scrnaVisualizationImage() {
            // 根据当前参数返回对应的图像URL
            return `/assets/tsne/scRNA_${this.scrnaMethod}_p${this.scrnaPerplexity}_g${this.scrnaGenes}.png`;
        }
    },
    mounted() {
        this.initializeTextVisualization();
    },
    beforeUnmount() {
        if (this.textChart) {
            this.textChart.dispose();
        }
    },
    methods: {
        updateScrnaDemo() {
            // 在实际应用中，这里可能会发送请求获取新的可视化
            console.log(`更新scRNA演示，参数: method=${this.scrnaMethod}, perplexity=${this.scrnaPerplexity}, genes=${this.scrnaGenes}`);
        },

        initializeTextVisualization() {
            // 初始化文本可视化图表
            this.textChart = echarts.init(this.$refs.textTsneChart);
            this.updateTextDemo();
        },

        async updateTextDemo() {
            // 模拟从服务器获取数据
            // 在实际应用中，这会从API获取不同嵌入方法的t-SNE结果
            try {
                // 显示加载中状态
                this.textChart.showLoading();

                // 模拟异步请求
                const data = await this.fetchTextTsneData();

                // 配置ECharts选项
                const option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: (params) => {
                            const doc = data.documents[params.dataIndex];
                            return `<strong>${doc.title}</strong><br/>
                      类别: ${doc.category}<br/>
                      ${doc.excerpt.substring(0, 100)}...`;
                        }
                    },
                    xAxis: {
                        type: 'value',
                        show: false
                    },
                    yAxis: {
                        type: 'value',
                        show: false
                    },
                    series: [{
                        type: 'scatter',
                        data: data.points,
                        symbolSize: 10,
                        itemStyle: {
                            color: (params) => {
                                if (this.showCategoryColors) {
                                    // 根据类别着色
                                    const colorMap = {
                                        'politics': '#e41a1c',
                                        'business': '#377eb8',
                                        'technology': '#4daf4a',
                                        'entertainment': '#984ea3',
                                        'sports': '#ff7f00',
                                        'health': '#a65628',
                                        'science': '#f781bf'
                                    };
                                    return colorMap[data.documents[params.dataIndex].category] || '#999';
                                }
                                return '#3498db';
                            },
                            opacity: 0.7
                        },
                        label: {
                            show: this.showDocumentLabels,
                            formatter: (params) => {
                                return data.documents[params.dataIndex].title.substring(0, 15) + '...';
                            },
                            position: 'right',
                            fontSize: 10,
                            color: '#555'
                        }
                    }]
                };

                // 设置图表选项
                this.textChart.setOption(option);

                // 事件监听
                this.textChart.on('mouseover', (params) => {
                    this.hoveredDocument = data.documents[params.dataIndex];
                });

                this.textChart.on('mouseout', () => {
                    this.hoveredDocument = null;
                });
            } catch (error) {
                console.error('更新文本可视化错误:', error);
            } finally {
                this.textChart.hideLoading();
            }
        },

        async fetchTextTsneData() {
            // 模拟异步数据获取
            return new Promise((resolve) => {
                setTimeout(() => {
                    // 生成模拟数据
                    const categories = ['politics', 'business', 'technology', 'entertainment', 'sports', 'health', 'science'];
                    const documents = [];
                    const points = [];

                    // 为每个类别生成聚类点
                    categories.forEach((category, categoryIndex) => {
                        const centerX = (categoryIndex % 3) * 10 - 10;
                        const centerY = Math.floor(categoryIndex / 3) * 10 - 10;

                        // 每个类别生成30-50个点
                        const numPoints = 30 + Math.floor(Math.random() * 20);

                        for (let i = 0; i < numPoints; i++) {
                            // 围绕中心点添加随机偏移
                            const x = centerX + (Math.random() - 0.5) * 5;
                            const y = centerY + (Math.random() - 0.5) * 5;

                            points.push([x, y]);

                            // 生成模拟文档数据
                            documents.push({
                                id: documents.length,
                                title: `${category.charAt(0).toUpperCase() + category.slice(1)} Article ${i + 1}`,
                                category: category,
                                excerpt: `This is a sample ${category} article. It contains content related to ${category} topics.`
                            });
                        }
                    });

                    // 模拟不同嵌入方法的效果
                    if (this.textEmbeddingMethod === 'bert') {
                        // BERT嵌入通常会产生更清晰的聚类
                        points.forEach((point, index) => {
                            // 向聚类中心收缩20%
                            const category = documents[index].category;
                            const categoryIndex = categories.indexOf(category);
                            const centerX = (categoryIndex % 3) * 10 - 10;
                            const centerY = Math.floor(categoryIndex / 3) * 10 - 10;

                            point[0] = point[0] * 0.8 + centerX * 0.2;
                            point[1] = point[1] * 0.8 + centerY * 0.2;
                        });
                    } else if (this.textEmbeddingMethod === 'tfidf') {
                        // TF-IDF通常聚类不如词嵌入方法清晰
                        points.forEach(point => {
                            // 添加更多随机性
                            point[0] += (Math.random() - 0.5) * 3;
                            point[1] += (Math.random() - 0.5) * 3;
                        });
                    }

                    resolve({ points, documents });
                }, 500);
            });
        },

        downloadDataset() {
            alert('在实际应用中，这里会下载项目所需的数据集。');
        },

        submitProject() {
            // 模拟项目提交
            this.projectSubmitted = true;
            alert('感谢您提交项目！在实际课程中，教师会对您的提交进行评估和反馈。');
        },

        previousLesson() {
            this.$router.push('/lesson6');
        },

        nextLesson() {
            this.$router.push('/lesson8');
        }
    }
};
</script>

<style scoped>
.lesson-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h2 {
    color: #2c3e50;
    margin-bottom: 25px;
    text-align: center;
}

.lesson-content {
    display: flex;
    flex-direction: column;
    gap: 40px;
}

.intro {
    font-size: 1.1em;
    line-height: 1.6;
    margin-bottom: 30px;
}

.case-study-section {
    margin-bottom: 50px;
}

.case-study-section h3 {
    color: #2c3e50;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e0e0e0;
}

.case-study-card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}

.case-info {
    margin-bottom: 20px;
}

.case-info h4 {
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 15px;
}

.application-info {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 15px;
    background-color: #f0f8ff;
    padding: 15px;
    border-radius: 4px;
}

.info-item {
    flex: 1;
    min-width: 200px;
}

.info-label {
    font-weight: bold;
    margin-right: 5px;
}

.case-visualization {
    margin: 25px 0;
    text-align: center;
}

.case-visualization img {
    max-width: 100%;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.caption {
    font-size: 0.9em;
    color: #666;
    margin-top: 8px;
}

.case-workflow {
    margin: 25px 0;
}

.workflow-steps {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 15px;
}

.workflow-step {
    flex: 1;
    min-width: 150px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}

.step-number {
    background-color: #3498db;
    color: white;
    width: 25px;
    height: 25px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    flex-shrink: 0;
}

.step-content h6 {
    margin: 0 0 5px 0;
    color: #2c3e50;
}

.step-content p {
    margin: 0;
    font-size: 0.9em;
}

.case-insights {
    margin: 25px 0;
    background-color: #f0f8ff;
    padding: 20px;
    border-radius: 4px;
    border-left: 4px solid #3498db;
}

.case-insights ul {
    margin: 10px 0;
    padding-left: 20px;
}

.case-insights li {
    margin-bottom: 8px;
}

.case-code {
    margin: 25px 0;
}

pre {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.9em;
    line-height: 1.4;
}

code {
    font-family: 'Courier New', Courier, monospace;
}

.interactive-demo {
    margin: 25px 0;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.demo-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 20px;
}

.control-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.control-group label {
    font-weight: bold;
}

.text-visualization-interactive {
    margin: 25px 0;
}

.visualization-container {
    position: relative;
    margin-bottom: 20px;
}

.text-tsne-chart {
    width: 100%;
    height: 400px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #eee;
}

.hover-info {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: rgba(255, 255, 255, 0.95);
    padding: 15px;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    max-width: 300px;
}

.hover-info h6 {
    margin-top: 0;
    margin-bottom: 8px;
    color: #2c3e50;
}

.hover-info p {
    margin: 5px 0;
    font-size: 0.9em;
}

.controls {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 20px;
}

.radio-group,
.checkbox-group {
    display: flex;
    gap: 15px;
}

.your-turn-section {
    margin-top: 40px;
}

.your-turn-section h3 {
    color: #2c3e50;
    margin-bottom: 20px;
}

.project-card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}

.project-card h4 {
    color: #2c3e50;
    margin-top: 0;
    margin-bottom: 15px;
}

.project-steps {
    margin: 25px 0;
}

.project-steps ol {
    padding-left: 20px;
}

.project-steps li {
    margin-bottom: 20px;
}

.project-steps li strong {
    color: #2c3e50;
}

.project-resources {
    margin: 30px 0;
}

.submission-instructions {
    margin-top: 30px;
    padding: 20px;
    background-color: #f0f8ff;
    border-radius: 4px;
}

.submit-button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 15px;
    transition: background-color 0.3s;
}

.submit-button:hover {
    background-color: #2980b9;
}

.navigation-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 40px;
}

.navigation-buttons button {
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.navigation-buttons button:hover {
    background-color: #2980b9;
}

@media (max-width: 768px) {
    .workflow-steps {
        flex-direction: column;
    }

    .application-info {
        flex-direction: column;
    }

    .demo-controls {
        flex-direction: column;
    }

    .radio-group,
    .checkbox-group {
        flex-direction: column;
    }
}
</style>
