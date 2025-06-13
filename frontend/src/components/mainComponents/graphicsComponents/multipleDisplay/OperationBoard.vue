<template>
    <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="数据集导入" name="dataImport">
            <DataImport @datasetImported="datasetImported"></DataImport>
        </el-tab-pane>

        <el-tab-pane label="预处理" name="pre-processing">
            <PreProcessing :nodeData="nodeData" @applyPreprocessing="applyPreprocessing"></PreProcessing>
        </el-tab-pane>

        <!-- <el-tab-pane label="协方差矩阵" name="covariance-matrix">
            <covariance-matrix :nodeData="currentNode" @calculation-complete="handleCalculationComplete" />
        </el-tab-pane> -->



        <el-tab-pane label="矩阵计算" name="second">
            <MatrixProcessBoard :nodeData="nodeData" @applyMatrix="applyMatrix"
                @handleCalculationComplete="handleCalculationComplete" @applyLDAdivergence="applyLDAdivergence"></MatrixProcessBoard>
        </el-tab-pane>

        <el-tab-pane label="特征值计算" name="eigenvalue">
            <EigenvalueCalculation :nodeData="nodeData" @analysis-complete="analysisComplete"></EigenvalueCalculation>
        </el-tab-pane>


        <!-- <el-tab-pane label="数值计算" name="szjs">
            <NumericalCalculationBoard></NumericalCalculationBoard>
        </el-tab-pane> -->

        <el-tab-pane label="投影" name="third">
            <ProjectionOperate :nodeData="nodeData" @projection-complete="projectionComplete"></ProjectionOperate>
        </el-tab-pane>

        <el-tab-pane label="低维空间生成" name="lowDimSpace">

            <LowDimGenerator :nodeData="nodeData" @coordinates-initialized="coordinatesInitialized"></LowDimGenerator>

        </el-tab-pane>
        <el-tab-pane label="梯度下降" name="tdxj">
            <GradientDescentBoard :nodeData="nodeData" @gradient-updated="gradientUpdated"></GradientDescentBoard>
        </el-tab-pane>

    </el-tabs>
</template>
<script>
import PreProcessing from '@/components/basicOperations/PreProcessing.vue';
import MatrixProcessBoard from '@/components/basicOperations/matrixProcess/MatrixProcessBoard.vue';
// import NumericalCalculationBoard from '@/components/basicOperations/NumericalCalculation/NumericalCalculationBoard.vue';
import GradientDescentBoard from '@/components/basicOperations/gradientDescent/GradientDescentBoard.vue';
import DataImport from '@/components/basicOperations/dataImport/DataImport.vue';
import LowDimGenerator from '@/components/basicOperations/lowDimSpaceGenerator/LowDimGenerator.vue';
import EigenvalueCalculation from '@/components/basicOperations/eigenvalueCalcu/EigenvalueCalculation.vue';
import ProjectionOperate from '@/components/basicOperations/projectionOperation/ProjectionOperate.vue';
export default {
    components: {
        PreProcessing,
        MatrixProcessBoard,
        // NumericalCalculationBoard,
        GradientDescentBoard,
        DataImport,
        LowDimGenerator,
        EigenvalueCalculation,
        ProjectionOperate,
    },
    props: {
        nodeData: {
            type: Object,
            default: () => (null)
        }
    },
    data() {
        return {
            activeName: 'dataImport'
        };
    },
    methods: {
        applyMatrix(data) {
            this.$emit("applyMatrix", data);
        },
        handleClick(tab, event) {
            console.log(tab, event);
        },

        applyPreprocessing(data) {
            this.$emit("applyPreprocessing", data);
        },
        applyLDAdivergence(data){
            this.$emit("applyLDAdivergence", data);
        },

        applyOperation(operation) {
            this.$emit("applyOperation", operation);
        },

        projectionComplete(data) {
            this.$emit("projectionComplete", data);
        },

        handleCalculationComplete(data) {
            this.$emit("handleCalculationComplete", data);
        },

        datasetImported(data) {
            // console.log("接受到数据集进行导入1", data)
            this.$emit("datasetImported", data);
        },

        analysisComplete(data) {
            this.$emit("analysisComplete", data);
        },

        coordinatesInitialized(data) {
            this.$emit("coordinatesInitialized", data);
            console.log("低维空间生成", data);
        },

        gradientUpdated(data) {
            this.$emit("gradientUpdated", data);
            console.log("梯度下降", data);
        }
    }
};
</script>

<style>
.el-tabs {
    height: 100%;
    flex: 1;
    display: flex;
    flex-direction: column;
}



.el-tabs__content {
    /* height: 90%; */
    flex: 1;
    overflow-y: auto;
}
</style>