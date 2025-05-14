<template>
    <div>
        <el-tabs v-model="activeTab" type="card">
            <el-tab-pane label="相似度计算" name="similarity">
                <SimilarityMatrix :nodeData="nodeData" @applySimilarity="applyMatrix"></SimilarityMatrix>
            </el-tab-pane>
            <el-tab-pane label="协方差矩阵" name="covariance">
                <covariance-matrix :nodeData="nodeData" @calculation-complete="handleCalculationComplete" />
            </el-tab-pane>
            <el-tab-pane label="散度矩阵" name="LDAdivergence">
                <LDAdivergence :nodeData="nodeData" @applyLDAdivergence="applyLDAdivergence" />
            </el-tab-pane>
        </el-tabs>


    </div>
</template>

<script>
import SimilarityMatrix from './SimilarityMatrix.vue';
import CovarianceMatrix from './CovarianceMatrix.vue';
import LDAdivergence from './LDAdivergence.vue';


export default {
    // name: 'TabSwitcher',
    components: {
        SimilarityMatrix,
        CovarianceMatrix,
        LDAdivergence,

    },
    props: {
        nodeData: {
            type: Object,
            default: () => (null)
        }
    },
    data() {
        return {
            activeTab: 'similarity'
        }
    },
    // computed: {
    //     currentComponent() {
    //         return this.activeTab === 'A' ? 'ComponentA' : 'ComponentB'
    //     }
    // },

    methods: {
        handleCalculationComplete(data) {
            this.$emit("handleCalculationComplete", data);
        },
        applyMatrix(data) {
            this.$emit("applyMatrix", data);
        },
        applyLDAdivergence(data) {
            this.$emit("applyLDAdivergence", data);
        },
    }
}
</script>