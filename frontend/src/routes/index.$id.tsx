import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useContext, useMemo, useEffect, useState } from "react";
import { PictureContext } from "./__root";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/api";

export const Route = createFileRoute("/index/$id")({
  component: RouteComponent,
});

function RouteComponent() {
  const { id } = Route.useParams();
  const navigate = useNavigate();
  const { pictureData, setPictureData } = useContext(PictureContext);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [correctLabel, setCorrectLabel] = useState("");

  // Fetch picture data from API if not in context (e.g., page refresh)
  useEffect(() => {
    if (!pictureData) {
      setLoading(true);
      api
        .get(`/picture/${id}`)
        .then((response) => {
          const data = response.data;
          // Convert base64 image to Blob, then to File
          const byteCharacters = atob(data.image);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const blob = new Blob([byteArray], { type: "image/jpeg" });
          const file = new File([blob], data.filename, { type: "image/jpeg" });

          setPictureData({
            id: data.id,
            filename: data.filename,
            label: data.label,
            confidence: data.confidence,
            imageFile: file,
          });
        })
        .catch((err) => {
          console.error("Failed to fetch picture:", err);
          setError("Failed to load picture data");
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [id, pictureData, setPictureData]);

  const handleCorrectClassification = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.post(`/feedback/${id}`, {
        is_correct: true,
        message: "Classification is correct",
        correct_label: pictureData?.label || "",
      });
      alert("Thank you for confirming!");
      navigate({ to: "/dashboard" });
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to submit feedback");
    } finally {
      setLoading(false);
    }
  };

  const handleIncorrectClassification = () => {
    setShowFeedbackForm(true);
  };

  const handleSubmitFeedback = async () => {
    if (!correctLabel.trim()) {
      setError("Please provide the correct label");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      await api.post(`/feedback/${id}`, {
        is_correct: false,
        message: feedbackMessage || "Classification is incorrect",
        correct_label: correctLabel,
      });
      alert("Thank you for your feedback!");
      navigate({ to: "/dashboard" });
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to submit feedback");
    } finally {
      setLoading(false);
    }
  };

  // Create object URL for the image (memoized to avoid recreating on every render)
  const imageUrl = useMemo(() => {
    return pictureData?.imageFile
      ? URL.createObjectURL(pictureData.imageFile)
      : null;
  }, [pictureData?.imageFile]);

  if (loading && !pictureData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Card>
          <CardHeader>
            <CardTitle>Loading...</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500">Fetching picture data...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error && !pictureData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-500">{error}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!pictureData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Card>
          <CardHeader>
            <CardTitle>No Data Available</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500">Please upload an image first.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen p-4">
      <Card className="max-w-2xl w-full">
        <CardHeader>
          <CardTitle>AI Classification Result</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Display the uploaded image */}
          {imageUrl && (
            <div className="flex justify-center">
              <img
                src={imageUrl}
                alt={pictureData.filename}
                className="max-w-full h-auto rounded-lg shadow-lg max-h-96 object-contain"
              />
            </div>
          )}

          {/* AI Classification Tag */}
          <div className="bg-primary/10 p-4 rounded-lg">
            <h3 className="font-semibold text-lg mb-2">Classification:</h3>
            <p className="text-2xl font-bold text-primary">
              {pictureData.label}
            </p>
          </div>

          {/* Confidence Score */}
          <div className="bg-secondary/10 p-4 rounded-lg">
            <h3 className="font-semibold text-lg mb-2">Confidence Score:</h3>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-200 rounded-full h-4">
                <div
                  className="bg-green-500 h-4 rounded-full transition-all"
                  style={{ width: `${pictureData.confidence * 100}%` }}
                />
              </div>
              <span className="font-bold text-lg">
                {(pictureData.confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>

          {/* Filename */}
          <div className="text-sm text-gray-600">
            <p>
              <strong>Filename:</strong> {pictureData.filename}
            </p>
            <p>
              <strong>ID:</strong> {id}
            </p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Feedback Buttons or Form */}
          {!showFeedbackForm ? (
            <div className="flex gap-2 pt-4">
              <Button
                variant="default"
                className="flex-1 bg-green-600 hover:bg-green-700"
                onClick={handleCorrectClassification}
                disabled={loading}
              >
                ✓ Correct Classification
              </Button>
              <Button
                variant="destructive"
                className="flex-1"
                onClick={handleIncorrectClassification}
                disabled={loading}
              >
                ✗ Incorrect - Submit Feedback
              </Button>
            </div>
          ) : (
            <div className="space-y-4 pt-4 border-t">
              <h3 className="font-semibold text-lg">Submit Correction</h3>

              <div>
                <Label htmlFor="correctLabel">Correct Label *</Label>
                <Input
                  id="correctLabel"
                  value={correctLabel}
                  onChange={(e) => setCorrectLabel(e.target.value)}
                  placeholder="e.g., plastic, cardboard, metal..."
                  className="mt-1"
                />
              </div>

              <div>
                <Label htmlFor="message">Additional Comments (Optional)</Label>
                <Input
                  id="message"
                  value={feedbackMessage}
                  onChange={(e) => setFeedbackMessage(e.target.value)}
                  placeholder="Why was the classification incorrect?"
                  className="mt-1"
                />
              </div>

              <div className="flex gap-2">
                <Button
                  variant="default"
                  onClick={handleSubmitFeedback}
                  disabled={loading || !correctLabel.trim()}
                  className="flex-1"
                >
                  {loading ? "Submitting..." : "Submit Feedback"}
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setShowFeedbackForm(false)}
                  disabled={loading}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
