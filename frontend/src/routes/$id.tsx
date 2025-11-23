import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useContext, useMemo, useEffect, useState } from "react";
import { PictureContext } from "./__root";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import api from "@/api";

export const Route = createFileRoute("/$id")({
  component: RouteComponent,
});

function RouteComponent() {
  const { id } = Route.useParams();
  const { pictureData, setPictureData } = useContext(PictureContext);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [correctLabel, setCorrectLabel] = useState("");

  // Fetch picture data from API if not in context
  useEffect(() => {
    const fetchPicture = async () => {
      // If we already have the data, no need to fetch
      if (pictureData && pictureData.id === id) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response = await api.get(`/picture/${id}`);
        const data = response.data;

        // Convert base64 image to File object
        const binaryString = atob(data.image);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        const blob = new Blob([bytes], { type: "image/jpeg" });
        const file = new File([blob], data.filename, { type: "image/jpeg" });

        setPictureData({
          id: data.id,
          filename: data.filename,
          label: data.label,
          confidence: data.confidence,
          imageFile: file,
          feedback_given: data.feedback_given,
        });
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load picture");
      } finally {
        setLoading(false);
      }
    };

    fetchPicture();
  }, [id, pictureData, setPictureData]);

  const imageUrl = useMemo(() => {
    return pictureData?.imageFile
      ? URL.createObjectURL(pictureData.imageFile)
      : null;
  }, [pictureData?.imageFile]);

  const handleCorrectClassification = async () => {
    try {
      await api.post(`/feedback/${id}`, {
        is_correct: true,
        message: "Classification is correct",
        correct_label: pictureData?.label,
      });
      navigate({ to: "/dashboard" });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to submit feedback");
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

    try {
      await api.post(`/feedback/${id}`, {
        is_correct: false,
        message: feedbackMessage || "Classification is incorrect",
        correct_label: correctLabel,
      });
      navigate({ to: "/dashboard" });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to submit feedback");
    }
  };

  if (loading) {
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

  if (!pictureData) {
    return (
      <div className="flex items-center justify-center h-screen">
        <Card>
          <CardHeader>
            <CardTitle>No Data Available</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500">
              {error || "Please upload an image first."}
            </p>
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
          can't access property "length", stats.feedback_by_date is undefined
          {/* Filename */}
          <div className="text-sm text-white">
            <p>
              <strong>Filename:</strong> {pictureData.filename}
            </p>
          </div>
          {/* Error Display */}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          {/* Feedback Buttons or Form */}
          {pictureData.feedback_given ? (
            <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded">
              <p className="font-semibold">
                ✓ Feedback already submitted for this image
              </p>
              <p className="text-sm mt-1">Thank you for your contribution!</p>
            </div>
          ) : !showFeedbackForm ? (
            <div className="flex gap-2 pt-4">
              <Button
                variant="outline"
                className="flex-1"
                onClick={handleCorrectClassification}
              >
                Correct Classification
              </Button>
              <Button
                variant="outline"
                className="flex-1"
                onClick={handleIncorrectClassification}
              >
                Incorrect - Submit Feedback
              </Button>
            </div>
          ) : (
            <div className="space-y-4 pt-4">
              <div>
                <Label htmlFor="correctLabel">Correct Label *</Label>
                <Input
                  id="correctLabel"
                  value={correctLabel}
                  onChange={(e) => setCorrectLabel(e.target.value)}
                  placeholder="Enter the correct classification"
                />
              </div>
              <div>
                <Label htmlFor="feedbackMessage">
                  Additional Message (Optional)
                </Label>
                <Textarea
                  id="feedbackMessage"
                  value={feedbackMessage}
                  onChange={(e) => setFeedbackMessage(e.target.value)}
                  placeholder="Provide additional details about why the classification is incorrect..."
                  rows={3}
                />
              </div>
              <div className="flex gap-2">
                <Button
                  onClick={handleSubmitFeedback}
                  className="flex-1"
                  disabled={!correctLabel.trim()}
                >
                  Submit Feedback
                </Button>
                <Button
                  variant="outline"
                  onClick={() => setShowFeedbackForm(false)}
                  className="flex-1"
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
