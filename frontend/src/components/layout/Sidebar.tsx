"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/reports", label: "Reports" },
  { href: "/schedule", label: "Schedule" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-56 shrink-0 border-r border-gray-200/60 bg-gray-50/80 backdrop-blur-xl dark:border-zinc-800/60 dark:bg-zinc-900/50 lg:block">
      <nav className="flex flex-col gap-1 p-4">
        {links.map((link) => {
          const active = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`rounded-lg px-3 py-2 text-sm font-medium transition-all duration-200 ${
                active
                  ? "bg-brand-100 text-brand-700 shadow-sm dark:bg-brand-500/10 dark:text-brand-500"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-white"
              }`}
            >
              {link.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
