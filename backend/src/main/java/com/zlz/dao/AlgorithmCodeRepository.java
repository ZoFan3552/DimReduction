package com.zlz.dao;

import com.zlz.pojo.AlgorithmCode;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface AlgorithmCodeRepository extends JpaRepository<AlgorithmCode, Long> {

    /**
     * 获取第一条算法代码记录
     * @return 算法代码记录
     */
    Optional<AlgorithmCode> findFirstByOrderById();
}