// for getting values in .env
import React from "react";
import {
  Box,
  Button,
  DarkMode,
  Divider,
  HStack,
  Text,
  VStack,
} from "@chakra-ui/react";
import { FaComment, FaGithub } from "react-icons/fa";

export default function SocialLogin() {
  const githubParams = {
    client_id: process.env.REACT_APP_GH_CLIENT_ID || "",
    scope: "read:user,user:email",
  };
  const githubProcessedParams = new URLSearchParams(githubParams).toString();
  const kakaoParams = {
    client_id: process.env.REACT_APP_KAKAO_CLIENT_ID || "",
    redirect_uri: "https://sueweetstay.com/social/kakao",
    response_type: "code",
  };
  const kakaoProcessedParams = new URLSearchParams(kakaoParams).toString();
  return (
    <Box mb={4}>
      <HStack my={8}>
        <Divider />
        <Text transform="uppercase" fontSize="xs" as="b">
          Or
        </Text>
        <Divider />
      </HStack>
      <VStack>
        <Button
          w="100%"
          leftIcon={<FaGithub />}
          bg="gray.600"
          _hover={{ bg: "gray.800" }}
          color="white"
          as="a"
          href={`https://github.com/login/oauth/authorize?${githubProcessedParams}`}
        >
          Continue with GitHub
        </Button>
        <DarkMode>
          <Button
            w="100%"
            leftIcon={<FaComment />}
            bg="yellow.300"
            _hover={{ bg: "yellow.400" }}
            color="black"
            as="a"
            href={`https://kauth.kakao.com/oauth/authorize?${kakaoProcessedParams}`}
          >
            Continue with Kakao
          </Button>
        </DarkMode>
      </VStack>
    </Box>
  );
}
