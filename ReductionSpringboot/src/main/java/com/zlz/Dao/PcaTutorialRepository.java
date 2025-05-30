package com.zlz.Dao;


import com.zlz.pojo.PcaTutorialProgress;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public interface PcaTutorialRepository extends JpaRepository<PcaTutorialProgress, String> {

    /**
     * 根据用户ID和章节ID更新章节答案
     * @param userId 用户ID
     * @param columnName 列名（章节ID）
     * @param answer 用户回答
     * @return 更新的行数
     */
    @Modifying
    @Query(
            value = "UPDATE PCA_tutorial SET :columnName = :answer WHERE userId = :userId",
            nativeQuery = true
    )
    int updateSegmentAnswer(
            @Param("userId") String userId,
            @Param("columnName") String columnName,
            @Param("answer") String answer
    );
    /**
     * 更新用户已完成的章节数
     * @param userId 用户ID
     * @param completeCount 已完成章节数
     * @return 更新的行数
     */
    @Modifying
    @Transactional
    @Query("UPDATE PcaTutorialProgress p SET p.completeCount = :completeCount WHERE p.userId = :userId")
    int updateCompleteCount(@Param("userId") String userId, @Param("completeCount") int completeCount);
}
