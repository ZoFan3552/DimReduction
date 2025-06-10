package com.zlz.dao;


import com.zlz.pojo.TreeData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface TreeDataRepository extends JpaRepository<TreeData, Long> {
    Optional<TreeData> findByUserIdAndAlgorithmType(String userId, String algorithmType);
}
