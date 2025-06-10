package com.zlz.controller;

import com.zlz.pojo.TreeData;
import com.zlz.pojo.TreeDataSaveRequest;
import com.zlz.service.TreeDataService;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/treeData")
@CrossOrigin(origins = "*")
public class TreeDataController {

    private final TreeDataService treeDataService;

    public TreeDataController(TreeDataService treeDataService) {
        this.treeDataService = treeDataService;
    }

    @GetMapping("/{userId}/{algorithmType}")
    @Operation(summary = "获取算法类型")
    public ResponseEntity<?> getTreeData(@PathVariable String userId, @PathVariable String algorithmType) {
        TreeData treeData = treeDataService.getTreeData(userId, algorithmType);
        return ResponseEntity.ok(treeData);
    }

    @PostMapping("/save")
    @Operation(summary = "保存TreeData")
    public ResponseEntity<?> saveTreeData(@RequestBody TreeDataSaveRequest request) {
        treeDataService.saveTreeData(request.getUserId(), request.getAlgorithmType(), request.getTreeData());
        return ResponseEntity.ok().build();
    }
}
