package com.zlz.pojo;


import lombok.Getter;
import lombok.Setter;

/**
 * 用于接收保存代码请求的数据模型
 */
@Setter
@Getter
public class SaveCodeRequest {

    private String userId;
    private String algorithmType;
    private String code;
}