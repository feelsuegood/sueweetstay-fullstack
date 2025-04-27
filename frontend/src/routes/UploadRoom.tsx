import {
  Box,
  Button,
  Checkbox,
  Container,
  FormControl,
  FormHelperText,
  FormLabel,
  Grid,
  Heading,
  Input,
  InputGroup,
  InputLeftAddon,
  Select,
  Text,
  Textarea,
  useToast,
  VStack,
} from "@chakra-ui/react";
import HostOnlyPage from "../components/HostOnlyPage";
import ProtectedPage from "../components/ProtectedPage";
import { FaBed, FaDollarSign, FaToilet } from "react-icons/fa";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  getAmenities,
  getRoomCategories,
  IUploadRoomVariables,
  uploadRoom,
} from "../api";
import { IAmenity, ICategory, IRoomIdDetail } from "../types";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

export default function UploadRoom() {
  const toast = useToast();
  const navigate = useNavigate();
  // use for checking value before submit
  // const { register, watch, handleSubmit } = useForm<IUploadRoomVariables>();
  const { register, handleSubmit } = useForm<IUploadRoomVariables>();
  const mutation = useMutation({
    mutationFn: uploadRoom,
    onSuccess: (data: IRoomIdDetail) => {
      toast({
        title: "Room uploaded 🥳",
        status: "success",
        position: "bottom-right",
      });
      // * when user upload a room, django response.data has id not pk
      // console.log(data);
      navigate(`/rooms/${data.id}`);
    },
  });
  const { isLoading: isAmenitesLoading, data: amenities } = useQuery<
    IAmenity[]
  >({
    queryKey: ["amenities"],
    queryFn: getAmenities,
  });
  const { isLoading: roomCategoriesIsLoding, data: roomCategories } = useQuery<
    ICategory[]
  >({
    queryKey: ["categories/rooms"],
    queryFn: getRoomCategories,
  });
  // console.log(watch());
  const onSubmit = (data: IUploadRoomVariables) => {
    // ! don't forget
    mutation.mutate(data);
  };
  return (
    <ProtectedPage>
      <HostOnlyPage>
        <Box pb={40} mt={10} px={{ base: 10, lg: 40 }}>
          <Container>
            <Heading textAlign={"center"}>Upload Room</Heading>
            <VStack
              spacing={5}
              as={"form"}
              onSubmit={handleSubmit(onSubmit)}
              mt={5}
            >
              <FormControl>
                <FormLabel>Name</FormLabel>
                <Input
                  {...register("name", { required: true })}
                  required
                  type="text"
                />
                <FormHelperText>Writhe the name of your room</FormHelperText>
              </FormControl>
              <FormControl>
                <FormLabel>County</FormLabel>
                <Input
                  {...register("country", { required: true })}
                  required
                  type="text"
                />
              </FormControl>
              <FormControl>
                <FormLabel>City</FormLabel>
                <Input
                  {...register("city", { required: true })}
                  required
                  type="text"
                />
              </FormControl>
              <FormControl>
                <FormLabel>Address</FormLabel>
                <Input
                  {...register("address", { required: true })}
                  required
                  type="text"
                />
              </FormControl>
              <FormControl>
                <FormLabel>Price</FormLabel>
                <InputGroup>
                  <InputLeftAddon children={<FaDollarSign />} />
                  <Input
                    {...register("price", { required: true })}
                    required
                    type="number"
                    min={0}
                  />
                </InputGroup>
              </FormControl>
              <FormControl>
                <FormLabel>Rooms</FormLabel>
                <InputGroup>
                  <InputLeftAddon children={<FaBed />} />
                  <Input
                    {...register("rooms", { required: true })}
                    required
                    type="number"
                    min={0}
                  />
                </InputGroup>
              </FormControl>
              <FormControl>
                <FormLabel>Toilets</FormLabel>
                <InputGroup>
                  <InputLeftAddon children={<FaToilet />} />
                  <Input
                    {...register("toilets", { required: true })}
                    required
                    type="number"
                    min={0}
                  />
                </InputGroup>
              </FormControl>
              <FormControl>
                <FormLabel>Description</FormLabel>
                <Textarea {...register("description", { required: true })} />
              </FormControl>
              <FormControl>
                <Checkbox {...register("pet_friendly")}>Pet friendly?</Checkbox>
              </FormControl>
              <FormControl>
                <FormLabel>Kind</FormLabel>
                <Select
                  {...register("kind", { required: true })}
                  placeholder="Choose a kind"
                >
                  <option value="entire_place">Entire Place</option>
                  <option value="private_room">Private Room</option>
                  <option value="shared_room">Shared Room</option>
                </Select>
                <FormHelperText>
                  What kind of room are you renting?
                </FormHelperText>
              </FormControl>
              <FormControl>
                <FormLabel>Category</FormLabel>
                <Select
                  {...register("category", { required: true })}
                  placeholder="Choose a category"
                >
                  {roomCategories?.map((roomCategory) => (
                    <option key={roomCategory.pk} value={roomCategory.pk}>
                      {roomCategory.name}
                    </option>
                  ))}
                </Select>
                <FormHelperText>
                  What category descreibs your room?
                </FormHelperText>
              </FormControl>
              <FormControl>
                <FormLabel>Amenities</FormLabel>
                <Grid templateColumns={"1fr 1fr"}>
                  {amenities?.map((amenity) => (
                    <Box key={amenity.pk}>
                      <Checkbox
                        value={amenity.pk}
                        {...register("amenities", { required: true })}
                      >
                        {amenity.name}
                      </Checkbox>
                      <FormHelperText ml={5} mt={1}>
                        {amenity.description}
                      </FormHelperText>
                    </Box>
                  ))}
                </Grid>
              </FormControl>
              {mutation.isError ? (
                <Text color={"red.500"}>Something went wrong</Text>
              ) : null}
              <Button
                type="submit"
                isLoading={mutation.isPending}
                colorScheme="purple"
                size={"lg"}
                width={"100%"}
              >
                Upload a Room
              </Button>
            </VStack>
          </Container>
        </Box>
      </HostOnlyPage>
    </ProtectedPage>
  );
}
