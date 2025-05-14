<!-- D3DatasetDisplay.vue -->
<template>
    <div class="dataset-container">
        <div v-if="!nodeData" class="no-data-tip">
            <el-empty description="暂无数据"></el-empty>
        </div>
        <div v-else>
            <div class="header-container">
                <h3>数据集展示 - {{ nodeData.operation }}</h3>
                <div class="display-controls">
                    <el-radio-group v-model="displayMode" size="small">
                        <el-radio-button label="standard">标准比例展示</el-radio-button>
                        <el-radio-button label="square">相对比例展示</el-radio-button>
                    </el-radio-group>


                </div>
            </div>

            <div v-if="hasData" class="data-info">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-card shadow="hover" class="info-card">
                            <div slot="header">
                                <span>数据集大小</span>
                            </div>
                            <div class="info-content">
                                <i class="el-icon-s-data"></i>
                                <span>{{ datasetSize }} 条记录</span>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" class="info-card">
                            <div slot="header">
                                <span>特征数量</span>
                            </div>
                            <div class="info-content">
                                <i class="el-icon-s-grid"></i>
                                <span>{{ featureCount }} 个特征</span>
                            </div>
                        </el-card>
                    </el-col>
                    <el-col :span="8">
                        <el-card shadow="hover" class="info-card">
                            <div slot="header">
                                <span>标签类别</span>
                            </div>
                            <div class="info-content">
                                <i class="el-icon-collection-tag"></i>
                                <span>{{ labelCount }} 个类别</span>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </div>

            <!-- 特征选择部分 -->
            <div v-if="hasData && featureCount > 0" class="dimension-selector">
                <el-card shadow="hover">
                    <div slot="header">
                        <span>特征维度选择</span>
                        <el-tag type="info" size="small" style="margin-left: 10px;">
                            {{ dimensionText }}
                        </el-tag>
                    </div>

                    <div v-if="featureCount > 1" class="dimension-options">
                        <div class="dimension-item">
                            <span class="dimension-label">X轴:</span>
                            <el-select v-model="selectedDimensions.x" placeholder="选择X轴特征" style="width: 160px;">
                                <el-option v-for="(name, index) in featureNames" :key="'x-' + index" :label="name"
                                    :value="index">
                                </el-option>
                            </el-select>
                        </div>

                        <div v-if="featureCount > 1" class="dimension-item">
                            <span class="dimension-label">Y轴:</span>
                            <el-select v-model="selectedDimensions.y" placeholder="选择Y轴特征" style="width: 160px;"
                                :disabled="featureCount < 2">
                                <el-option v-for="(name, index) in featureNames" :key="'y-' + index" :label="name"
                                    :value="index">
                                </el-option>
                            </el-select>
                        </div>

                        <div v-if="featureCount > 2" class="dimension-item">
                            <span class="dimension-label">Z轴:</span>
                            <el-select v-model="selectedDimensions.z" placeholder="选择Z轴特征" style="width: 160px;"
                                :disabled="featureCount < 3">
                                <el-option v-for="(name, index) in featureNames" :key="'z-' + index" :label="name"
                                    :value="index">
                                </el-option>
                            </el-select>
                        </div>
                    </div>
                    <div v-else class="dimension-notice">
                        数据只有一个维度，将自动使用该维度展示。
                    </div>
                </el-card>
            </div>

            <!-- 可视化区域 -->
            <div v-if="hasData" class="visualization-container">


                <el-card shadow="hover">

                    <div class="vis-header" slot="header">
                        <span>数据可视化</span>
                        <el-tooltip v-if="displayMode === 'standard'" content="标准模式：保持数据真实比例，X和Y轴使用相同的单位长度"
                            placement="top">
                            <i class="el-icon-info" style="margin-left: 8px; color: #909399; cursor: help;"></i>
                        </el-tooltip>
                        <el-tooltip v-else content="相对比例模式：调整坐标轴使数据分布类似于正方形" placement="top">
                            <i class="el-icon-info" style="margin-left: 8px; color: #909399; cursor: help;"></i>
                        </el-tooltip>
                        <el-tooltip content="刷新数据" placement="top">
                            <el-button type="primary" icon="el-icon-refresh" circle size="small" @click="refreshData"
                                :disabled="!hasData">
                            </el-button>
                        </el-tooltip>
                    </div>

                    <div class="chart-container" :class="displayMode">
                        <div ref="chartRef" class="d3-chart"></div>
                    </div>

                    <div class="legend-container">
                        <div class="legend-title">标签图例:</div>
                        <div class="legend-items">
                            <div v-for="(color, label) in colorMap" :key="label" class="legend-item">
                                <span class="legend-color" :style="{ backgroundColor: color }"></span>
                                <span class="legend-label">{{ label }}</span>
                            </div>
                        </div>
                    </div>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'D3DatasetDisplay',
    props: {
        nodeData: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            displayMode: 'standard', // 'standard' or 'square'
            selectedDimensions: {
                x: '0',  // 默认选择第一个特征作为X轴
                y: '1',  // 默认选择第二个特征作为Y轴
                z: '2'   // 默认选择第三个特征作为Z轴
            },
            // 标签颜色映射
            colorMap: {},
            uniqueColors: [
                '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
                '#9B59B6', '#3498DB', '#1ABC9C', '#F39C12', '#E74C3C',
                '#16A085', '#2980B9', '#8E44AD', '#F1C40F', '#D35400'
            ],
            svgContainer: null,
            tooltip: null,
            resizeTimer: null
        };
    },
    computed: {
        hasData() {
            return this.nodeData &&
                this.nodeData.dataset &&
                this.nodeData.dataset.length > 0;
        },
        datasetSize() {
            return this.hasData ? this.nodeData.dataset.length : 0;
        },
        featureCount() {
            if (!this.hasData || this.nodeData.dataset.length === 0) return 0;

            // 计算数据集中每条记录的特征数量（即数组长度）
            // 假设所有记录的特征数量相同，取第一条记录的特征数量
            return this.nodeData.dataset[0].length;
        },
        labelCount() {
            if (!this.hasData || !this.nodeData.target) return 0;

            // 获取唯一的标签值
            const uniqueLabels = [...new Set(this.nodeData.target)];
            return uniqueLabels.length;
        },
        featureNames() {
            return this.hasData && this.nodeData.feature_names
                ? this.nodeData.feature_names
                : {};
        },
        dimensionText() {
            if (this.featureCount <= 0) return '无维度';
            if (this.featureCount === 1) return '一维数据';
            if (this.featureCount === 2) return '二维数据';
            if (this.featureCount === 3) return '三维数据';
            return `${this.featureCount}维数据 (选择3个维度展示)`;
        },
        processedData() {
            if (!this.hasData) return [];

            return this.nodeData.dataset.map((dataPoint, index) => {
                const x = dataPoint[this.selectedDimensions.x] || 0;
                const y = this.featureCount > 1 ? (dataPoint[this.selectedDimensions.y] || 0) : 0;
                const z = this.featureCount > 2 ? (dataPoint[this.selectedDimensions.z] || 0) : 0;

                return {
                    x,
                    y,
                    z,
                    target: this.nodeData.target[index],
                    originalData: dataPoint
                };
            });
        }
    },
    watch: {
        nodeData: {
            handler() {
                this.initColorMap();
                this.$nextTick(() => {
                    this.renderChart();
                });
            },
            deep: true
        },
        displayMode() {
            this.$nextTick(() => {
                this.renderChart();
            });
        },
        selectedDimensions: {
            handler() {
                this.$nextTick(() => {
                    this.renderChart();
                });
            },
            deep: true
        }
    },
    mounted() {
        this.initColorMap();
        this.$nextTick(() => {
            this.renderChart();
        });

        // 创建tooltip元素
        this.tooltip = d3.select('body').append('div')
            .attr('class', 'd3-tooltip')
            .style('opacity', 0)
            .style('position', 'absolute')
            .style('background-color', 'rgba(0, 0, 0, 0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('pointer-events', 'none')
            .style('font-size', '12px')
            .style('z-index', 1000)
            .style('max-width', '250px')
            .style('overflow', 'auto')
            .style('max-height', '200px')
            .style('word-wrap', 'break-word');

        // 监听窗口大小变化，自动调整图表
        window.addEventListener('resize', this.handleResize);
    },
    beforeDestroy() {
        // 清除tooltip
        if (this.tooltip) {
            this.tooltip.remove();
        }

        // 移除窗口大小变化监听
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        refreshData() {
            // 刷新图表
            this.renderChart();
            this.$message({
                message: '数据已刷新',
                type: 'success'
            });
        },
        initColorMap() {
            if (!this.hasData) return;

            const uniqueLabels = [...new Set(this.nodeData.target)];
            const colorMap = {};

            uniqueLabels.forEach((label, index) => {
                colorMap[label] = this.uniqueColors[index % this.uniqueColors.length];
            });

            this.colorMap = colorMap;
        },
        renderChart() {
            if (!this.hasData || !this.$refs.chartRef) return;

            // 清除旧图表
            d3.select(this.$refs.chartRef).selectAll('*').remove();

            const container = this.$refs.chartRef;
            const width = container.clientWidth;
            const height = container.clientHeight || 500;
            const margin = { top: 20, right: 20, bottom: 40, left: 50 };
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            // 创建SVG容器
            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height);

            // 创建内部绘图区域
            const g = svg.append('g')
                .attr('transform', `translate(${margin.left}, ${margin.top})`);

            // 根据维度数量选择不同的绘制方法
            if (this.featureCount === 1) {
                this.render1DChart(g, innerWidth, innerHeight);
            } else if (this.featureCount >= 2) {
                this.render2DChart(g, innerWidth, innerHeight);
            }
        },
        render1DChart(g, width, height) {
            const data = this.processedData;

            // 获取数据范围
            const xMin = d3.min(data, d => d.x);
            const xMax = d3.max(data, d => d.x);

            let xScale;

            if (this.displayMode === 'standard') {
                // 标准模式：为X轴使用实际数据范围
                xScale = d3.scaleLinear()
                    .domain([xMin, xMax])
                    .range([0, width])
                    .nice();
            } else {
                // 正方形模式：调整X轴使数据在视图范围内均匀分布
                // 添加一些边距防止数据点触及边缘
                const padding = (xMax - xMin) * 0.1;
                xScale = d3.scaleLinear()
                    .domain([xMin - padding, xMax + padding])
                    .range([0, width])
                    .nice();
            }

            // Y轴比例尺（一维数据使用随机分布或固定位置）
            d3.scaleLinear()
                .domain([0, 1])
                .range([height, 0]);

            // 绘制X轴
            g.append('g')
                .attr('class', 'x-axis')
                .attr('transform', `translate(0, ${height})`)
                .call(d3.axisBottom(xScale));

            // 如果是标准模式，添加网格线
            if (this.displayMode === 'standard') {
                // 添加X轴网格线
                g.append('g')
                    .attr('class', 'grid')
                    .attr('transform', `translate(0, ${height})`)
                    .call(d3.axisBottom(xScale)
                        .tickSize(-height)
                        .tickFormat(''))
                    .call(g => g.select('.domain').remove())
                    .call(g => g.selectAll('.tick line')
                        .attr('stroke', '#e0e0e0')
                        .attr('stroke-dasharray', '3,3'));
            }

            // 添加X轴标签
            g.append('text')
                .attr('class', 'x-label')
                .attr('text-anchor', 'middle')
                .attr('x', width / 2)
                .attr('y', height + 35)
                .text(this.featureNames[this.selectedDimensions.x]);

            // 绘制数据点
            g.selectAll('.data-point')
                .data(data)
                .enter()
                .append('circle')
                .attr('class', 'data-point')
                .attr('cx', d => xScale(d.x))
                .attr('cy', (d) => {
                    // 一维数据，Y值使用不同策略
                    if (this.displayMode === 'standard') {
                        return height / 2; // 标准模式下固定在中间
                    } else {
                        // 正方形模式下，使用伪随机（但确定性）的Y值分布，根据X值生成
                        // 这样相同X值的点会有不同的Y值，但每次渲染都是一致的
                        const seed = (d.x + '').split('').reduce((a, b) => {
                            return (a * 31 + b.charCodeAt(0)) % 997;
                        }, 7);
                        return height * 0.1 + (seed % 80) / 100 * height;
                    }
                })
                .attr('r', 5)
                .attr('fill', d => this.colorMap[d.target] || '#409EFF')
                .attr('stroke', '#fff')
                .attr('stroke-width', 1)
                .attr('opacity', 0.7)
                .on('mouseover', (event, d) => {
                    this.showTooltip(event, d);
                })
                .on('mouseout', () => {
                    this.hideTooltip();
                });
        },
        render2DChart(g, width, height) {
            const data = this.processedData;

            // 找出X和Y的数据范围
            const xValues = data.map(d => d.x);
            const yValues = data.map(d => d.y);

            const xMin = d3.min(xValues);
            const xMax = d3.max(xValues);
            const yMin = d3.min(yValues);
            const yMax = d3.max(yValues);

            let xScale, yScale;

            if (this.displayMode === 'standard') {
                // 标准模式：使用相同的比例尺单位（保持真实数据比例）
                // 计算数据范围
                const xRange = xMax - xMin;
                const yRange = yMax - yMin;

                // 找出更大的范围，并使用它来确定两个轴的比例尺
                const maxRange = Math.max(xRange, yRange);

                // 计算中心点
                const xCenter = (xMin + xMax) / 2;
                const yCenter = (yMin + yMax) / 2;

                // 设置相同比例尺的domain，确保xy轴的单位长度一致
                xScale = d3.scaleLinear()
                    .domain([xCenter - maxRange / 2, xCenter + maxRange / 2])
                    .range([0, width])
                    .nice();

                yScale = d3.scaleLinear()
                    .domain([yCenter - maxRange / 2, yCenter + maxRange / 2])
                    .range([height, 0]) // 反转Y轴，使原点在左下角
                    .nice();
            } else {
                // 正方形模式：独立缩放X和Y轴使散点图呈现为正方形
                xScale = d3.scaleLinear()
                    .domain([xMin, xMax])
                    .range([0, width])
                    .nice();

                yScale = d3.scaleLinear()
                    .domain([yMin, yMax])
                    .range([height, 0]) // 反转Y轴，使原点在左下角
                    .nice();
            }

            // 绘制X轴
            g.append('g')
                .attr('class', 'x-axis')
                .attr('transform', `translate(0, ${height})`)
                .call(d3.axisBottom(xScale));

            // 绘制Y轴
            g.append('g')
                .attr('class', 'y-axis')
                .call(d3.axisLeft(yScale));

            // 如果是标准模式，添加网格线以帮助观察等比例
            if (this.displayMode === 'standard') {
                // 添加X轴网格线
                g.append('g')
                    .attr('class', 'grid')
                    .attr('transform', `translate(0, ${height})`)
                    .call(d3.axisBottom(xScale)
                        .tickSize(-height)
                        .tickFormat(''))
                    .call(g => g.select('.domain').remove())
                    .call(g => g.selectAll('.tick line')
                        .attr('stroke', '#e0e0e0')
                        .attr('stroke-dasharray', '3,3'));

                // 添加Y轴网格线
                g.append('g')
                    .attr('class', 'grid')
                    .call(d3.axisLeft(yScale)
                        .tickSize(-width)
                        .tickFormat(''))
                    .call(g => g.select('.domain').remove())
                    .call(g => g.selectAll('.tick line')
                        .attr('stroke', '#e0e0e0')
                        .attr('stroke-dasharray', '3,3'));
            }

            // 添加X轴标签
            g.append('text')
                .attr('class', 'x-label')
                .attr('text-anchor', 'middle')
                .attr('x', width / 2)
                .attr('y', height + 35)
                .text(this.featureNames[this.selectedDimensions.x]);

            // 添加Y轴标签
            g.append('text')
                .attr('class', 'y-label')
                .attr('text-anchor', 'middle')
                .attr('transform', 'rotate(-90)')
                .attr('x', -height / 2)
                .attr('y', -35)
                .text(this.featureNames[this.selectedDimensions.y]);

            // 绘制数据点
            g.selectAll('.data-point')
                .data(data)
                .enter()
                .append('circle')
                .attr('class', 'data-point')
                .attr('cx', d => xScale(d.x))
                .attr('cy', d => yScale(d.y))
                .attr('r', d => {
                    // 如果是三维数据，可以用Z值影响大小
                    if (this.featureCount > 2) {
                        const zMin = d3.min(data, d => d.z);
                        const zMax = d3.max(data, d => d.z);
                        const zRange = zMax - zMin;
                        // 计算半径 (从3到8)
                        return zRange === 0 ? 5 : 3 + ((d.z - zMin) / zRange) * 5;
                    }
                    return 5; // 默认半径
                })
                .attr('fill', d => this.colorMap[d.target] || '#409EFF')
                .attr('stroke', '#fff')
                .attr('stroke-width', 1)
                .attr('opacity', 0.7)
                .on('mouseover', (event, d) => {
                    this.showTooltip(event, d);
                })
                .on('mouseout', () => {
                    this.hideTooltip();
                });

            // 如果是标准模式，添加等比例指示器
            if (this.displayMode === 'standard') {
                // 添加一个对角线作为参考
                g.append('line')
                    .attr('class', 'reference-line')
                    .attr('x1', xScale(xMin))
                    .attr('y1', yScale(yMin))
                    .attr('x2', xScale(xMax))
                    .attr('y2', yScale(yMax))
                    .attr('stroke', '#ddd')
                    .attr('stroke-width', 1)
                    .attr('stroke-dasharray', '5,5')
                    .attr('opacity', 0.5);
            }
        },
        showTooltip(event, d) {
            // 构建提示信息
            let tooltipContent = `标签: ${d.target}<br/>`;
            tooltipContent += `${this.featureNames[this.selectedDimensions.x]}: ${d.x}<br/>`;

            if (this.featureCount > 1) {
                tooltipContent += `${this.featureNames[this.selectedDimensions.y]}: ${d.y}<br/>`;
            }

            if (this.featureCount > 2) {
                tooltipContent += `${this.featureNames[this.selectedDimensions.z]}: ${d.z}<br/>`;
            }

            // 显示tooltip
            this.tooltip
                .html(tooltipContent)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 28) + 'px')
                .transition()
                .duration(200)
                .style('opacity', 0.9);
        },
        hideTooltip() {
            this.tooltip
                .transition()
                .duration(500)
                .style('opacity', 0);
        },

        handleResize() {
            // 防抖动处理窗口大小变化
            clearTimeout(this.resizeTimer);
            this.resizeTimer = setTimeout(() => {
                this.renderChart();
            }, 300);
        }
    }
};
</script>

<style scoped>
.dataset-container {
    height: 100%;
    width: 97%;
    padding: 20px;
    background-color: #f5f7fa;
    border-radius: 4px;
    /* max-height: 90vh; */
    overflow-y: auto;
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.header-container h3 {
    margin: 0;
    color: #303133;
}

.display-controls {
    display: flex;
    align-items: center;
}

.display-controls .el-radio-group {
    margin-right: 15px;
}

.no-data-tip {
    height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.data-info {
    margin-bottom: 20px;
}

.info-card {
    margin-bottom: 20px;
}

.info-content {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

.info-content i {
    margin-right: 8px;
    font-size: 20px;
    color: #409EFF;
}

.dimension-selector {
    margin-bottom: 20px;
}

.dimension-options {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    max-height: 120px;
    overflow-y: auto;
    padding: 5px;
}

.dimension-item {
    display: flex;
    align-items: center;
}

.dimension-label {
    margin-right: 10px;
    font-weight: bold;
    min-width: 40px;
}

.dimension-notice {
    color: #909399;
    font-style: italic;
}

.visualization-container {
    margin-top: 20px;
}

.chart-container {
    width: 100%;
    height: 500px;
    position: relative;
    overflow: auto;
}

.chart-container.standard {
    height: 500px;
}

.chart-container.square {
    height: 600px;
}

.d3-chart {
    width: 100%;
    height: 100%;
}

.legend-container {
    margin-top: 20px;
    padding: 10px;
    border-top: 1px solid #EBEEF5;
    max-height: 150px;
    overflow-y: auto;
}

.legend-title {
    font-weight: bold;
    margin-bottom: 10px;
}

.legend-items {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    max-height: 100px;
    overflow-y: auto;
    padding-right: 10px;
}

.legend-item {
    display: flex;
    align-items: center;
}

.legend-color {
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: 3px;
    margin-right: 5px;
}

/* 自定义散点图样式 */
.data-point {
    cursor: pointer;
    transition: r 0.2s, opacity 0.2s;
}

.data-point:hover {
    /* r: 8; */
    opacity: 1 !important;
}

/* 自定义滚动条样式 */
.dataset-container::-webkit-scrollbar,
.chart-container::-webkit-scrollbar,
.legend-items::-webkit-scrollbar,
.dimension-options::-webkit-scrollbar,
.legend-container::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

.dataset-container::-webkit-scrollbar-track,
.chart-container::-webkit-scrollbar-track,
.legend-items::-webkit-scrollbar-track,
.dimension-options::-webkit-scrollbar-track,
.legend-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.dataset-container::-webkit-scrollbar-thumb,
.chart-container::-webkit-scrollbar-thumb,
.legend-items::-webkit-scrollbar-thumb,
.dimension-options::-webkit-scrollbar-thumb,
.legend-container::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.dataset-container::-webkit-scrollbar-thumb:hover,
.chart-container::-webkit-scrollbar-thumb:hover,
.legend-items::-webkit-scrollbar-thumb:hover,
.dimension-options::-webkit-scrollbar-thumb:hover,
.legend-container::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
</style>