// src/api/ldaTutorialService.js
import axios from '@/utils/myAxios';

/**
 * LDA教程进度管理服务
 */
export default {
    /**
     * 获取用户进度
     * @param {string} userId 用户ID
     * @returns {Promise} 包含用户进度的Promise对象
     */
    getUserProgress(userId) {
        return axios.get(`/lda-tutorial/progress/${userId}`);
    },

    /**
     * 保存用户进度
     * @param {Object} progressData 包含用户进度的对象
     * @returns {Promise} 操作结果的Promise对象
     */
    saveUserProgress(progressData) {
        return axios.post('/lda-tutorial/progress', progressData);
    },

    /**
     * 保存用户对特定章节的回答
     * @param {string} userId 用户ID
     * @param {string} sectionId 章节ID
     * @param {string} answer 用户回答
     * @returns {Promise} 操作结果的Promise对象
     */
    saveUserAnswer(userId, sectionId, answer) {
        return axios.post('/lda-tutorial/answer', {
            userId,
            sectionId,
            answer
        });
    },

    /**
     * 标记章节为已完成
     * @param {string} userId 用户ID
     * @param {string} sectionId 章节ID
     * @returns {Promise} 操作结果的Promise对象
     */
    markSectionComplete(userId, sectionId) {
        return axios.post('/lda-tutorial/complete-section', {
            userId,
            sectionId
        });
    }
};