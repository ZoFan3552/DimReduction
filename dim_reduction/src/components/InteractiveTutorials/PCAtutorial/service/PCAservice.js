// /service/PCAservice.js
import axios from '@/utils/myAxios';

// PCA教程进度服务
export const tutorialProgressService = {
    /**
     * 获取用户的教程进度
     * @param {string} userId 用户ID
     * @returns {Promise} 包含用户进度数据的Promise
     */
    getProgress(userId) {
        console.log("获取进度1", userId);
        return axios.get(`/tutorial/pca/progress/${userId}`);
    },

    /**
     * 保存用户的教程进度
     * @param {Object} progressData 包含进度信息的对象
     * @returns {Promise} 保存结果的Promise
     */
    saveProgress(progressData) {
        return axios.post('/tutorial/pca/progress', progressData);
    },

    /**
     * 更新特定章节的回答
     * @param {string} userId 用户ID
     * @param {string} segmentId 章节ID
     * @param {string} answer 用户的回答
     * @returns {Promise} 更新结果的Promise
     */
    updateSegmentAnswer(userId, segmentId, answer) {
        return axios.patch('/tutorial/pca/progress/answer', {
            userId,
            segmentId,
            answer
        });
    },

    /**
     * 标记章节为已完成
     * @param {string} userId 用户ID
     * @param {string} segmentId 章节ID
     * @returns {Promise} 更新结果的Promise
     */
    markSegmentComplete(userId, segmentId) {
        return axios.patch('/tutorial/pca/progress/complete', {
            userId,
            segmentId
        });
    }
};