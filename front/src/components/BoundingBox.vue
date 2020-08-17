<template>
  <svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">
    <rect id="box" class="bnd" :style="color" style="fill:transparent; stroke-width:1;" :x="x" :y="y" :width="w" :height="h"/>
    <!--
    <template v-if="circle === 'yes'">
      <circle style="stroke:red; fill:red; stroke-width:1.2;" :cx="x+w-1" :cy="y" r="2"/>
    </template>
    -->
  </svg>
</template>

<script>
export default {
  name: 'BoundingBox',
  props: ['color', 'box_info', 'border', 'circle'],
  data() {
    return {
      clicked: true,
      selected: false,
      annotated: false,
    }
  },
  computed: {
    x: function () {
      return parseInt(this.box_info.x_pos)
    },
    y: function () {
      return parseInt(this.box_info.y_pos)
    },
    w: function () {
      return parseInt(this.box_info.x_len) + 2
    },
    h: function () {
      return parseInt(this.box_info.y_len) + 2
    }
    // x: () => {return parseInt(this.box_info.x_pos)},
    // y: () => {return parseInt(this.box_info.y_pos)},
    // w: () => {return parseInt(this.box_info.x_len) + 2},
    // h: () => {return parseInt(this.box_info.y_len) + 2}
  },
  methods: {
    // int: function(elem) {
    //   return parseInt(elem)
    // },
    add: function(li) {
      var res = 0
      for (var elem in li) {
        res += this.int(li[elem])
      }
      return res
    }
  }
}
</script>
