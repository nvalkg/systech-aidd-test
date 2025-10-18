import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { format, formatDistanceToNow } from "date-fns";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format a number with thousand separators
 * @example formatNumber(1234.56) => "1,234.56"
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 1,
  }).format(value);
}

/**
 * Format a date string to readable format
 * @example formatDate("2025-10-17T14:30:00Z") => "Oct 17, 2025"
 */
export function formatDate(dateString: string): string {
  return format(new Date(dateString), "MMM d, yyyy");
}

/**
 * Format a date string to relative time
 * @example formatRelativeTime("2025-10-17T14:30:00Z") => "2 hours ago"
 */
export function formatRelativeTime(dateString: string): string {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true });
}
