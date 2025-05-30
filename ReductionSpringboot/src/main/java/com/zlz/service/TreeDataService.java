package com.zlz.service;


import com.zlz.Dao.TreeDataRepository;
import com.zlz.pojo.TreeData;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.Optional;

@Service
public class TreeDataService {

    @Autowired
    private TreeDataRepository treeDataRepository;

    public TreeData getTreeData(String userId, String algorithmType) {
        return treeDataRepository.findByUserIdAndAlgorithmType(userId, algorithmType)
                .orElse(null);
    }

    public void saveTreeData(String userId, String algorithmType, String treeData) {
        TreeData entity = treeDataRepository.findByUserIdAndAlgorithmType(userId, algorithmType)
                .orElse(new TreeData());

        entity.setUserId(userId);
        entity.setAlgorithmType(algorithmType);
        entity.setTreeData(treeData);
        entity.setLastUpdated(new Date());

        treeDataRepository.save(entity);
    }
}
