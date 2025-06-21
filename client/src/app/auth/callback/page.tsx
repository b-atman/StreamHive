"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function CallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get("code");
      if (!code) {
        alert("Missing authorization code");
        return;
      }

      try {
        const res = await fetch(`http://127.0.0.1:8000/auth/callback?code=${code}`);
        const data = await res.json();
        const userId = data.user_id;
        router.push(`/dashboard?user_id=${userId}`);
      } catch (err) {
        console.error(err);
        alert("Login failed");
      }
    };

    handleCallback();
  }, [searchParams, router]);

  return (
    <div className="flex items-center justify-center h-screen">
      <p className="text-xl">Logging you in...</p>
    </div>
  );
}
