<template>
  <v-row justify="center" align-content="center" align="center" style="height:100%">
    <v-col>
      TEST CODE IS :::
    </v-col>
    </v-row>
</template>

<script>
export default {
  name: 'AfterDone',
  beforeMount() {
    this.$helpers.isWrongAccess(this)
  }
}
</script>
