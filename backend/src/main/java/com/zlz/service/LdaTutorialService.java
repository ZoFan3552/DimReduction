package com.zlz.service;

import com.zlz.dao.LdaTutorialRepository;
import com.zlz.pojo.LdaTutorialProgress;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class LdaTutorialService {

    private final LdaTutorialRepository ldaTutorialRepository;

    public LdaTutorialService(LdaTutorialRepository ldaTutorialRepository) {
        this.ldaTutorialRepository = ldaTutorialRepository;
    }

    /**
     * 获取用户的LDA教程学习进度
     */
    public Map<String, Object> getUserProgress(String userId) {
        // 从数据库获取用户进度
        LdaTutorialProgress userProgress = ldaTutorialRepository.findByUserId(userId);

        Map<String, Object> result = new HashMap<>();

        if (userProgress != null) {
            // 构建已完成章节列表
            List<String> completedSections = new ArrayList<>();
            Map<String, String> answers = new HashMap<>();

            // 检查每个章节是否已完成，并获取用户回答
            checkAndAddSection(userProgress.getIntroductionToLda(), "introduction-to-lda", completedSections, answers);
            checkAndAddSection(userProgress.getDimensionalityReduction(), "dimensionality-reduction", completedSections, answers);
            checkAndAddSection(userProgress.getLdaMathematicalFoundation(), "lda-mathematical-foundation", completedSections, answers);
            checkAndAddSection(userProgress.getWithinClassScatter(), "within-class-scatter", completedSections, answers);
            checkAndAddSection(userProgress.getBetweenClassScatter(), "between-class-scatter", completedSections, answers);
            checkAndAddSection(userProgress.getEigenvalueFormulation(), "eigenvalue-formulation", completedSections, answers);
            checkAndAddSection(userProgress.getLdaImplementation(), "lda-implementation", completedSections, answers);
            checkAndAddSection(userProgress.getLdaVisualization(), "lda-visualization", completedSections, answers);
            checkAndAddSection(userProgress.getLdaApplications(), "lda-applications", completedSections, answers);

            result.put("completedSections", completedSections);
            result.put("answers", answers);
        } else {
            // 如果没有找到用户进度，返回空结果
            result.put("completedSections", new ArrayList<>());
            result.put("answers", new HashMap<>());
        }

        return result;
    }

    /**
     * 检查章节是否已完成并添加到列表中
     */
    private void checkAndAddSection(String sectionData, String sectionId,
                                    List<String> completedSections,
                                    Map<String, String> answers) {
        if (sectionData != null && !sectionData.isEmpty()) {
            // 如果章节数据不为空，则认为章节已完成
            completedSections.add(sectionId);
            // 添加用户回答
            answers.put(sectionId, sectionData);
        }
    }

    /**
     * 保存用户的LDA教程学习进度
     */
    @Transactional
    public void saveUserProgress(LdaTutorialProgress progressData) {
        // 检查用户是否已有进度记录
        LdaTutorialProgress existingProgress = ldaTutorialRepository.findByUserId(progressData.getUserId());

        if (existingProgress != null) {
            // 更新现有进度
            updateExistingProgress(existingProgress, progressData);
            ldaTutorialRepository.save(existingProgress);
        } else {
            // 创建新进度记录
            ldaTutorialRepository.save(progressData);
        }
    }

    /**
     * 更新已有的进度记录
     */
    private void updateExistingProgress(LdaTutorialProgress existing, LdaTutorialProgress newData) {
        // 只更新有值的字段，保留现有数据
        if (newData.getIntroductionToLda() != null) {
            existing.setIntroductionToLda(newData.getIntroductionToLda());
        }
        if (newData.getDimensionalityReduction() != null) {
            existing.setDimensionalityReduction(newData.getDimensionalityReduction());
        }
        if (newData.getLdaMathematicalFoundation() != null) {
            existing.setLdaMathematicalFoundation(newData.getLdaMathematicalFoundation());
        }
        if (newData.getWithinClassScatter() != null) {
            existing.setWithinClassScatter(newData.getWithinClassScatter());
        }
        if (newData.getBetweenClassScatter() != null) {
            existing.setBetweenClassScatter(newData.getBetweenClassScatter());
        }
        if (newData.getEigenvalueFormulation() != null) {
            existing.setEigenvalueFormulation(newData.getEigenvalueFormulation());
        }
        if (newData.getLdaImplementation() != null) {
            existing.setLdaImplementation(newData.getLdaImplementation());
        }
        if (newData.getLdaVisualization() != null) {
            existing.setLdaVisualization(newData.getLdaVisualization());
        }
        if (newData.getLdaApplications() != null) {
            existing.setLdaApplications(newData.getLdaApplications());
        }
    }

    /**
     * 保存用户对特定章节的回答
     */
    @Transactional
    public void saveUserAnswer(String userId, String sectionId, String answer) {
        // 获取或创建用户进度
        LdaTutorialProgress progress = ldaTutorialRepository.findByUserId(userId);
        if (progress == null) {
            progress = new LdaTutorialProgress();
            progress.setUserId(userId);
        }

        // 根据章节ID更新相应的回答字段
        switch (sectionId) {
            case "introduction-to-lda":
                progress.setIntroductionToLda(answer);
                break;
            case "dimensionality-reduction":
                progress.setDimensionalityReduction(answer);
                break;
            case "lda-mathematical-foundation":
                progress.setLdaMathematicalFoundation(answer);
                break;
            case "within-class-scatter":
                progress.setWithinClassScatter(answer);
                break;
            case "between-class-scatter":
                progress.setBetweenClassScatter(answer);
                break;
            case "eigenvalue-formulation":
                progress.setEigenvalueFormulation(answer);
                break;
            case "lda-implementation":
                progress.setLdaImplementation(answer);
                break;
            case "lda-visualization":
                progress.setLdaVisualization(answer);
                break;
            case "lda-applications":
                progress.setLdaApplications(answer);
                break;
            default:
                throw new IllegalArgumentException("未知的章节ID: " + sectionId);
        }

        // 保存更新
        ldaTutorialRepository.save(progress);
    }

    /**
     * 标记章节为已完成
     */
    @Transactional
    public void markSectionComplete(String userId, String sectionId) {
        // 获取用户进度
        LdaTutorialProgress progress = ldaTutorialRepository.findByUserId(userId);
        if (progress == null) {
            // 如果用户没有进度记录，则创建一个
            progress = new LdaTutorialProgress();
            progress.setUserId(userId);
        }

        // 检查章节是否已有回答，若无则提供一个默认值表示已完成
        String completionMark = "COMPLETED";

        switch (sectionId) {
            case "introduction-to-lda":
                if (isEmpty(progress.getIntroductionToLda())) {
                    progress.setIntroductionToLda(completionMark);
                }
                break;
            case "dimensionality-reduction":
                if (isEmpty(progress.getDimensionalityReduction())) {
                    progress.setDimensionalityReduction(completionMark);
                }
                break;
            case "lda-mathematical-foundation":
                if (isEmpty(progress.getLdaMathematicalFoundation())) {
                    progress.setLdaMathematicalFoundation(completionMark);
                }
                break;
            case "within-class-scatter":
                if (isEmpty(progress.getWithinClassScatter())) {
                    progress.setWithinClassScatter(completionMark);
                }
                break;
            case "between-class-scatter":
                if (isEmpty(progress.getBetweenClassScatter())) {
                    progress.setBetweenClassScatter(completionMark);
                }
                break;
            case "eigenvalue-formulation":
                if (isEmpty(progress.getEigenvalueFormulation())) {
                    progress.setEigenvalueFormulation(completionMark);
                }
                break;
            case "lda-implementation":
                if (isEmpty(progress.getLdaImplementation())) {
                    progress.setLdaImplementation(completionMark);
                }
                break;
            case "lda-visualization":
                if (isEmpty(progress.getLdaVisualization())) {
                    progress.setLdaVisualization(completionMark);
                }
                break;
            case "lda-applications":
                if (isEmpty(progress.getLdaApplications())) {
                    progress.setLdaApplications(completionMark);
                }
                break;
            default:
                throw new IllegalArgumentException("未知的章节ID: " + sectionId);
        }

        // 保存更新
        ldaTutorialRepository.save(progress);
    }

    /**
     * 检查字符串是否为空
     */
    private boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }
}