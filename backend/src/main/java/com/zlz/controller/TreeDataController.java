package com.zlz.controller;

import com.zlz.pojo.TreeData;
import com.zlz.pojo.TreeDataSaveRequest;
import com.zlz.service.TreeDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/treeData")
@CrossOrigin(origins = "*")
public class TreeDataController {

    @Autowired
    private TreeDataService treeDataService;

    @GetMapping("/{userId}/{algorithmType}")
    public ResponseEntity<?> getTreeData(@PathVariable String userId, @PathVariable String algorithmType) {
        TreeData treeData = treeDataService.getTreeData(userId, algorithmType);
        return ResponseEntity.ok(treeData);
    }

    @PostMapping("/save")
    public ResponseEntity<?> saveTreeData(@RequestBody TreeDataSaveRequest request) {
        treeDataService.saveTreeData(request.getUserId(), request.getAlgorithmType(), request.getTreeData());
        return ResponseEntity.ok().build();
    }
}
