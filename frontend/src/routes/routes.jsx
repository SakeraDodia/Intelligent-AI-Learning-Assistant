import { useRoutes } from "react-router-dom";

import Login from "../pages/Login/Login";
import Signup from "../pages/Signup/Signup";
import ForgotPassword from "../pages/ForgotPassword/ForgotPassword";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/Dashboard/Dashboard";
import Chat from "../pages/Chat/Chat";
import PDFChat from "../pages/PDFChat/PDFChat";
import Notes from "../pages/Notes/Notes";
import Quiz from "../pages/Quiz/Quiz";
import Interview from "../pages/Interview/Interview";
import Roadmap from "../pages/Roadmap/Roadmap";
import History from "../pages/History/History";
import Profile from "../pages/Profile/Profile";
import Settings from "../pages/Settings/Settings";
import VerifyOtp from "../pages/VerifyOtp/VerifyOtp";
import ResetPassword from "../pages/ResetPassword/ResetPassword";

function AppRoutes() {
  const routes = useRoutes([
    {
      path: "/",
      element: <Login />,
    },
    {
      path: "/signup",
      element: <Signup />,
    },
    {
      path: "/forgot-password",
      element: <ForgotPassword />
    },
    {
      path: "/verify-otp",
      element: <VerifyOtp />
    },
    {
      path: "/reset-password",
      element: <ResetPassword />
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
          path: "pdf-chat",
          element: <PDFChat />,
        },
        {
          path: "notes",
          element: <Notes />,
        },
        {
          path: "quiz",
          element: <Quiz />,
        },
        {
          path: "interview",
          element: <Interview />,
        },
        {
          path: "roadmap",
          element: <Roadmap />,
        },
        {
          path: "history",
          element: <History />,
        },
        {
          path: "profile",
          element: <Profile />,
        },
        {
          path: "settings",
          element: <Settings />,
        },
      ],
    },
  ]);

  return routes;
}

export default AppRoutes;