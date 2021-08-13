<template>
    <v-container fluid fill-height>
        <v-row>
            <Progress style="padding: 3px;"/>
        </v-row>
        <v-row align-content="start">
            <v-col cols="4">
            </v-col>
            <v-col cols="4">
               
                    <image-panel/>
                
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
import ImagePanel from '@/components/ImagePanel.vue'
import Progress from '@/components/Progress.vue'

export default {
    name: "ImageView",
    components: {
        ImagePanel,
        Progress
    },
    data() {
        return {

        }
    },

    mounted: function() {

    },

    methods: {

    }
}
</script>