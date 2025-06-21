// src/app/dashboard/page.tsx

"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { fetchUser } from "@/lib/api";

export default function DashboardPage() {
  const searchParams = useSearchParams();
  const userId = searchParams.get("user_id");

  const [user, setUser] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadUser() {
      if (!userId) return;

      try {
        const data = await fetchUser(userId);
        setUser(data);
      } catch (err: any) {
        setError("Failed to load user");
      }
    }

    loadUser();
  }, [userId]);

  if (error) return <div className="text-red-500 p-4">{error}</div>;
  if (!user) return <div className="text-white p-4">Loading user...</div>;

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold mb-4">🎵 Welcome, {user.display_name}!</h1>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Country:</strong> {user.country}</p>
      <p><strong>User ID:</strong> {user.id}</p>
    </div>
  );
}
