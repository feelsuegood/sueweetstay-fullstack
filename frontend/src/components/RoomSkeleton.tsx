import { Box, HStack, Skeleton, SkeletonText } from "@chakra-ui/react";

export default function RoomSkeleton() {
  return (
    <Box>
      <Skeleton rounded={"2xl"} height={240} mb={7} />
      <HStack justifyContent={"space-between"}>
        <SkeletonText w={"50%"} noOfLines={2} mb={6} />
        <SkeletonText w={"15%"} noOfLines={1} mb={10} mr={2} />
      </HStack>
      <SkeletonText w={"20%"} noOfLines={1} />
    </Box>
  );
}
