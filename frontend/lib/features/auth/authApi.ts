import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// ==========================================
// ১. TypeScript Interfaces (Pydantic-এর মতো)
// ==========================================

// লগিন করার পর ব্যাকএন্ড আমাদের কী কী ডাটা ফেরত দেবে, তার ছাঁচ
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

// ==========================================
// ২. RTK Query API Setup
// ==========================================
export const authApi = createApi({
  reducerPath: 'authApi',
  // আমাদের FastAPI সার্ভারের মূল ঠিকানা
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:8000' }), 
  
  endpoints: (builder) => ({
    // লগিন করার এন্ডপয়েন্ট (POST রিকোয়েস্ট)
    login: builder.mutation<LoginResponse, URLSearchParams>({
      query: (formData) => ({
        url: '/auth/login',
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }),
    }),
  }),
});

// React-এর জন্য স্বয়ংক্রিয়ভাবে তৈরি হওয়া Hook
export const { useLoginMutation } = authApi;