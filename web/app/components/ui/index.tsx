"use client";

import { ButtonHTMLAttributes, ReactNode } from "react";

// --- Button ---
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "outline" | "gold" | "ghost";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

export function Button({
  variant = "primary",
  size = "md",
  loading,
  children,
  className = "",
  disabled,
  ...props
}: ButtonProps) {
  const base = "inline-flex items-center justify-center rounded-[10px] font-medium transition-all duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  const sizes = {
    sm: "px-4 py-2 text-sm min-h-[36px]",
    md: "px-6 py-3 text-base min-h-[44px]",
    lg: "px-8 py-4 text-lg min-h-[52px]",
  };
  const variants = {
    primary: "bg-primary-600 text-white hover:bg-primary-700 focus-visible:outline-primary-500 shadow-sm",
    outline: "border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus-visible:outline-primary-500",
    gold: "bg-gold-500 text-white hover:bg-gold-600 focus-visible:outline-gold-400 shadow-sm",
    ghost: "text-primary-600 hover:bg-primary-50 focus-visible:outline-primary-500",
  };

  return (
    <button
      className={`${base} ${sizes[size]} ${variants[variant]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin ml-2 h-4 w-4" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      )}
      {children}
    </button>
  );
}

// --- Card ---
interface CardProps {
  children: ReactNode;
  clickable?: boolean;
  className?: string;
}

export function Card({ children, clickable, className = "" }: CardProps) {
  return (
    <div
      className={`bg-surface-card rounded-[16px] shadow-sm border border-border p-6 transition-all duration-200 ${
        clickable
          ? "hover:shadow-md hover:-translate-y-0.5 cursor-pointer"
          : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}

// --- Badge ---
interface BadgeProps {
  variant?: "success" | "warning" | "danger" | "neutral";
  children: ReactNode;
  className?: string;
}

export function Badge({ variant = "neutral", children, className = "" }: BadgeProps) {
  const variants = {
    success: "bg-success/10 text-success",
    warning: "bg-warning/10 text-warning",
    danger: "bg-danger/10 text-danger",
    neutral: "bg-primary-100 text-primary-700",
  };

  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${variants[variant]} ${className}`}
    >
      {children}
    </span>
  );
}

// --- SectionTitle ---
interface SectionTitleProps {
  title: string;
  subtitle?: string;
  className?: string;
}

export function SectionTitle({ title, subtitle, className = "" }: SectionTitleProps) {
  return (
    <div className={`mb-8 ${className}`}>
      <h2 className="text-2xl md:text-3xl font-bold text-foreground">{title}</h2>
      <div className="mt-3 h-1 w-16 bg-gold-500 rounded-full" />
      {subtitle && (
        <p className="mt-3 text-muted text-lg">{subtitle}</p>
      )}
    </div>
  );
}

// --- LoadingSkeleton ---
export function LoadingSkeleton({ className = "" }: { className?: string }) {
  return (
    <div className={`animate-pulse bg-border rounded-[16px] ${className}`} />
  );
}

// --- EmptyState ---
interface EmptyStateProps {
  icon?: string;
  message: string;
  action?: ReactNode;
}

export function EmptyState({ icon = "📋", message, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <span className="text-4xl mb-4">{icon}</span>
      <p className="text-muted text-lg mb-4">{message}</p>
      {action}
    </div>
  );
}
