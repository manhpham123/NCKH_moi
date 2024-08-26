import { lazy } from "react";
import { RULE } from "../../routes/route.constant";
const rule = lazy(() => import("../Rule"));

export default {
  path: RULE,
  element: rule,
};
