import {
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Text,
  useToast,
  VStack,
} from "@chakra-ui/react";
import { FaLock, FaUserNinja } from "react-icons/fa";
import SocialLogin from "./SocialLogin";
import { useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  IUsernameLogInError,
  IUsernameLogInSuccess,
  IUsernameLogInVariables,
  usernameLogIn,
} from "../api";

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface IForm {
  username: string;
  password: string;
}

export default function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IForm>();
  const toast = useToast();
  const queryClient = useQueryClient();
  const mutation = useMutation<
    IUsernameLogInSuccess,
    IUsernameLogInError,
    IUsernameLogInVariables
  >({
    mutationFn: usernameLogIn,
    onSuccess: (data) => {
      toast({
        title: "Welcome",
        description: "Logged in successfully",
        status: "success",
        position: "bottom-right",
      });
      onClose();
      queryClient.refetchQueries({ queryKey: ["me"] });
      reset();
    },
    onError: (error) => {},
  });
  const onSubmit = ({ username, password }: IForm) => {
    mutation.mutate({ username, password });
  };
  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Log in</ModalHeader>
        <ModalCloseButton />
        <ModalBody as={"form"} onSubmit={handleSubmit(onSubmit)}>
          <VStack>
            <InputGroup>
              <InputLeftElement children={<FaUserNinja />} />
              <Input
                isInvalid={Boolean(errors.username?.message)}
                required
                {...register("username", {
                  required: "Please enter a username",
                })}
                variant={"filled"}
                placeholder="Username"
              />
            </InputGroup>
            <InputGroup>
              <InputLeftElement children={<FaLock />} />
              <Input
                isInvalid={Boolean(errors.password?.message)}
                required
                {...register("password", {
                  required: "Please enter a password",
                })}
                variant={"filled"}
                placeholder="Password"
                type="password"
              />
            </InputGroup>
          </VStack>
          {mutation.error ? (
            <Text color={"red.500"} textAlign={"center"} fontSize={"sm"}>
              Username or password are wrong
            </Text>
          ) : null}
          <Button
            isLoading={mutation.isPending}
            type="submit"
            mt={4}
            w="100%"
            colorScheme="purple"
          >
            Log in
          </Button>
          <SocialLogin />
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
