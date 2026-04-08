"use client"; // ১. Next.js-কে বলছি এটি ক্লায়েন্ট কম্পোনেন্ট

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useLoginMutation } from "@/lib/features/auth/authApi"; // আমাদের বানানো হুক

export default function LoginPage() {
  const router = useRouter(); // অন্য পেজে রিডাইরেক্ট করার জন্য

  // ২. ফর্মের ডাটা ধরে রাখার জন্য State
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // ৩. RTK Query Hook ব্যবহার করা
  const [login, { isLoading, isError, error }] = useLoginMutation();

  // ৪. ফর্ম সাবমিট করার ফাংশন (TypeScript Best Practice)
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault(); // পেজ রিলোড হওয়া বন্ধ করে

    // FastAPI-এর জন্য Form Data তৈরি করা (যেহেতু আমাদের ব্যাকএন্ড Form Data চায়, JSON নয়)
    const formData = new URLSearchParams();
    formData.append("username", email); // FastAPI-তে ফিল্ডের নাম 'username' ছিল
    formData.append("password", password);

    try {
      // .unwrap() হলো RTK Query এর Best Practice। 
      // এটি সফল হলে সরাসরি ডাটা দেয়, আর ব্যর্থ হলে সরাসরি catch ব্লকে পাঠিয়ে দেয়।
      const response = await login(formData).unwrap();
      
      // ৫. টোকেন সেভ করা
      console.log("Login Success!", response);
      localStorage.setItem("token", response.access_token);
      
      // ৬. সফল হলে ড্যাশবোর্ডে পাঠিয়ে দেওয়া (আপাতত হোম পেজে পাঠাচ্ছি)
      router.push("/");
      
    } catch (err) {
      console.error("Login Failed:", err);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
        <h2 className="mb-6 text-center text-2xl font-bold text-gray-800">
          Sign In (FastAPI + Next.js)
        </h2>

        {/* এরর মেসেজ দেখানো */}
        {isError && (
          <div className="mb-4 rounded bg-red-100 p-3 text-sm text-red-700">
            ইমেইল অথবা পাসওয়ার্ড ভুল হয়েছে!
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 w-full rounded-md border border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
              placeholder="test@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 w-full rounded-md border border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading} // লোডিং অবস্থায় বাটন ডিজেবল থাকবে
            className="w-full rounded-md bg-blue-600 p-2 text-white transition hover:bg-blue-700 disabled:bg-blue-400"
          >
            {isLoading ? "লগিন হচ্ছে..." : "লগিন করুন"}
          </button>
        </form>
      </div>
    </div>
  );
}