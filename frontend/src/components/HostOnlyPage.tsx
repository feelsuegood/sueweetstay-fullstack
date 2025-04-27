import { useEffect } from "react";
import useUser from "../lib/useUser";
import { useNavigate } from "react-router-dom";

interface IHostOnlyPageProps {
  children: React.ReactNode;
}

// block unloggedin user and not host user
export default function HostOnlyPage({ children }: IHostOnlyPageProps) {
  // in Header.tsx, useUser() is already called so it's cached
  const { isUserLoading, user } = useUser();
  const navigate = useNavigate();
  useEffect(() => {
    if (!isUserLoading) {
      if (!user?.is_host) {
        navigate("/");
      }
    }
  }, [user, isUserLoading, navigate]);
  return <>{children}</>;
}
