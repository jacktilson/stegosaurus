<template lang="pug">
    b-navbar(toggleable="lg" sticky)
        .container
            b-navbar-brand.my-0.mx-3
                img(src="/ct_logo.svg" height="96px")
            b-navbar-toggle(target="nav-collapse").my-0.mx-0
                font-awesome-icon(icon="bars" size="2x")
            b-collapse(id="nav-collapse" is-nav).mx-3
                b-navbar-nav.row.w-100.text-lg-center
                    b-nav-item.col-lg(to="/about") About
                    b-nav-item.col-lg(to="/encode") Encode
                    b-nav-item.col-lg(to="/decode") Decode
</template>

<script>
export default {
  name: "Navbar"
};
</script>

<style lang="scss">
.navbar {
  border-bottom: solid rgb(63, 127, 63) 4px;
  background-color: rgb(54, 54, 54);
}

.navbar-toggler {
  color: rgb(63, 127, 63) !important;
}

.nav-link {
  color: rgb(63, 127, 63) !important;
  &:hover {
    transition: 255ms;
    color: rgb(31, 95, 31) !important;
  }
}

#nav-collapse {
  text-transform: uppercase;
  font-size: 20px;
  letter-spacing: 2px;
}
</style>
