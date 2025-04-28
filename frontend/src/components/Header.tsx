import {
  Avatar,
  Box,
  Button,
  HStack,
  IconButton,
  LightMode,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  ToastId,
  useColorMode,
  useColorModeValue,
  useDisclosure,
  useToast,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignUpModal from "./SignUpModal";
import useUser from "../lib/useUser";
import { logOut } from "../api";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FaMoon, FaSun } from "react-icons/fa";
import { LuCandy } from "react-icons/lu";
import { useEffect, useRef } from "react";

export default function Header() {
  // getMe -> useUser -> Header
  const { isUserLoading, user, isLoggedIn } = useUser();
  const {
    isOpen: isLoginOpen,
    onClose: onLoginClose,
    onOpen: onLoginOpen,
  } = useDisclosure();
  const {
    isOpen: isSignUpOpen,
    onClose: onSignUpClose,
    onOpen: onSignUpOpen,
  } = useDisclosure();
  const { toggleColorMode } = useColorMode();
  const logoColor = useColorModeValue("purple.300", "purple:300");
  const Icon = useColorModeValue(FaMoon, FaSun);
  const toast = useToast();
  // for automatically refetching, absolute bosss
  const queryClient = useQueryClient();
  const toastId = useRef<ToastId>();
  const mutation = useMutation({
    mutationFn: logOut,
    onMutate: () => {
      toastId.current = toast({
        title: "Logging out...",
        description: "Sad to see you go 😭",
        status: "loading",
        position: "bottom-right",
      });
    },
    onSuccess: () => {
      queryClient.refetchQueries({ queryKey: ["me"] });
      if (toastId.current) {
        toast.update(toastId.current, {
          title: "See you 👋",
          description: "Logged out successfully",
          status: "success",
        });
      }
    },
  });
  const onLogOut = async () => {
    mutation.mutate();
  };
  useEffect(() => {
    const hasVisited = sessionStorage.getItem("hasVisited");
    if (!hasVisited) {
      toast({
        status: "info",
        title: "Welcome to My Practice Project",
        description:
          "This website is part of my personal portfolio and is for educational and non-commercial purposes only.",
        isClosable: true,
        duration: 20000,
        position: "top",
      });
    }
    sessionStorage.setItem("hasVisited", "true");
  }, []);

  return (
    <HStack
      justifyContent={"space-between"}
      alignItems={"center"}
      mx={10}
      py={5}
      px={{
        sm: 4,
        md: 40,
      }}
      spacing={{
        sm: 4,
        md: 0,
      }}
      direction={{
        sm: "column",
        md: "row",
      }}
      borderBottomWidth={1}
    >
      <Box color={logoColor}>
        <Link to={"/"}>
          <LuCandy size={"48"} />
        </Link>
      </Box>
      <HStack spacing={2}>
        <IconButton
          onClick={toggleColorMode}
          variant={"ghost"}
          aria-label="Toggle dark mode"
          icon={<Icon />}
        />
        {/* different ui for a login user and unloggedin user */}
        {!isUserLoading ? (
          !isLoggedIn ? (
            <>
              <Button onClick={onLoginOpen}>Log in</Button>
              <LightMode>
                <Button onClick={onSignUpOpen} colorScheme={"purple"}>
                  Sign up
                </Button>
              </LightMode>
            </>
          ) : (
            <Menu>
              <MenuButton>
                <Avatar size={"md"} name={user?.name} src={user?.avatar} />
              </MenuButton>
              <MenuList>
                {user?.is_host ? (
                  <Link to="/rooms/upload">
                    <MenuItem>Upload room</MenuItem>
                  </Link>
                ) : null}
                <MenuItem onClick={onLogOut}>Log out</MenuItem>
              </MenuList>
            </Menu>
          )
        ) : null}
      </HStack>
      <LoginModal isOpen={isLoginOpen} onClose={onLoginClose} />
      <SignUpModal isOpen={isSignUpOpen} onClose={onSignUpClose} />
    </HStack>
  );
}
