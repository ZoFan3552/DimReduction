package com.zlz.service;

import com.zlz.dao.PcaTutorialRepository;
import com.zlz.pojo.PcaTutorialProgress;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.Optional;

@Service
public class PcaTutorialService {

    private final PcaTutorialRepository pcaTutorialRepository;

    @PersistenceContext
    private EntityManager entityManager;

    private final String[] segmentIds = {
            "intro-to-pca",
            "data-variance",
            "covariance-matrix",
            "eigenvectors",
            "selecting-pcs",
            "dimensionality-reduction",
            "pca-applications",
            "pca-limitations",
            "practical-example"
    };

    public PcaTutorialService(PcaTutorialRepository pcaTutorialRepository) {
        this.pcaTutorialRepository = pcaTutorialRepository;
    }

    /**
     * 获取用户教程进度
     * @param userId 用户ID
     * @return 用户进度数据
     */
    public PcaTutorialProgress getUserProgress(String userId) {
        Optional<PcaTutorialProgress> userProgressOpt = pcaTutorialRepository.findById(userId);
        return userProgressOpt.orElse(new PcaTutorialProgress());
    }

    /**
     * 保存用户教程进度
     * @param progressData 进度数据
     * @return 保存后的进度数据
     */
    public PcaTutorialProgress saveUserProgress(PcaTutorialProgress progressData) {
        return pcaTutorialRepository.save(progressData);
    }

    /**
     * 更新章节回答
     * @param userId 用户ID
     * @param segmentId 章节ID
     * @param answer 用户回答
     * @return 是否更新成功
     */
    @Transactional
    public boolean updateSegmentAnswer(String userId, String segmentId, String answer) {
        Optional<PcaTutorialProgress> progressOpt = pcaTutorialRepository.findById(userId);

        if (progressOpt.isPresent()) {
            PcaTutorialProgress progress = progressOpt.get();
            progress.setValueBySegmentId(segmentId, answer);
            pcaTutorialRepository.save(progress);
            return true;
        } else {
            // 如果用户记录不存在，创建新记录
            PcaTutorialProgress newProgress = new PcaTutorialProgress();
            newProgress.setUserId(userId);
            newProgress.setCompleteCount(0); // 默认完成数为0
            newProgress.setValueBySegmentId(segmentId, answer);
            pcaTutorialRepository.save(newProgress);
            return true;
        }
    }

    /**
     * 标记章节为已完成
     * @param userId 用户ID
     * @param segmentId 章节ID
     * @return 是否更新成功
     */
    @Transactional
    public boolean markSegmentComplete(String userId, String segmentId) {
        Optional<PcaTutorialProgress> progressOpt = pcaTutorialRepository.findById(userId);

        if (progressOpt.isPresent()) {
            PcaTutorialProgress progress = progressOpt.get();

            // 找到当前章节的索引
            int currentIndex = -1;
            for (int i = 0; i < segmentIds.length; i++) {
                if (segmentIds[i].equals(segmentId)) {
                    currentIndex = i;
                    break;
                }
            }

            if (currentIndex != -1) {
                // 更新完成的章节数（索引+1表示完成的数量）
                int newCompleteCount = currentIndex + 1;

                // 只有当新完成数大于当前完成数时才更新
                if (newCompleteCount > progress.getCompleteCount()) {
                    progress.setCompleteCount(newCompleteCount);
                    pcaTutorialRepository.save(progress);
                }
                return true;
            }
            return false;
        } else {
            // 如果用户记录不存在，创建新记录
            PcaTutorialProgress newProgress = new PcaTutorialProgress();
            newProgress.setUserId(userId);

            // 找到当前章节的索引并设置完成数
            for (int i = 0; i < segmentIds.length; i++) {
                if (segmentIds[i].equals(segmentId)) {
                    newProgress.setCompleteCount(i + 1);
                    break;
                }
            }

            pcaTutorialRepository.save(newProgress);
            return true;
        }
    }

    /**
     * 执行原生SQL语句更新章节回答
     * @param userId 用户ID
     * @param segmentId 章节ID
     * @param answer 用户回答
     * @return 是否更新成功
     */
    @Transactional
    public boolean updateSegmentAnswerNative(String userId, String segmentId, String answer) {
        // 为了防止SQL注入，我们需要验证segmentId是否合法
        boolean isValidSegmentId = false;
        for (String validId : segmentIds) {
            if (validId.equals(segmentId)) {
                isValidSegmentId = true;
                break;
            }
        }

        if (!isValidSegmentId) {
            throw new IllegalArgumentException("无效的章节ID");
        }

        // 使用原生SQL语句更新
        String sql = String.format("UPDATE PCA_tutorial SET `%s` = ? WHERE userId = ?", segmentId);
        int updatedRows = entityManager.createNativeQuery(sql)
                .setParameter(1, answer)
                .setParameter(2, userId)
                .executeUpdate();

        if (updatedRows > 0) {
            return true;
        } else {
            // 如果没有更新任何行，创建新记录
            PcaTutorialProgress newProgress = new PcaTutorialProgress();
            newProgress.setUserId(userId);
            newProgress.setCompleteCount(0);
            newProgress.setValueBySegmentId(segmentId, answer);
            pcaTutorialRepository.save(newProgress);
            return true;
        }
    }
}