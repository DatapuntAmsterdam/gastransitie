<template>
  <div class="container">
    <header>
      <img class="logo" src="../../static/logo-short.svg">
      <h1><slot></slot></h1>
    </header>
  </div>
</template>

<style lang="scss" scoped>
header {
  margin-top: 10px;
}

.logo {
  height: 45px;
  margin-left: -18px;
  margin-right: 15px;
  float: left;
}
</style>
