import axios from "axios";

const instance = axios.create({
    baseURL: "http://localhost:8080/api", // Spring Boot 的 API 根路径
    timeout: 100000, // 请求超时时间
});

// 拦截请求（可选）
instance.interceptors.request.use(
    (config) => {
        // 可以在这里添加请求头信息
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 拦截响应（可选）
instance.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default instance;
