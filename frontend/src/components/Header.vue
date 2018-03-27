<template>
  <div class="container mt-2">
    <header>
      <img class="logo" src="../../static/logo-short.svg">
      <h2><b><slot></slot></b></h2>
    </header>
  </div>
</template>

<style lang="scss" scoped>
.logo {
  height: 45px;
  margin-left: -18px;
  margin-right: 15px;
  float: left;
}
</style>
