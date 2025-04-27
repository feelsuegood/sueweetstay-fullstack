import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Textarea,
  useToast,
  VStack,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { useParams } from "react-router-dom";
import HostOnlyPage from "../components/HostOnlyPage";
import ProtectedPage from "../components/ProtectedPage";
import { useMutation } from "@tanstack/react-query";
import { getuploadURL, uploadImage, uploadRoomPhoto } from "../api";

interface IForm {
  file: FileList;
  description: string;
}

interface IUploadURLResponsse {
  id: string;
  uploadURL: string;
}

export default function UploadPhotos() {
  const { roomPk } = useParams();
  const toast = useToast();
  const { register, watch, handleSubmit, reset } = useForm<IForm>();
  const uploadRoomPhotoMutation = useMutation({
    mutationFn: uploadRoomPhoto,
    onSuccess: (data: any) => {
      // console.log(data);
      toast({
        status: "success",
        title: "Photo uploaded successfully",
        description: "feel free to upload more photos",
        isClosable: true,
      });
      reset();
    },
  });
  //   when get variables in mutation, it should be one object
  const uploadImageMutation = useMutation({
    mutationFn: uploadImage,
    onSuccess: ({ result }: any) => {
      // console.log(result);
      if (roomPk) {
        uploadRoomPhotoMutation.mutate({
          description:
            watch("description") === ""
              ? "no description"
              : watch("description"),
          file: `https://imagedelivery.net/8wupMKx7lfJzP_Fr3VkPUA/${result.id}/public`,
          roomPk,
        });
      }
    },
  });
  const uploadURLMutation = useMutation({
    mutationFn: getuploadURL,
    onSuccess: (data: IUploadURLResponsse) => {
      uploadImageMutation.mutate({
        uploadURL: data.uploadURL,
        // * oh..
        file: watch("file"),
      });
    },
  });
  const onSubmit = () => {
    uploadURLMutation.mutate();
  };
  return (
    <ProtectedPage>
      <HostOnlyPage>
        <Box
          pb={40}
          mt={10}
          px={{
            base: 10,
            lg: 40,
          }}
        >
          <Container>
            <Heading textAlign={"center"}>Upload a Photo</Heading>
            <VStack
              spacing={5}
              mt={10}
              as={"form"}
              onSubmit={handleSubmit(onSubmit)}
            >
              <FormControl>
                <Input {...register("file")} type="file" accept="image/*" />
              </FormControl>
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Textarea {...register("description")} />
              </FormControl>
              <Button
                isLoading={
                  uploadRoomPhotoMutation.isPending ||
                  uploadImageMutation.isPending ||
                  uploadURLMutation.isPending
                }
                w="full"
                colorScheme={"purple"}
                type="submit"
              >
                Upload photos
              </Button>
            </VStack>
          </Container>
        </Box>
      </HostOnlyPage>
    </ProtectedPage>
  );
}
