import { Box } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
// ^ no need to console.log()
import Header from "./Header";

export default function Root() {
  return (
    <Box>
      <Header />
      <Outlet />
      <ReactQueryDevtools />
    </Box>
  );
}
