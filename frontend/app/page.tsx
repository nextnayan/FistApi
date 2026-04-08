import type { Metadata } from "next";


export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">
        Tailwind v4 + Next.js (TS) Ready! 🚀
      </h1>
     
    </div>
  );
}

export const metadata: Metadata = {
  title: "Redux Toolkit",
};
