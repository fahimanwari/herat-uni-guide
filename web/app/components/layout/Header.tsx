"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";

type NavItem = { href: string; label: string; badge?: string };
type NavEntry = { label: string; href?: string; children?: NavItem[] };

const navItems: NavEntry[] = [
  { label: "خانه", href: "/" },
  { label: "پوهنځی‌ها", href: "/faculties" },
  {
    label: "کانکور",
    children: [
      { href: "/mock-kankor", label: "کانکور آزمایشی", badge: "جدید" },
      { href: "/kankor/chance", label: "چانس قبولی" },
      { href: "/kankor", label: "راهنما و کات‌آف" },
    ],
  },
  { label: "اخبار", href: "/news" },
  { label: "پرسش‌های متداول", href: "/faq" },
  { label: "مشاور AI", href: "/chat" },
];

function ChevronDown({ className = "" }: { className?: string }) {
  return (
    <svg className={className} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 9l6 6 6-6" />
    </svg>
  );
}

function DesktopDropdown({ entry }: { entry: NavEntry }) {
  const [open, setOpen] = useState(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);

  const show = () => {
    if (closeTimer.current) clearTimeout(closeTimer.current);
    setOpen(true);
  };
  const hide = () => {
    closeTimer.current = setTimeout(() => setOpen(false), 120);
  };

  useEffect(() => {
    function onClickOutside(e: MouseEvent) {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  return (
    <div ref={rootRef} className="relative" onMouseEnter={show} onMouseLeave={hide}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex items-center gap-1 text-muted hover:text-primary-600 transition-colors font-medium"
      >
        {entry.label}
        <ChevronDown className={`transition-transform ${open ? "rotate-180" : ""}`} />
      </button>

      <div
        className={`absolute top-full right-0 pt-3 transition-all duration-150 ${
          open ? "opacity-100 translate-y-0 pointer-events-auto" : "opacity-0 -translate-y-1 pointer-events-none"
        }`}
      >
        <div className="min-w-[220px] rounded-[10px] border border-border bg-surface-card shadow-lg overflow-hidden">
          {entry.children!.map((child) => (
            <Link
              key={child.href}
              href={child.href}
              className="flex items-center justify-between px-4 py-3 text-sm text-foreground hover:bg-primary-50 dark:hover:bg-primary-900/30 transition-colors"
            >
              <span>{child.label}</span>
              {child.badge && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-gold-500 text-white">
                  {child.badge}
                </span>
              )}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileGroupOpen, setMobileGroupOpen] = useState<string | null>(null);

  return (
    <header className="sticky top-0 z-50 bg-surface-card/95 backdrop-blur-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold text-lg">
            ه
          </div>
          <div className="hidden sm:block">
            <div className="font-bold text-foreground text-lg leading-tight">پوهنتون هرات</div>
            <div className="text-xs text-muted">راهنمای هوشمند</div>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-7">
          {navItems.map((entry) =>
            entry.children ? (
              <DesktopDropdown key={entry.label} entry={entry} />
            ) : (
              <Link
                key={entry.href}
                href={entry.href!}
                className="text-muted hover:text-primary-600 transition-colors font-medium"
              >
                {entry.label}
              </Link>
            )
          )}
        </nav>

        {/* Mobile Toggle */}
        <button
          className="md:hidden p-2 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/30"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="منو"
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            {mobileOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile Nav */}
      {mobileOpen && (
        <nav className="md:hidden border-t border-border bg-surface-card px-4 py-2">
          {navItems.map((entry) =>
            entry.children ? (
              <div key={entry.label} className="border-b border-border last:border-b-0">
                <button
                  type="button"
                  onClick={() => setMobileGroupOpen(mobileGroupOpen === entry.label ? null : entry.label)}
                  className="w-full flex items-center justify-between py-3 text-muted hover:text-primary-600 transition-colors font-medium"
                >
                  {entry.label}
                  <ChevronDown className={`transition-transform ${mobileGroupOpen === entry.label ? "rotate-180" : ""}`} />
                </button>
                {mobileGroupOpen === entry.label && (
                  <div className="pb-2 pr-4 flex flex-col gap-1">
                    {entry.children.map((child) => (
                      <Link
                        key={child.href}
                        href={child.href}
                        className="flex items-center gap-2 py-2 text-sm text-foreground hover:text-primary-600 transition-colors"
                        onClick={() => {
                          setMobileOpen(false);
                          setMobileGroupOpen(null);
                        }}
                      >
                        {child.label}
                        {child.badge && (
                          <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-gold-500 text-white">
                            {child.badge}
                          </span>
                        )}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <Link
                key={entry.href}
                href={entry.href!}
                className="block py-3 text-muted hover:text-primary-600 transition-colors font-medium border-b border-border last:border-b-0"
                onClick={() => setMobileOpen(false)}
              >
                {entry.label}
              </Link>
            )
          )}
        </nav>
      )}
    </header>
  );
}
