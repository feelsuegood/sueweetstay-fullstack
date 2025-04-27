import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import {
  checkBooking,
  checkBookingQueryKey,
  getRoom,
  getRoomReviews,
} from "../api";
import { IRoomDetail, IReview } from "../types";
import {
  Avatar,
  Box,
  Button,
  Container,
  Grid,
  GridItem,
  Heading,
  HStack,
  Image,
  Skeleton,
  Text,
  VStack,
} from "@chakra-ui/react";
import { FaStar } from "react-icons/fa";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../styles/Calendar.css";
import { useState } from "react";
import { Helmet } from "react-helmet";

type ValuePiece = Date | null;

type Value = ValuePiece | [ValuePiece, ValuePiece];
// type Value = [ValuePiece, ValuePiece];

export default function RoomDetail() {
  const { roomPk } = useParams();
  const { isLoading, data } = useQuery<IRoomDetail>({
    queryKey: [`room`, roomPk],
    queryFn: getRoom,
  });
  const { isLoading: isReviewsLoading, data: reviewsData } = useQuery<
    IReview[]
  >({
    queryKey: ["room", roomPk, "reviews"],
    queryFn: getRoomReviews,
  });
  const [dates, setDates] = useState<Value>();
  const { isLoading: IsCheckingBooking, data: checkBookingData } = useQuery({
    queryKey: ["check", roomPk, dates] as checkBookingQueryKey,
    queryFn: checkBooking,
    enabled: dates !== undefined,
    gcTime: 0,
  });
  // console.log(checkBookingData, IsCheckingBooking);

  return (
    <Box
      mt={10}
      py={5}
      px={{
        base: 10,
        lg: 40,
      }}
    >
      <Helmet>
        <title>{data ? data.name : "Loading..."}</title>
      </Helmet>
      <Skeleton height={"43px"} w="25%" isLoaded={!isLoading}>
        <Heading w="500px">{data?.name}</Heading>
      </Skeleton>
      <Grid
        overflow={"hidden"}
        rounded="xl"
        mt={8}
        gap={3}
        h={"60vh"}
        templateRows={"1fr 1fr"}
        templateColumns={"repeat(4,1fr)"}
      >
        {[0, 1, 2, 3, 4].map((index) => (
          <GridItem
            colSpan={index === 0 ? 2 : 1}
            rowSpan={index === 0 ? 2 : 1}
            overflow={"hidden"}
            key={index}
          >
            <Skeleton isLoaded={!isLoading} h="100%" w="100%">
              {data?.photos && data.photos.length > 0 ? (
                <Image
                  objectFit={"cover"}
                  w={"100%"}
                  h={"100%"}
                  src={data?.photos[index]?.file}
                />
              ) : null}
            </Skeleton>
          </GridItem>
        ))}
      </Grid>
      <Grid gap={20} templateColumns={"2fr 1fr"} maxW="container.xl">
        <Box>
          <HStack mt={10} justifyContent={"space-between"}>
            <VStack alignItems={"flex-start"}>
              <Skeleton isLoaded={!isLoading} h={"30px"}>
                <Heading fontSize={"2xl"}>
                  House hoseted by {data?.owner.name}
                </Heading>
              </Skeleton>
              <Skeleton isLoaded={!isLoading} h={"30px"}>
                <HStack justifyContent={"flex-start"} w={"100%"}>
                  <Text>
                    {data?.rooms} room
                    {data?.rooms === 1 || reviewsData?.length === 0 ? "" : "s"}
                  </Text>
                  <Text>•</Text>
                  <Text>
                    {data?.toilets} toilet
                    {data?.toilets === 1 || reviewsData?.length === 0
                      ? ""
                      : "s"}
                  </Text>
                </HStack>
              </Skeleton>
            </VStack>
            <Avatar
              name={data?.owner.name}
              size={"xl"}
              src={data?.owner.avatar}
            />
          </HStack>
          <Box mt={10}>
            <Heading fontSize={"2xl"} mb={5}>
              <Skeleton h={"35px"} isLoaded={!isReviewsLoading && !isLoading}>
                <HStack>
                  <FaStar /> <Text>{data?.rating}</Text>
                  <Text>•</Text>
                  <Text>
                    {reviewsData?.length} review
                    {reviewsData?.length === 1 || reviewsData?.length === 0
                      ? ""
                      : "s"}
                  </Text>
                </HStack>
              </Skeleton>
            </Heading>
            <Container mt={15} maxW={"container.lg"} marginX={"none"}>
              <Grid gap={10} templateColumns={"1fr 1fr"}>
                {reviewsData?.map((review, index) => (
                  <VStack alignItems={"flex-start"} key={index}>
                    <Skeleton h={50} isLoaded={!isReviewsLoading && !isLoading}>
                      <HStack>
                        <Avatar
                          name={review.user.name}
                          src={review.user.avatar}
                          size={"md"}
                        />
                        <VStack spacing={0} alignItems={"flex-start"}>
                          <Heading fontSize={"md"}>{review.user.name}</Heading>
                          <HStack spacing={1}>
                            <FaStar size={"12px"} />
                            <Text>{review.rating}</Text>
                          </HStack>
                        </VStack>
                      </HStack>
                    </Skeleton>
                    <Skeleton
                      w={"70%"}
                      h={30}
                      isLoaded={!isReviewsLoading && !isLoading}
                    >
                      <Text>{review.payload}</Text>
                    </Skeleton>
                  </VStack>
                ))}
              </Grid>
            </Container>
          </Box>
        </Box>
        <Box pt={10} borderRadius="md">
          <Calendar
            onChange={setDates}
            prev2Label={null}
            next2Label={null}
            minDetail={"month"}
            minDate={new Date()}
            maxDate={new Date(Date.now() + 60 * 60 * 24 * 7 * 4 * 6 * 1000)}
            selectRange
            className="custom-calendar"
          />
          <Button
            disabled={!checkBookingData?.ok}
            isLoading={IsCheckingBooking}
            my={5}
            w={"100%"}
            colorScheme="purple"
          >
            Make booking
          </Button>
          {!IsCheckingBooking && !checkBookingData?.ok ? (
            <Text color={"red.800"} fontWeight={"bold"}>
              Can't book those dates 😢
            </Text>
          ) : null}
        </Box>
      </Grid>
    </Box>
  );
}
