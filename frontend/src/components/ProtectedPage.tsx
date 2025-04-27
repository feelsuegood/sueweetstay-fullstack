import { useEffect } from "react";
import useUser from "../lib/useUser";
import { useNavigate } from "react-router-dom";

interface IProtectedPageProps {
  children: React.ReactNode;
}
// block unloggedin user
export default function ProtectedPage({ children }: IProtectedPageProps) {
  // in Header.tsx, useUser() is already called so it's cached
  const { isUserLoading, isLoggedIn } = useUser();
  const navigate = useNavigate();
  useEffect(() => {
    if (!isUserLoading) {
      if (!isLoggedIn) {
        navigate("/");
      }
    }
  }, [isLoggedIn, isUserLoading, navigate]);
  return <>{children}</>;
}
