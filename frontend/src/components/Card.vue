<template>
  <div class="card mt-2">
    <div class="card-header">
      <h3>{{title}}</h3>
    </div>
    <slot></slot>
  </div>
</template>

<script>
	export default {
		name: 'card',
    props: [
      'title'
    ]
	}
</script>

<style scoped>

</style>
