"use client";

import Link from "next/link";
import { ThemeToggle } from "@/components/ui/ThemeToggle";

export function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-gray-200/60 bg-white/80 backdrop-blur-xl dark:border-zinc-800/60 dark:bg-zinc-900/80">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-2xl font-bold text-brand-700 dark:text-brand-500">Alpha</span>
            <span className="text-2xl font-light text-gray-500 dark:text-zinc-400">Watch</span>
          </Link>
          <div className="flex items-center gap-6">
            <nav className="flex items-center gap-6">
              <Link href="/" className="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900 dark:text-zinc-400 dark:hover:text-white">
                Dashboard
              </Link>
              <Link href="/reports" className="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900 dark:text-zinc-400 dark:hover:text-white">
                Reports
              </Link>
              <Link href="/schedule" className="text-sm font-medium text-gray-600 transition-colors hover:text-gray-900 dark:text-zinc-400 dark:hover:text-white">
                Schedule
              </Link>
            </nav>
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>
  );
}
