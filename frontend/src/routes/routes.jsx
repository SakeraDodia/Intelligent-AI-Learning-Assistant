import { useRoutes } from "react-router-dom";

import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Chat from "../pages/Chat/Chat";
import Profile from "../pages/Profile/Profile";
import MainLayout from "../pages/layouts/MainLayout";
import Signup from "../pages/Signup/Signup";
import ForgotPassword from "../pages/ForgotPassword/ForgotPassword";

function AppRoutes() {
  const routes = useRoutes([
    {
      path: "/",
      element: <Login />,
    },
    {
      path: "/",
      element: <MainLayout />,
      children: [
        {
          path: "dashboard",
          element: <Dashboard />,
        },
        {
          path: "chat",
          element: <Chat />,
        },
        {
          path: "profile",
          element: <Profile />,
        },
        {
          path: "signup",
          element: <Signup />
        },
        {
          path: "forgot-password",
          element: <ForgotPassword />
        }
      ],
    },
  ]);

  return routes;
}

export default AppRoutes;