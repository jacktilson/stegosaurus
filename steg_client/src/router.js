import Vue from "vue";
import Router from "vue-router";
import About from "./views/About.vue";
import Decode from "./views/Decode.vue";
import Encode from "./views/NewNewEncode.vue";
import Error from "./views/Error.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      alias: "/about",
      name: "About",
      component: About
    },
    {
      path: "/encode",
      name: "Encode",
      component: Encode
    },
    {
      path: "/decode",
      name: "Decode",
      component: Decode
    },
    {
      path: "*",
      name: "Error",
      component: Error
    }
  ]
});
