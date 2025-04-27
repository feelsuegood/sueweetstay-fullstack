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
import { FaEnvelope, FaLock, FaUserNinja, FaUserSecret } from "react-icons/fa";
import SocialLogin from "./SocialLogin";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { ISignUpError, ISignUpSuccess, ISignUpVariables, signUp } from "../api";

// [x] code challenge: complete using useMutation

interface SignUpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

interface IForm {
  name: string;
  email: string;
  username: string;
  password: string;
}

export default function SignUpModal({ isOpen, onClose }: SignUpModalProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<IForm>();
  const toast = useToast();
  const queryClient = useQueryClient();
  const mutation = useMutation<ISignUpSuccess, ISignUpError, ISignUpVariables>({
    mutationFn: signUp,
    onSuccess: (data) => {
      // console.log(data);
      toast({
        title: "Welcome 🥳",
        description: "Signed up successfully",
        status: "success",
        position: "bottom-right",
      });
      // close modal
      onClose();
      // refetch user data
      queryClient.refetchQueries({ queryKey: ["me"] });
      // reset sign up input
      reset();
    },
    onError: (error) => {
      console.log(error);
    },
  });
  // const onSubmit = ({ name, email, username, password }: IForm) => {
  //   mutation.mutate({ name, email, username, password });
  // };
  const onSubmit = (data: IForm) => {
    mutation.mutate(data);
  };

  return (
    <Modal onClose={onClose} isOpen={isOpen}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Sign up</ModalHeader>
        <ModalCloseButton />
        <ModalBody as={"form"} onSubmit={handleSubmit(onSubmit)}>
          <VStack>
            <InputGroup>
              <InputLeftElement children={<FaUserSecret />} />
              <Input
                isInvalid={Boolean(errors.name?.message)}
                required
                {...register("name", {
                  required: "Please enter a name",
                })}
                variant={"filled"}
                placeholder="Name"
              />
            </InputGroup>
            <InputGroup>
              <InputLeftElement children={<FaEnvelope />} />
              <Input
                isInvalid={Boolean(errors.email?.message)}
                required
                {...register("email", {
                  required: "Please enter a email",
                })}
                variant={"filled"}
                placeholder="Email"
              />
            </InputGroup>
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
            <Text color={".500"} textAlign={"center"} fontSize={"sm"}>
              Please enter valid inputs
            </Text>
          ) : null}
          <Button
            isLoading={mutation.isPending}
            type="submit"
            mt={4}
            w="100%"
            colorScheme="purple"
          >
            Sign up
          </Button>
          <SocialLogin />
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}
