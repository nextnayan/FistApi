import { configureStore } from '@reduxjs/toolkit';
import { authApi } from './features/auth/authApi'; // আমাদের বানানো API ইমপোর্ট করলাম

export const makeStore = () => {
  return configureStore({
    reducer: {
      // API-এর রিডিউসার যুক্ত করা
      [authApi.reducerPath]: authApi.reducer,
    },
    // API ক্যাশিং, পোলিং এবং অন্যান্য ফিচারের জন্য মিডলওয়্যার যুক্ত করা
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(authApi.middleware),
  });
};

// TypeScript-এর জন্য স্টোরের টাইপগুলো (ডিফল্ট টেমপ্লেটে এগুলো থাকেই)
export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore['getState']>;
export type AppDispatch = AppStore['dispatch'];