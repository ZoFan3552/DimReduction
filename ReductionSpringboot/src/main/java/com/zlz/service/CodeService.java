package com.zlz.service;

import com.zlz.Dao.AlgorithmCodeRepository;
import com.zlz.Dao.CodeRepository;
import com.zlz.pojo.AlgorithmCode;
import com.zlz.pojo.TutorialCode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CodeService {

    @Autowired
    private CodeRepository tutorialCodeRepository;

    @Autowired
    private AlgorithmCodeRepository algorithmCodeRepository;

    /**
     * 获取用户保存的代码
     * @param userId 用户ID
     * @param algorithmType 算法类型 (PCA, tSNE, UMAP)
     * @return 用户保存的代码，如果没有返回null
     */
    public String getUserCode(String userId, String algorithmType) {
        Optional<TutorialCode> userCode = tutorialCodeRepository.findByUserId(userId);

        if (userCode.isPresent()) {
            TutorialCode code = userCode.get();

            switch (algorithmType) {
                case "PCA":
                    return code.getPcaCode();
                case "tSNE":
                    return code.getTsneCode();
                case "UMAP":
                    return code.getUmapCode();
                default:
                    return null;
            }
        }

        return null;
    }

    /**
     * 获取标准算法代码
     * @param algorithmType 算法类型 (PCA, tSNE, UMAP)
     * @return 标准算法代码
     */
    public String getStandardCode(String algorithmType) {
        Optional<AlgorithmCode> algorithmCode = algorithmCodeRepository.findFirstByOrderById();

        if (algorithmCode.isPresent()) {
            AlgorithmCode code = algorithmCode.get();

            switch (algorithmType) {
                case "PCA":
                    return code.getPcaCode();
                case "LDA":
                    return code.getLdaCode();
                case "tSNE":
                    return code.getTsneCode();
                case "UMAP":
                    return code.getUmapCode();
                default:
                    return "# 未找到相应算法代码";
            }
        }

        return "# 标准算法代码数据库未初始化";
    }

    /**
     * 保存用户代码
     * @param userId 用户ID
     * @param algorithmType 算法类型
     * @param code 代码内容
     * @return 是否保存成功
     */
    public boolean saveUserCode(String userId, String algorithmType, String code) {
        try {
            // 查找用户是否已有代码记录
            Optional<TutorialCode> existingCode = tutorialCodeRepository.findByUserId(userId);
            TutorialCode tutorialCode;

            // 如果存在则更新，不存在则创建新记录
            if (existingCode.isPresent()) {
                tutorialCode = existingCode.get();
            } else {
                tutorialCode = new TutorialCode();
                tutorialCode.setUserId(userId);
            }

            // 根据算法类型更新相应字段
            switch (algorithmType) {
                case "PCA":
                    tutorialCode.setPcaCode(code);
                    break;
                case "LDA":
                    tutorialCode.setLdaCode(code);
                    break;
                case "tSNE":
                    tutorialCode.setTsneCode(code);
                    break;
                case "UMAP":
                    tutorialCode.setUmapCode(code);
                    break;
                default:
                    return false;
            }

            // 保存到数据库
            tutorialCodeRepository.save(tutorialCode);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
