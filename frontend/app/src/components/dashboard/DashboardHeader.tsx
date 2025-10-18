import { Github } from "lucide-react";
import { Button } from "@/components/ui/button";

export function DashboardHeader() {
  return (
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Statistics and analytics for AI dialogue system
        </p>
      </div>
      <Button variant="outline" size="sm" asChild>
        <a
          href="https://github.com/your-repo/aidd"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Github className="mr-2 h-4 w-4" />
          GitHub
        </a>
      </Button>
    </div>
  );
}
