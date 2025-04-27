// eslint-disable-next-line @typescript-eslint/no-unused-vars
import Cookie from "js-cookie";
import { QueryFunctionContext } from "@tanstack/react-query";
import axios from "axios";
import { formatDate } from "./lib/utils";

const instance = axios.create({
  baseURL:
    process.env.NODE_ENV === "development"
      ? "http://127.0.0.1:8000/api/v1/"
      : "https://backend.sueweetstay.com/api/v1/",
  // add cookies
  withCredentials: true,
});

export const getRooms = () => {
  return instance.get("rooms/").then((response) => response.data);
};

export const getRoom = ({ queryKey }: QueryFunctionContext) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, roomPk] = queryKey;
  return instance.get(`rooms/${roomPk}`).then((response) => response.data);
  // * return instance.get(`rooms/${queryKey[1]}`).then((response) => response.data);
};

export const getRoomReviews = ({ queryKey }: QueryFunctionContext) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, roomPk] = queryKey;
  return instance
    .get(`rooms/${roomPk}/reviews`)
    .then((response) => response.data);
  // * return instance.get(`rooms/${queryKey[1]}`).then((response) => response.data);
};

export const getMe = () => {
  return instance.get(`users/me`).then((response) => response.data);
};

export const logOut = () => {
  return instance
    .post("users/log-out", null, {
      headers: {
        "X-CSRFToken": Cookie.get("csrftoken") || "",
      },
    })
    .then((response) => response.data);
};

export const githubLogIn = (code: string) => {
  return instance
    .post(
      "users/github",
      { code },
      {
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken") || "",
        },
      },
    )
    .then((response) => response.status);
};

export const kakaoLogIn = (code: string) => {
  return instance
    .post(
      "users/kakao",
      { code },
      {
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken") || "",
        },
      },
    )
    .then((response) => response.status);
};

export interface IUsernameLogInVariables {
  username: string;
  password: string;
}

export interface IUsernameLogInSuccess {
  ok: string;
}
export interface IUsernameLogInError {
  error: string;
}
export const usernameLogIn = ({
  username,
  password,
}: IUsernameLogInVariables) => {
  return instance
    .post(
      "users/log-in",
      { username, password },
      {
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken") || "",
        },
      },
    )
    .then((response) => response.data);
};
export interface ISignUpVariables {
  name: string;
  email: string;
  username: string;
  password: string;
}

export interface ISignUpSuccess {
  ok: string;
}
export interface ISignUpError {
  error: string;
}
export const signUp = (variables: ISignUpVariables) => {
  return instance
    .post("users/sign-up", variables, {
      headers: {
        "X-CSRFToken": Cookie.get("csrftoken") || "",
      },
    })
    .then((response) => response.data);
};

export const getAmenities = () => {
  return instance.get(`rooms/amenities`).then((response) => response.data);
};

export const getRoomCategories = () => {
  return instance.get(`categories/rooms`).then((response) => response.data);
};

export interface IUploadRoomVariables {
  name: string;
  country: string;
  city: string;
  price: number;
  rooms: number;
  toilets: number;
  description: string;
  address: string;
  pet_friendly: boolean;
  kind: string;
  amenities: number[];
  category: number;
}
export const uploadRoom = (variables: IUploadRoomVariables) => {
  return instance
    .post("rooms/", variables, {
      headers: {
        "X-CSRFToken": Cookie.get("csrftoken") || "",
      },
    })
    .then((response) => response.data);
};

export const getuploadURL = () => {
  return instance
    .post("medias/photos/get-url", null, {
      headers: {
        "X-CSRFToken": Cookie.get("csrftoken") || "",
      },
    })
    .then((response) => response.data);
};

export const uploadImage = ({
  file,
  uploadURL,
}: {
  file: FileList;
  uploadURL: string;
}) => {
  const form = new FormData();
  form.append("file", file[0]);
  return axios
    .post(uploadURL, form, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => response.data);
};

export const uploadRoomPhoto = ({
  file,
  description,
  roomPk,
}: {
  file: string;
  description: string;
  roomPk: string;
}) => {
  return instance
    .post(
      `rooms/${roomPk}/photos`,
      { file, description },
      {
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken") || "",
        },
      },
    )
    .then((response) => response.data);
};

export type checkBookingQueryKey = [string, number?, [Date, Date]?];

export const checkBooking = ({
  queryKey,
}: QueryFunctionContext<checkBookingQueryKey>) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [_, roomPk, dates] = queryKey;
  if (dates) {
    const selectedDates = Array.isArray(dates)
      ? {
          // [x]Timezone is not applied to these codes.
          // checkIn: dates[0]?.toJSON().split("T")[0],
          // checkOut: dates[1]?.toJSON().split("T")[0],
          checkIn: formatDate(dates[0]),
          checkOut: formatDate(dates[1]),
        }
      : dates;
    return instance
      .get(
        `rooms/${roomPk}/bookings/check?check_in=${selectedDates.checkIn}&check_out=${selectedDates.checkOut}`,
      )
      .then((response) => response.data);
  }
};

// * second
// export async function getRooms() {
//   const response = await instance(`rooms/`);
//   return response.data;
// }

// * first
// export async function getRooms() {
// const response = await fetch(`${BASE_URL}/rooms/`);
// const json = await response.json(); // axios do it for you
// return json;
// }
