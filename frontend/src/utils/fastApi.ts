import { API_BASE_URL } from './conf';

export async function queryFastApi<T = any>(
    path: string, 
    options: RequestInit & { body?: any } = {}
): Promise<T> {
    const { body, ...customConfig } = options;

    const config: RequestInit = {
        method: 'GET', // Default to GET if unspecified
        ...customConfig,
        headers: {
            'Content-Type': 'application/json',
            ...customConfig.headers,
        },
    };

    if (body !== undefined) {
        config.body = typeof body === 'string' ? body : JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${path}`, config);

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.status !== 204 ? await response.json() : null;
}