<template lang="pug">
    b-navbar(toggleable="lg" type="light" variant="light" sticky).bb.p-0
        b-navbar-brand.my-0.mx-auto.mx-lg-5
            img(src="@/assets/ct_logo.svg" height="96px")
        b-navbar-toggle(target="nav-collapse").mr-5
        b-collapse(id="nav-collapse" is-nav)
            b-navbar-nav.w-100
                b-nav-item.mx-auto(to="/about") About
                b-nav-item.mx-auto(to="/encode") Encode
                b-nav-item.mx-auto(to="/decode") Decode
</template>

<script>
export default {
  name: "Navbar"
};
</script>

<style scoped lang="scss">
    .bb {
        border-bottom: solid rgb(63, 127, 63) 4px;
    }
    #nav-collapse{
        font-family: "Gill Sans MT", sans-serif;
        text-transform: uppercase;
        font-size: 20px;
        letter-spacing: 2px;

    }
</style>
