const BASE_URL = "http://127.0.0.1:8000";

export async function getSpotifyLoginUrl(): Promise<string> {
    const res = await fetch(`${BASE_URL}/auth/login`);
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Login URL fetch failed: ${res.status} ${errorText}`);
    }
    const data = await res.json();
    return data.auth_url;
  }
  

export async function fetchUser(userId: string) {
  const res = await fetch(`${BASE_URL}/me/${userId}`);
  if (!res.ok) throw new Error("User not found");
  return res.json();
}
