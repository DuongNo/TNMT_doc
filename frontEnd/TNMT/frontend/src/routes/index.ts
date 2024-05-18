import { DefaultLayout, LoginLayout } from "@/layouts";
import { HomePage, LoginPage, AboutPage, MessagePage, NewHome } from "@/pages";

export const publicRoutes = [
  {
    id: 1,
    path: "/",
    page: NewHome,
    layout: DefaultLayout,
  },
  {
    id: 3,
    path: "/home",
    page: HomePage,
    layout: DefaultLayout,
  },
  {
    id: 4,
    path: "/about",
    page: AboutPage,
    layout: DefaultLayout,
  },
  {
    id: 5,
    path: "/message",
    page: MessagePage,
    layout: DefaultLayout,
  },
  {
    id: 6,
    path: "/login",
    page: LoginPage,
    layout: LoginLayout,
  },
  {
    id: 7,
    path: "/new-home",
    page: NewHome,
    layout: DefaultLayout,
  },
];
