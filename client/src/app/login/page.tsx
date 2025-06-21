"use client";

import { getSpotifyLoginUrl } from "@/lib/api";
import { useState } from "react";

export default function LoginPage() {
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    try {
      const authUrl = await getSpotifyLoginUrl();
      window.location.href = authUrl;
    } catch (error) {
      alert("Failed to get login URL");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold mb-6">Welcome to StreamHive 🎵</h1>
      <button
        onClick={handleLogin}
        className="bg-green-500 text-white px-6 py-3 rounded-xl hover:bg-green-600"
        disabled={loading}
      >
        {loading ? "Redirecting..." : "Login with Spotify"}
      </button>
    </div>
  );
}
