import { API_BASE_URL } from './conf';

export const fastApi = async (endpoint, options = {}) => {
    const { method = 'GET', params, body, ...customConfig } = options;

    let url = `${API_BASE_URL}${endpoint}`;
    if (params) {
        const searchParams = new URLSearchParams(params).toString();
        url += `?${searchParams}`;
    }

    const config = {
        method,
        headers: { 'Content-Type': 'application/json', ...customConfig.headers },
        credentials: 'include', // This is the 'withCredentials' equivalent for cookies
        ...customConfig,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    const response = await fetch(url, config);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
};
