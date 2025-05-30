package com.zlz.Dao;

import com.zlz.pojo.LdaTutorialProgress;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * LDA教程进度数据访问接口
 */
@Repository
public interface LdaTutorialRepository extends JpaRepository<LdaTutorialProgress, String> {

    /**
     * 根据用户ID查找教程进度
     * @param userId 用户ID
     * @return 用户的教程进度
     */
    LdaTutorialProgress findByUserId(String userId);
}