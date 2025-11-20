import { createFileRoute } from "@tanstack/react-router";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import api from "@/api";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null);
    const f = e.target.files?.[0] ?? null;

    if (!f) {
      setFile(null);
      return;
    }

    setFile(f);
  };

  const handleClear = async () => {
    if (!file) return;

    try {
      const form = new FormData();
      form.append("file", file);

      const { data } = await api.post<{
        filename: string;
        label: string;
        confidence: number;
      }>("/picture", form);

      console.table(data);
      setFile(null);
      setError(null);
    } catch (err: any) {
      console.error(err);
      if (err?.response?.data?.message) {
        setError(String(err.response.data.message));
      } else if (err?.response) {
        setError(
          `Server error: ${err.response.status} ${err.response.statusText}`
        );
      } else {
        setError(err?.message ?? "Upload failed");
      }
    }
  };

  return (
    <div className="flex-1 justify-center items-center h-screen flex">
      <Card>
        <CardHeader>
          <CardTitle>Upload file to scan</CardTitle>
        </CardHeader>
        <CardContent className="gap-2">
          <Label className="p-2" htmlFor="file">
            Upload picture
          </Label>
          <Input
            className="bg-border"
            type="file"
            id="file"
            placeholder=""
            accept=".jpg,.jpeg,image/jpeg,.png"
            onChange={handleChange}
          />
          <Button
            onClick={handleClear}
            disabled={!file}
            className="mt-2 text-sm text-white"
          >
            Scan Trash
          </Button>
          {error && <p className="text-red-500 mt-2">{error}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
