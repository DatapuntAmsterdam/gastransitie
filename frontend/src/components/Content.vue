<template>
  <div class="outer-wrapper">
    <div class="grid-wrapper wrapper_12 contents-wrapper">
      <div class="grid-container container_12">
        <div class="grid-zone grid_12">
          <section>
            <h1>{{$route.name}}</h1>

            <div class="grid-blok grid_12">
              <div class="grid-element">
                <div class="grid-edge">
                  <div class="grid-inside">
                      <slot></slot>
                  </div>
                </div>
              </div>
            </div>

            <div class="zone-clear clear"></div>
          </section>
        </div>

        <div class="clear"></div>
      </div>

    </div>
  </div>
</template>
