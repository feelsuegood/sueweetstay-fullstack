import { Heading, Spinner, Text, useToast, VStack } from "@chakra-ui/react";
import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { githubLogIn } from "../api";
import { useMutation, useQueryClient } from "@tanstack/react-query";

// [x] code challenge: refactor using useMutation
export default function GithubConfirm() {
  // get url
  const { search } = useLocation();
  const toast = useToast();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const params = new URLSearchParams(search);
  const code = params.get("code");
  const mutation = useMutation({
    mutationFn: githubLogIn,
    onSuccess: () => {
      toast({
        title: "Welcome",
        description: "successfully logged in",
        status: "success",
        position: "bottom-right",
      });
      // ["me"] is used in headers
      queryClient.refetchQueries({ queryKey: ["me"] });
      navigate("/");
    },
    onError: () => {
      toast({
        title: "Error",
        description: "log in failed",
        status: "error",
        position: "bottom-right",
      });
    },
  });
  const confirmLogin = async () => {
    if (code) {
      mutation.mutate(code);
    }
  };
  useEffect(() => {
    confirmLogin();
  }, []);
  return (
    <VStack justifyContent={"center"} mt={100} spacing={3}>
      <Heading>Processing Log in...</Heading>
      <Text>Please stay 👀</Text>
      <Spinner size={"lg"} />
    </VStack>
  );
}
