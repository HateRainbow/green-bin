import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import api from "@/api";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
} from "@/components/ui/chart";

export const Route = createFileRoute("/dashboard")({
  component: DashboardComponent,
});

type FeedbackData = {
  date: string;
  correct: number;
  incorrect: number;
};

type DashboardStats = {
  total_pictures: number;
  total_feedback: number;
  feedback_by_date: FeedbackData[];
};

const chartConfig = {
  correct: {
    label: "Correct",
    color: "hsl(var(--chart-1))",
  },
  incorrect: {
    label: "Incorrect",
    color: "hsl(var(--chart-2))",
  },
} satisfies ChartConfig;

function DashboardComponent() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await api.get("/dashboard");
        const data = response.data;
        console.log("Dashboard data:", data); // Debug log
        // Ensure feedback_by_date is always an array
        setStats({
          ...data,
          feedback_by_date: data.feedback_by_date || [],
        });
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card>
          <CardHeader>
            <CardTitle>Loading Dashboard...</CardTitle>
          </CardHeader>
        </Card>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-500">{error || "Failed to load data"}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Total Pictures</CardTitle>
            <CardDescription>Images uploaded and classified</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{stats.total_pictures}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Total Feedback</CardTitle>
            <CardDescription>User feedback received</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{stats.total_feedback}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Accuracy</CardTitle>
            <CardDescription>AI classification accuracy</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">
              {stats.total_feedback > 0 && stats.feedback_by_date
                ? (
                    (stats.feedback_by_date.reduce(
                      (acc, day) => acc + day.correct,
                      0
                    ) /
                      stats.total_feedback) *
                    100
                  ).toFixed(1)
                : 0}
              %
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Feedback Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Feedback Over Time</CardTitle>
          <CardDescription>
            Daily feedback showing correct vs incorrect classifications
          </CardDescription>
        </CardHeader>
        <CardContent>
          {stats.feedback_by_date && stats.feedback_by_date.length > 0 ? (
            <ChartContainer config={chartConfig}>
              <BarChart
                data={stats.feedback_by_date}
                margin={{
                  left: 12,
                  right: 12,
                  top: 12,
                  bottom: 12,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis
                  dataKey="date"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tickFormatter={(value) => {
                    const date = new Date(value);
                    return date.toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                    });
                  }}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  allowDecimals={false}
                />
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent />}
                />
                <ChartLegend content={<ChartLegendContent />} />
                <Bar
                  dataKey="correct"
                  fill="var(--color-correct)"
                  radius={[4, 4, 0, 0]}
                />
                <Bar
                  dataKey="incorrect"
                  fill="var(--color-incorrect)"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ChartContainer>
          ) : (
            <div className="flex items-center justify-center h-64">
              <p className="text-gray-500">No feedback data available yet</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
