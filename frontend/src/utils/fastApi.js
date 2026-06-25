import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import { API_BASE_URL } from './conf';
import router from '@/router';

// Axios client
export const fastApi = axios.create({
    baseURL: API_BASE_URL,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true // important so cookies are sent automatically
});


// Set the access token into the headers
fastApi.interceptors.request.use((config) => {
    const auth = useAuthStore();

    // Attach token if available
    if (auth.accessToken) {
        config.headers.Authorization = `Bearer ${auth.accessToken}`;
    }

    return config;
});

// Response interceptor for automatic refresh
fastApi.interceptors.response.use(
    response => response,
    async error => {
        const auth = useAuthStore();
        const originalRequest = error.config;

        const isAuthEndpoint =
            originalRequest.url.startsWith('/auth/') &&
            !originalRequest.url.startsWith('/auth/me');

        if (
            error.response?.status === 401 &&
            !originalRequest._retry &&
            !isAuthEndpoint
        ) {
            originalRequest._retry = true;
            try {
                await auth.refresh();
                originalRequest.headers.Authorization = `Bearer ${auth.accessToken}`;
                return fastApi(originalRequest);
            } catch {
                auth.accessToken = null;
                router.push({
                    path: '/login',
                    query: { redirect_reason: 'session_expired' }
                })
            }
        }

        return Promise.reject(error);
    }
);
