import { Link } from "@tanstack/react-router";

import { Leaf } from "lucide-react";

export default function Header() {
  return (
    <>
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-[#2E2E2E] backdrop-blur supports-backdrop-filter:bg-[#2E2E2E]/95">
        <div className="container flex h-16 items-center justify-between px-4">
          <Link
            to="/"
            className="flex items-center gap-2 text-xl font-bold text-foreground hover:text-primary transition-colors"
          >
            <Leaf className="h-6 w-6 text-primary" />
            <span>GreenBin</span>
          </Link>
          <nav className="flex items-center justify-center gap-6">
            <Link
              to="/"
              className={
                "text-sm font-medium transition-colors text-foreground hover:text-primary"
              }
              activeProps={{
                style: {
                  color: "var(--primary)",
                },
              }}
            >
              AI scanner
            </Link>
            <Link
              to="/dashboard"
              className={
                "text-sm font-medium transition-colors text-foreground hover:text-primary"
              }
              activeProps={{
                style: {
                  color: "var(--primary)",
                },
              }}
            >
              Dashboard
            </Link>
          </nav>
        </div>
      </header>
    </>
  );
}
