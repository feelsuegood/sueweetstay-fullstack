import {
  AspectRatio,
  Box,
  Button,
  Grid,
  HStack,
  Image,
  Text,
  useColorModeValue,
  VStack,
} from "@chakra-ui/react";
import { FaCamera, FaRegHeart, FaStar } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";

interface IRoomProps {
  pk: number;
  imageUrl: string;
  name: string;
  rating: number;
  city: string;
  country: string;
  price: number;
  isOwner: boolean;
}

export default function Room({
  pk,
  imageUrl,
  name,
  rating,
  city,
  country,
  price,
  isOwner,
}: IRoomProps) {
  const gray = useColorModeValue("gray.600", "gray.300");
  const navigate = useNavigate();
  // upload room photos for owner
  // * prevent entire link boundaries
  const onCameraClick = (event: React.SyntheticEvent<HTMLButtonElement>) => {
    event.preventDefault();
    navigate(`/rooms/${pk}/photos`);
  };
  return (
    <Link to={`/rooms/${pk}`}>
      <VStack alignItems={"flex-start"}>
        <AspectRatio ratio={4 / 3} w="100%">
          <Box
            backgroundColor={"gray.300"}
            position={"relative"}
            overflow={"hidden"}
            mb={3}
            rounded={"2xl"}
          >
            <Image minH={"240"} objectFit={"cover"} src={imageUrl} />
            <Button
              variant={"unstyled"}
              cursor={"pointer"}
              position={"absolute"}
              top={0}
              right={0}
              color={"white"}
              onClick={onCameraClick}
            >
              {isOwner ? <FaCamera size={20} /> : <FaRegHeart size={20} />}
            </Button>
          </Box>
        </AspectRatio>
        <Box>
          <Grid gap={2} templateColumns={"6fr 1fr"}>
            <Text display={"block"} as={"b"} noOfLines={1} fontSize={"medium"}>
              {name}
            </Text>
            <HStack spacing={1}>
              <FaStar size={15} />
              <Text>{rating}</Text>
            </HStack>
          </Grid>
          <Text fontSize={"smaller"} color={gray}>
            {city}, {country}
          </Text>
        </Box>
        <Text fontSize={"small"} color={gray} textDecoration={"underline"}>
          <Text as={"b"}>${price}</Text> Total
        </Text>
      </VStack>
    </Link>
  );
}
