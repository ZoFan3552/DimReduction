package com.zlz.pojo;


/**
 * 用于接收保存代码请求的数据模型
 */
public class SaveCodeRequest {

    private String userId;
    private String algorithmType;
    private String code;

    // Getters and Setters

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getAlgorithmType() {
        return algorithmType;
    }

    public void setAlgorithmType(String algorithmType) {
        this.algorithmType = algorithmType;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }
}