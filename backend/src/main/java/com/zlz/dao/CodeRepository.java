package com.zlz.dao;


import com.zlz.pojo.TutorialCode;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CodeRepository extends JpaRepository<TutorialCode, Long> {

    /**
     * 根据用户ID查找代码记录
     * @param userId 用户ID
     * @return 用户代码记录
     */
    Optional<TutorialCode> findByUserId(String userId);
}
