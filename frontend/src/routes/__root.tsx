import { Outlet, createRootRoute } from "@tanstack/react-router";
import { TanStackRouterDevtoolsPanel } from "@tanstack/react-router-devtools";
import { TanStackDevtools } from "@tanstack/react-devtools";
import { createContext, useState } from "react";

import Header from "../components/Header";

// Define the shape of your picture data
type PictureData = {
  id: string;
  filename: string;
  label: string;
  confidence: number;
  imageFile: File; // The actual File object
  feedback_given?: boolean; // Optional flag for feedback status
} | null;

type PictureContextType = {
  pictureData: PictureData;
  setPictureData: (data: PictureData) => void;
};

// Create and export the context
export const PictureContext = createContext<PictureContextType>({
  pictureData: null,
  setPictureData: () => {},
});

function RootComponent() {
  const [pictureData, setPictureData] = useState<PictureData>(null);

  return (
    <PictureContext.Provider value={{ pictureData, setPictureData }}>
      <Header />
      <Outlet />
      <TanStackDevtools
        config={{
          position: "bottom-right",
        }}
        plugins={[
          {
            name: "Tanstack Router",
            render: <TanStackRouterDevtoolsPanel />,
          },
        ]}
      />
    </PictureContext.Provider>
  );
}

export const Route = createRootRoute({
  component: RootComponent,
});
