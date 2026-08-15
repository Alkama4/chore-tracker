import { API_BASE_URL } from './conf';

export async function queryFastApi(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
        // Automatically stringify body if an object is passed
        ...(options.body && typeof options.body === "object" && {
            body: JSON.stringify(options.body)
        }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Handle empty responses (like 204 No Content on DELETE)
    return response.status !== 204 ? await response.json() : null;
}
