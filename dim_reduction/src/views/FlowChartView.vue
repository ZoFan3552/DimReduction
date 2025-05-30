<template>
    <div style="height: 90vh;overflow: hidden;">
        <split-pane split="vertical" :min-percent="20" :default-percent="50">
            <!-- 左半边：上下分割 -->
            <template slot="paneL">
                <div style="height: 100%;">
                    <split-pane split="horizontal" :min-percent="20" :default-percent="50">
                        <template slot="paneL">
                            <div class="area-a">
                                <dataset-display :nodeData="nodeData"></dataset-display>
                            </div>
                        </template>
                        <template slot="paneR">
                            <div class="area-c">

                                <NodeDetailDisplay :nodeData="nodeData"></NodeDetailDisplay>
                            </div>
                        </template>
                    </split-pane>
                </div>
            </template>

            <!-- 右半边：上下分割 -->
            <template slot="paneR">
                <div style="height: 100%;">
                    <split-pane split="horizontal" :min-percent="20" :default-percent="50">
                        <template slot="paneL">
                            <div class="area-b">

                                <FlowChart class="flowChart-section" :treeData="treeData" @node-selected="nodeSelected"
                                    @node-contextmenu="nodeContextmenu">
                                </FlowChart>
                            </div>
                        </template>
                        <template slot="paneR">
                            <div class="area-d">

                                <operation-board :nodeData="nodeData" @datasetImported="datasetImported"
                                    @coordinatesInitialized="coordinatesInitialized" @gradientUpdated="gradientUpdated"
                                    @handleCalculationComplete="handleCalculationComplete"
                                    @analysisComplete="analysisComplete" @projectionComplete="projectionComplete"
                                    @applyMatrix="applyMatrix" @applyPreprocessing="applyPreprocessing"
                                    @applyLDAdivergence="applyLDAdivergence"></operation-board>
                            </div>
                        </template>
                    </split-pane>
                </div>
            </template>
        </split-pane>
    </div>
</template>

<script>
import SplitPane from 'vue-splitpane';
import DatasetDisplay from '@/components/mainComponents/graphicsComponents/multipleDisplay/DatasetDisplay.vue';
import FlowChart from '@/components/mainComponents/graphicsComponents/FlowChart.vue'
import OperationBoard from "@/components/mainComponents/graphicsComponents/multipleDisplay/OperationBoard.vue";
import NodeDetailDisplay from "@/components/mainComponents/graphicsComponents/multipleDisplay/NodeDetailDisplay.vue";
import axios from '@/utils/myAxios.js'; // 导入axios用于HTTP请求

export default {
    components: {
        SplitPane,
        DatasetDisplay,
        FlowChart,
        OperationBoard,
        NodeDetailDisplay,
    },
    props: {
        // 接收从父组件传递的算法类型参数
        algorithmType: {
            type: String,
            default: 'common',
            validator: function (value) {
                // 验证算法类型是否有效
                return ['PCA', 'LDA', 'tSNE', 'UMAP', 'common'].includes(value);
            }
        }
    },
    data() {
        return {
            nodeData: null,
            newNode: null,
            userId: null, // 用户ID
            isSaving: false, // 防止多次保存操作的标志
            saveTimeout: null, // 用于延迟保存操作的定时器
            // 默认treeData
            treeData: {
                "id": "1",
                "selected": false,
                "operation": "原始数据集",
                "parameters": {},
                "target_names": [],
                "target": [],
                "feature_names": [],
                "dataset": [],
                "computed": {},
                "children": []
            },
        }
    },
    watch: {
        // 监听treeData的变化，当发生变化时自动保存
        treeData: {
            handler: function () {
                this.saveTreeDataDebounced();
            },
            deep: true // 深度监听，检测嵌套对象的变化
        }
    },
    created() {
        // 从localStorage获取userId
        this.userId = localStorage.getItem('userId');

        // 根据用户登录状态加载树数据
        this.loadTreeData();
    },
    methods: {

        // 加载树数据
        loadTreeData() {
            if (this.userId) {
                // 用户已登录，从数据库加载
                this.loadUserTreeData();
            } else {
                // 用户未登录，使用默认树数据
                console.log('用户未登录，使用默认treeData');
            }
        },

        // 从数据库加载用户的树数据
        loadUserTreeData() {
            axios.get(`/treeData/${this.userId}/${this.algorithmType}`)
                .then(response => {
                    if (response && response.treeData) {
                        // 从响应中设置treeData
                        this.$set(this, 'treeData', JSON.parse(response.treeData));
                        console.log('从数据库加载用户treeData成功');
                    } else {
                        console.log('未找到保存的treeData，使用默认值');
                    }
                })
                .catch(error => {
                    console.error('加载treeData错误:', error);
                });
        },

        // 延迟保存treeData，防止频繁保存
        saveTreeDataDebounced() {
            // 只有用户登录时才保存
            if (!this.userId) {
                console.log('用户未登录，treeData不保存');
                return;
            }

            // 清除现有的定时器
            if (this.saveTimeout) {
                clearTimeout(this.saveTimeout);
            }

            // 设置新的定时器，1秒钟不活动后保存
            this.saveTimeout = setTimeout(() => {
                this.saveTreeData();
            }, 1000);
        },

        // 保存treeData到数据库
        saveTreeData() {
            // 防止多次保存操作
            if (this.isSaving) {
                return;
            }

            this.isSaving = true;

            const payload = {
                userId: this.userId,
                algorithmType: this.algorithmType,
                treeData: JSON.stringify(this.treeData)
            };

            axios.post('/treeData/save', payload)
                .then(response => {
                    console.log("treeData保存回应", response);
                    console.log('TreeData保存成功');
                })
                .catch(error => {
                    console.error('保存treeData错误:', error);
                })
                .finally(() => {
                    this.isSaving = false;
                });
        },

        // 修改现有的nodeContextmenu方法
        nodeContextmenu({ option, node }) {
            // 原有代码保持不变
            if (option !== 'delete' || !node?.id || node.id === 'root') {
                console.warn('根节点不可删除');
                return;
            }

            // 深拷贝避免污染原始数据
            const treeDataCopy = JSON.parse(JSON.stringify(this.treeData));

            // 执行删除
            const newTreeData = this.deleteNodeById(treeDataCopy, node.id);

            // 更新响应式数据
            this.$set(this, 'treeData', newTreeData);
            // watcher会处理保存更新后的treeData
        },

        deleteNodeById(nodeOrNodes, targetId) {
            if (Array.isArray(nodeOrNodes)) {
                return nodeOrNodes
                    .filter(node => node.id !== targetId)
                    .map(node => ({
                        ...node,
                        children: this.deleteNodeById(node.children, targetId)
                    }));
            }
            else if (typeof nodeOrNodes === 'object' && nodeOrNodes !== null) {
                // 根节点会走到这里，但已经被 handleDeleteNode 拦截
                return {
                    ...nodeOrNodes,
                    children: this.deleteNodeById(nodeOrNodes.children, targetId)
                };
            }
            return nodeOrNodes;
        },
        generateId() {
            return '_' + Math.random().toString(36).substr(2, 9);
        },

        addNewNodeToTree(nodeData, newNode) {
            console.log("加入节点", newNode);

            // 确保 nodeData 有 children 数组
            if (!nodeData.children) {
                this.$set(nodeData, 'children', []);
            }

            if (nodeData.nodeType === "loop") {
                // 找到 newNode 的最深层 children 节点
                let deepest = newNode;
                while (deepest.children && deepest.children.length > 0) {
                    deepest = deepest.children[0]; // 如果有多个子节点你可以自定义策略
                }

                // 确保 deepest 有 children 属性
                if (!deepest.children) {
                    this.$set(deepest, 'children', []);
                }

                // 将原 nodeData 的 children 挂到 deepest.children 上
                deepest.children.push(...nodeData.children);
                newNode.nodeType = "loop";
                // 替换整个 nodeData.children 为 newNode
                nodeData.children = [newNode];
            } else {
                // 正常情况直接添加
                nodeData.children.push(newNode);
            }
        },

        nodeSelected(nodeData) {
            this.nodeData = nodeData;
        },



        datasetImported(data) {
            console.log("接受到数据集进行导入", data)
            this.treeData = data;
            //重新处理树
        },

        applyMatrix(data) {
            this.addNewNodeToTree(this.nodeData, data);
        },
        applyLDAdivergence(data) {
            this.addNewNodeToTree(this.nodeData, data);
        },

        applyPreprocessing(data) {
            this.addNewNodeToTree(this.nodeData, data);
        },

        projectionComplete(data) {
            this.addNewNodeToTree(this.nodeData, data);
        },

        analysisComplete(data) {
            this.addNewNodeToTree(this.nodeData, data);
        },

        gradientUpdated(data) {

            this.addNewNodeToTree(this.nodeData, data);
        },

        handleCalculationComplete(data) {
            this.addNewNodeToTree(this.nodeData, data);
        },

        coordinatesInitialized(data) {
            const newNode = {
                "id": this.generateId(),
                "selected": false,
                "operation": "生成低维空间",
                // "nodeType": "common",
                "parameters": {
                    method: data.method,

                },
                "target": this.nodeData.target,
                "dataset": data.coordinates,
                "computed": this.nodeData.computed,
                "children": []
            }

            this.addNewNodeToTree(this.nodeData, newNode);
        },

    },
};
</script>

<style scoped>
/* 分别命名四个区域（方便后续定位） */
.area-a {
    height: 100%;
    background-color: #f8f8f8;
}

.area-b {
    height: 100%;
    background-color: #f0f0f0;
}

.area-c {
    height: 100%;
    background-color: #e8e8e8;
}

.area-d {
    height: 100%;
    background-color: #e0e0e0;

}
</style>