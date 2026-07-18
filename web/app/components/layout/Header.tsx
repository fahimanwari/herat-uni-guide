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
      { href: "/quiz", label: "آزمون انتخاب رشته" },
    ],
  },
  { label: "اخبار", href: "/news" },
  { label: "پرسش‌های متداول", href: "/faq" },
  { label: "مشاور AI", href: "/chat" },
  { label: "نقشه کمپس", href: "/campus" },
];

const languages = [
  { code: "fa", label: "دری" },
  { code: "ps", label: "پشتو" },
  { code: "en", label: "English" },
];

function ChevronDown({ className = "" }: { className?: string }) {
  return (
    <svg className={className} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 9l6 6 6-6" />
    </svg>
  );
}

function SearchIcon() {
  return (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  );
}

function SunIcon() {
  return (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  );
}

function MoonIcon() {
  return (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
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
        <div className="min-w-[240px] rounded-[10px] border border-border bg-surface-card shadow-lg overflow-hidden">
          {entry.children!.map((child) => (
            <Link
              key={child.href}
              href={child.href}
              className="flex items-center justify-between px-4 py-3 text-sm text-foreground hover:bg-primary-50 transition-colors"
            >
              <span>{child.label}</span>
              {child.badge && (
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-gold-500 text-white">
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
  const [darkMode, setDarkMode] = useState(false);
  const [lang, setLang] = useState("fa");
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  // Dark mode
  useEffect(() => {
    const saved = localStorage.getItem("darkMode") === "true";
    setDarkMode(saved);
    if (saved) document.documentElement.classList.add("dark");
  }, []);

  const toggleDark = () => {
    const next = !darkMode;
    setDarkMode(next);
    localStorage.setItem("darkMode", String(next));
    document.documentElement.classList.toggle("dark", next);
  };

  // Language
  useEffect(() => {
    const saved = localStorage.getItem("lang") || "fa";
    setLang(saved);
  }, []);

  const changeLang = (code: string) => {
    setLang(code);
    localStorage.setItem("lang", code);
  };

  // Search
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/faculties?search=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-surface-card/95 backdrop-blur-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 shrink-0">
          <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold text-lg">
            ه
          </div>
          <div className="hidden sm:block">
            <div className="font-bold text-foreground text-lg leading-tight">پوهنتون هرات</div>
            <div className="text-xs text-muted">راهنمای هوشمند</div>
          </div>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden lg:flex items-center gap-6">
          {navItems.map((entry) =>
            entry.children ? (
              <DesktopDropdown key={entry.label} entry={entry} />
            ) : (
              <Link
                key={entry.href}
                href={entry.href!}
                className="text-muted hover:text-primary-600 transition-colors font-medium text-sm"
              >
                {entry.label}
              </Link>
            )
          )}
        </nav>

        {/* Right side: Search + Lang + Dark mode + Mobile */}
        <div className="flex items-center gap-2">
          {/* Search */}
          {searchOpen ? (
            <form onSubmit={handleSearch} className="flex items-center gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="جستجو..."
                autoFocus
                className="px-3 py-1.5 rounded-lg border border-border bg-surface text-foreground text-sm w-40 focus:ring-2 focus:ring-primary-500 focus:outline-none"
              />
              <button type="button" onClick={() => setSearchOpen(false)} className="text-muted hover:text-foreground p-1">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </form>
          ) : (
            <button
              onClick={() => setSearchOpen(true)}
              className="p-2 rounded-lg text-muted hover:text-primary-600 hover:bg-primary-50 transition-colors"
              aria-label="جستجو"
            >
              <SearchIcon />
            </button>
          )}

          {/* Language switcher */}
          <div className="hidden sm:flex items-center gap-1 bg-surface rounded-lg p-0.5">
            {languages.map((l) => (
              <button
                key={l.code}
                onClick={() => changeLang(l.code)}
                className={`px-2 py-1 rounded-md text-xs font-medium transition-colors ${
                  lang === l.code ? "bg-primary-600 text-white" : "text-muted hover:text-foreground"
                }`}
              >
                {l.label}
              </button>
            ))}
          </div>

          {/* Dark mode toggle */}
          <button
            onClick={toggleDark}
            className="p-2 rounded-lg text-muted hover:text-primary-600 hover:bg-primary-50 transition-colors"
            aria-label={darkMode ? "حالت روشن" : "حالت تاریک"}
          >
            {darkMode ? <SunIcon /> : <MoonIcon />}
          </button>

          {/* Mobile Toggle */}
          <button
            className="lg:hidden p-2 rounded-lg hover:bg-primary-50 transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="منو"
          >
            <svg className="w-6 h-6 text-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {mobileOpen && (
        <nav className="lg:hidden border-t border-border bg-surface-card px-4 py-2 max-h-[70vh] overflow-y-auto">
          {/* Mobile Search */}
          <form onSubmit={handleSearch} className="mb-3">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="جستجو در سایت..."
                className="flex-1 px-3 py-2 rounded-lg border border-border bg-surface text-foreground text-sm"
              />
              <button type="submit" className="px-3 py-2 bg-primary-600 text-white rounded-lg text-sm">
                <SearchIcon />
              </button>
            </div>
          </form>

          {/* Mobile Language */}
          <div className="flex items-center gap-2 mb-3 pb-3 border-b border-border">
            {languages.map((l) => (
              <button
                key={l.code}
                onClick={() => changeLang(l.code)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  lang === l.code ? "bg-primary-600 text-white" : "bg-surface text-muted"
                }`}
              >
                {l.label}
              </button>
            ))}
            <button onClick={toggleDark} className="ml-auto p-2 rounded-lg hover:bg-surface text-muted">
              {darkMode ? <SunIcon /> : <MoonIcon />}
            </button>
          </div>

          {/* Mobile Nav Items */}
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
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-gold-500 text-white">
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
